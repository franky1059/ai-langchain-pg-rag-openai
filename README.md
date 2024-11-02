




OPEN AI api key
---------------------
- https://openai.com/api/





Docker Compose Deployment (db)
-----------------------------------

#### docker compose install (mac)
```
curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o docker-compose

docker-compose –version
```


#### docker compose install (linux - redhat)
```
sudo yum update
sudo yum install -y curl


sudo curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

sudo export PATH=$PATH:/usr/local/bin  # TODO: add this to default user paths

docker-compose –version
```


#### Docker imagees compile and run
```
#export PATH=$PATH:/usr/local/bin 
#docker-compose down --rmi all  # this forces a complete rebuild from scratch, so make sure it's tested in dev first
#docker-compose up
docker-compose up -d  # for daemon mode
```


#### misc cmds
```
docker exec -u 0 -it e6cc8c2b55b6 bash

pg_config --sharedir
```



py setup (dev)
---------------------
```
pip3.9 install virtualenv
python3.9 -m venv venv
source "venv/bin/activate"
```

```
pip3.9 install python-dotenv
```

```
pip3.9 install langchain==0.1.0 openai==1.7.2 langchain-openai==0.0.2 langchain-community==0.0.12 langchainhub==0.1.14
```

```
pip3.9 install psycopg2
pip3.9 install pgvector
```

```
pip3.9 install langchain_postgres
```


```
pip3.9 install numpy && pip3.9 install scipy && pip3.9 install scikit-learn && pip3.9 install pandas && pip3.9 install matplotlib
```



.env setup
---------------------
```
cp .env.example .env
```
- populate active OPENAI_API_KEY





Demo: Hospital data
--------------------------
#### create and test RAGS
```
$ python3.9 langchain_intro/create_retriever.py --mode clean
$ python3.9 langchain_intro/create_retriever.py --mode index --path 'data/reviews.csv' --colname 'reviews'
$ python3.9 langchain_intro/create_retriever.py --mode retrieve  --colname 'reviews'
```

#### use chat with store RAGS TODO, can't get this to work
$ python3.9
>>> from langchain_intro.chatbot import review_chain
>>> question = """Has anyone complained about communication with the hospital staff?"""
>>> review_chain.invoke(question)







Resources
---------------------
- docs - py langchain 0.1 - https://python.langchain.com/v0.1/docs/get_started/introduction/
- docs - py langchain 0.1 -  PGVector - https://python.langchain.com/v0.1/docs/integrations/vectorstores/pgvector/

- Build an LLM RAG Chatbot With LangChain - https://realpython.com/build-llm-rag-chatbot-with-langchain/#step-2-understand-the-business-requirements-and-data
- Using PostgreSQL as a vector database in RAG - https://www.infoworld.com/article/3516109/using-postgresql-as-a-vector-database-in-rag.html
- How to Build LLM Applications With Pgvector Vector Store in LangChain - https://www.timescale.com/blog/how-to-build-llm-applications-with-pgvector-vector-store-in-langchain/
- Docker with postgres and pgvector extension - https://www.thestupidprogrammer.com/blog/docker-with-postgres-and-pgvector-extension/



