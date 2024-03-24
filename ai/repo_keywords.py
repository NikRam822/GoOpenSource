import typing
import os
import openai
import sys
from getpass import getpass
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
import hashlib
import chromadb
import uuid
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

sys.path.append('../..')

from dotenv import load_dotenv



load_dotenv()  # read local .env file

openai.api_key = os.getenv('OPENAI_API_KEY')
class Query:

    def __init__(self, user_query):
        self.llm_name = "gpt-3.5-turbo"
        self.embedding = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model_name=self.llm_name, temperature=0)
        self.user_query = user_query
        self.correct_query = None

    def get_correct_query(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system",
             """You are an expert at finding repositories on GitHub. A person who does not know how to make such requests has contacted you, he writes a request in simple words, and your task is to make a competent and relevant request. As a response, you need to give only the text of the request that you recommend. Answer only english language"""),
            ("user", "User request: {user_query}")
        ])

        chain = prompt | self.llm

        return chain.invoke({"user_query": self.user_query}).content

    def get_key_queries_from_correct_query(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system",
             """You are an expert at finding repositories on GitHub. You have been contacted by the person who made 
             up the query, and your task is to use keywords from the user's query to write 5 short queries that the 
             user can best search for. Use no more than 3 words in one search query. Be brief. The requests must be 
             separated by commas. Answer only english language"""),
            ("user", "User request: {user_query}")
        ])

        chain = prompt | self.llm

        self.correct_query = self.get_correct_query()

        return chain.invoke({"user_query": self.correct_query}).content

    def extract_keywords(input: str) -> typing.List[str]:
        different_keywords = input.split(";")

        return [
            *different_keywords,  # отдельные кейворды
            " ".join(different_keywords),  # общий запрос, вдруг что-нибудь найдём
        ]
