import os,sys 

import dotenv

from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from langchain.schema.runnable import RunnablePassthrough
#from langchain_postgres import PGVector
from langchain.vectorstores.pgvector import PGVector
import langchain_postgres 

from langchain_openai import ChatOpenAI

from pydantic import BaseModel, Field, validator
#import langchain.prompts 

from langchain_core.prompts.prompt import (
    PromptTemplate
)

from langchain_core.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)


dotenv.load_dotenv()


MY_DB_HOST = os.environ['MY_DB_HOST']
MY_DB_PORT = os.environ['MY_DB_PORT']
MY_DB_NAME = os.environ['MY_DB_NAME']
MY_DB_USER = os.environ['MY_DB_USER']
MY_DB_PASSWORD = os.environ['MY_DB_PASSWORD']

CONNECTION_STRING = f"postgresql+psycopg2://{MY_DB_USER}:{MY_DB_PASSWORD}@{MY_DB_HOST}:{MY_DB_PORT}/{MY_DB_NAME}"


APP_COLLECTION_NAME = 'reviews'
embeddings = OpenAIEmbeddings()

vectorstore = PGVector(
    collection_name=APP_COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
    embedding_function=embeddings
)

reviews_retriever  = vectorstore.as_retriever()

#print(vectorstore.similarity_search("hospital", k=10))
print(vectorstore.similarity_search("hospital", k=10, filter={"patient_name": {"$like": "chris"}}))
#sys.exit()

# review_template_str = """Your job is to use patient
# reviews to answer questions about their experience at
# a hospital. Use the following context to answer questions.
# Be as detailed as possible, but don't make up any information
# that's not from the context. If you don't know an answer, say
# you don't know.

# {context}
# """

# review_system_prompt = SystemMessagePromptTemplate(
#     prompt=PromptTemplate(
#         input_variables=["context"],
#         template=review_template_str,
#     )
# )

# review_human_prompt = HumanMessagePromptTemplate(
#     prompt=PromptTemplate(
#         input_variables=["question"],
#         template="{question}",
#     )
# )
# messages = [review_system_prompt, review_human_prompt]

# review_prompt_template = ChatPromptTemplate(
#     input_variables=["context", "question"],
#     messages=messages,
# )

# chat_model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

# review_chain = (
#     {"context": reviews_retriever, "question": RunnablePassthrough()}
#     | review_prompt_template
#     | chat_model
#     | StrOutputParser()
# )

template = """Your job is to use patient
reviews to answer questions about their experience at
a hospital. Use the following context to answer questions.
Be as detailed as possible, but don't make up any information
that's not from the context. If you don't know an answer, say
you don't know.:

{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)


def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


chain = (
    {"context": reviews_retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)


chain.invoke("Has anyone complained about communication with the hospital staff?")