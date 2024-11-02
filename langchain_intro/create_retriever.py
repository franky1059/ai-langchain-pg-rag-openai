import os, sys

from langchain.document_loaders.csv_loader import CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.vectorstores.pgvector import DistanceStrategy
import langchain_postgres 

import dotenv
import psycopg2

import utils


dotenv.load_dotenv()


MY_DB_HOST = os.environ['MY_DB_HOST']
MY_DB_PORT = os.environ['MY_DB_PORT']
MY_DB_NAME = os.environ['MY_DB_NAME']
MY_DB_USER = os.environ['MY_DB_USER']
MY_DB_PASSWORD = os.environ['MY_DB_PASSWORD']

CONNECTION_STRING = f"postgresql+psycopg2://{MY_DB_USER}:{MY_DB_PASSWORD}@{MY_DB_HOST}:{MY_DB_PORT}/{MY_DB_NAME}"




def mode_index(args):

	CSV_PATH = args.path
	APP_COLLECTION_NAME = args.colname

	loader = CSVLoader(file_path=CSV_PATH, source_column="review")
	reviews = loader.load()

	# APP DEBUG START
	print('__file__: ' + __file__ + ' ')
	utils.debug_info()
	print('reviews[0]: ')
	utils.debug_pprint(reviews[0])
	# APP DEBUG END

	embeddings = OpenAIEmbeddings()
	

	#https://github.com/langchain-ai/langchain/blob/v0.1.0/libs/core/langchain_core/vectorstores.py
	#https://github.com/langchain-ai/langchain/blob/3b0b7cfb7455c973e73dbd00a42fda65a33a9286/libs/community/langchain_community/vectorstores/pgvector.py#L233
	db = PGVector.from_documents(
	    documents= reviews,
	    embedding = embeddings,
	    collection_name= APP_COLLECTION_NAME,
	    distance_strategy = DistanceStrategy.COSINE,
	    connection_string=CONNECTION_STRING)



def mode_rag_retrieve(args):
	APP_COLLECTION_NAME = args.colname
	
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





def mode_clean(args):


	APP_COLLECTION_NAME = args.colname
	embeddings = OpenAIEmbeddings()

	vectorstore = langchain_postgres.PGVector(
	    embeddings=embeddings,
	    collection_name=APP_COLLECTION_NAME,
	    connection=CONNECTION_STRING,
	    use_jsonb=True,
	)

	vectorstore.drop_tables()


	conn = psycopg2.connect(
	    host=MY_DB_HOST,
	    port=MY_DB_PORT,
	    dbname=MY_DB_NAME,
	    user=MY_DB_USER,
	    password=MY_DB_PASSWORD
	)
	cur = conn.cursor()

	cur.execute('''
		DROP TABLE IF EXISTS langchain_pg_collection CASCADE;
	    DROP TABLE IF EXISTS langchain_pg_embedding CASCADE;
	''')
	conn.commit()







if __name__ == '__main__':
	cli_args, unknown = utils.get_arg_parser().parse_known_args(args=sys.argv[1:])

	if cli_args.mode.lower() == 'index':
		mode_index(cli_args)
	elif cli_args.mode.lower() == 'clean':
		mode_clean(cli_args)
	elif cli_args.mode.lower() == 'retrieve':
		mode_rag_retrieve(cli_args)

	## APP DEBUG START
	#print('__file__: ' + __file__ + ' ')
	#utils.debug_info()
	#print('args: ')
	#utils.debug_pprint(args)
	## APP DEBUG END
