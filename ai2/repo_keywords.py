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
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain_community.embeddings import HuggingFaceEmbeddings

sys.path.append('../..')

from dotenv import load_dotenv



load_dotenv()  # read local .env file

# openai.api_key = os.getenv('OPENAI_API_KEY')


class MyLLM:
    def __init__(self, max_new_tokens=512, do_sample=False, top_k=50, top_p=0.95, num_return_sequences=1):
        print("-" * 50)
        print("Load tokenizer")
        self.tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-7b-instruct-v1.5",
                                                       trust_remote_code=True)
        print("-" * 50)
        print("Load model")
        self.model = AutoModelForCausalLM.from_pretrained("deepseek-ai/deepseek-coder-7b-instruct-v1.5",
                                                          trust_remote_code=True).cuda()
        print("-" * 50)
        print("Finish load")

        self.messages = [
            # { 'role': 'user', 'content': "write a quick sort algorithm in python."}
            {'role': 'user', 'content': "Hello! How are you?"}
        ]
        self.max_new_tokens = max_new_tokens
        self.do_sample = do_sample
        self.top_k = top_k
        self.top_p = top_p
        self.eos_token_id = self.tokenizer.eos_token_id
        self.num_return_sequences = num_return_sequences

    def invoke(self, message=None):
        self.messages = message if message is not None else self.messages
        inputs = self.tokenizer.apply_chat_template(self.messages, add_generation_prompt=True, return_tensors="pt").to(
            self.model.device)

        outputs = self.model.generate(
            inputs,
            max_new_tokens=self.max_new_tokens,
            do_sample=self.do_sample,
            top_k=self.top_k,
            top_p=self.top_p,
            num_return_sequences=self.num_return_sequences,
            eos_token_id=self.eos_token_id
        )

        answer = self.tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True)
        print(answer)

        return answer

class Query:
    def __init__(self, user_query):
        # self.llm_name = "gpt-3.5-turbo"
        self.embeddings = HuggingFaceEmbeddings()
        self.llm = MyLLM()
        self.user_query = user_query
        self.correct_query = None

    def get_correct_query(self):
        messages=[
            { 'role': 'system', 'content': "You are an expert at finding repositories on GitHub. A person who does not know how to make such requests has contacted you, he writes a request in simple words, and your task is to make a competent and relevant request. As a response, you need to give only the text of the request that you recommend. Answer only english language"},
            { 'role': 'user', 'content': "User request: " + self.user_query}
        ]

        answer = self.llm.invoke(messages)

        return answer

    def get_key_queries_from_correct_query(self):
        self.correct_query = self.get_correct_query()

        messages=[
            { 'role': 'system', 'content': "You are an expert at finding repositories on GitHub. You have been contacted by the person who made up the query, and your task is to use keywords from the user's query to write 5 short queries that the user can best search for. Use no more than 3 words in one search query. Be brief. Write requests separated by commas. Answer only english language"},
            { 'role': 'user', 'content': "User request: " + self.correct_query}
        ]

        answer = self.llm.invoke(messages)

        return answer