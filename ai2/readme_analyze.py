import os.path

from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate


class ReadMeAnalyzer:

    def __init__(self, query):
        self.query = query

    def fill_database(self, markdown_path):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=150
        )

        loader = UnstructuredMarkdownLoader(markdown_path)
        doc = loader.load()
        split_docs = text_splitter.split_documents(doc)

        # Add the unique documents to your database
        return Chroma.from_documents(split_docs, self.query.embeddings)

    def analyze_readme(self, models):
        from langchain.prompts import PromptTemplate

        # Build prompt
        template = """Use the following pieces of context to answer the question at the end. If you don't know the 
        answer, just say that you don't know, don't try to make up an answer. Use only yes or no. Answer yes if the 
        repo is corresponds at least somehow. Keep the answer as concise as possible. As a context, you will receive 
        a repository "readme" file and you need to answer whether this repository corresponds (even weakly) to the 
        question or not.
         
        {context} 
        
        Question: Does the repository corresponds the user's search query (at least somehow, 
        even if the correspondence is really weak): {question}? Helpful Answer:"""
        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

        out_meta = []
        out_description = []
        out_raiting = []

        for model in models:
            vectordb = self.fill_database(model.readme)
            if vectordb is None:
                out_meta.append("")
                out_description.append("")
                out_raiting.append(1)
                continue

            # Run chain
            qa_chain = RetrievalQA.from_chain_type(
                self.query.llm,
                retriever=vectordb.as_retriever(),
                return_source_documents=True,
                chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
            )

            question = self.query.correct_query  # Этот запрос по факту нужен, тот что внизу написан для теста
            # question = "I need project with ml for predict delivery food"

            result = qa_chain({"query": question})
            if result['result'] == "Yes":
                out_meta.append(result['source_documents'][0].metadata['source'])  # save path from right document
                chain = RetrievalQA.from_chain_type(
                    llm=self.query.llm,
                    chain_type="map_reduce",
                    retriever=vectordb.as_retriever()
                )
                q = ("What about this text? Explain it as for a person who does not have a technical education. "
                     "Explain in simple words and to the point, but do not write too much - a maximum of 5 sentences.")
                result = chain({"query": q})
                out_description.append(result['result'])
                # забираем максимальное значение сходства для этого документа
                out_raiting.append(
                    1 - max([doc[1] for doc in [docs for docs in vectordb.similarity_search_with_score(question)]]))
            else:
                out_meta.append("")
                out_description.append("")
                out_raiting.append(1)

            print(out_raiting)

        return out_meta, out_description, out_raiting
