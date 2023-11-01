import os, json
from tortoise import Tortoise
from sqlalchemy import make_url
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.text_splitter import SpacyTextSplitter
from llama_index import SimpleDirectoryReader, LLMPredictor, ServiceContext, StorageContext, load_index_from_storage
from llama_index.indices.vector_store import VectorStoreIndex
from llama_index.vector_stores import PGVectorStore
from llama_index.node_parser import SimpleNodeParser
from salesgpt.models import ChatMessage
import pytest


async def init_db():
    await Tortoise.init(
        db_url=os.environ.get('DB_URL'),
        modules={'models': ['__main__']},
    )


async def db_close():
    await Tortoise.close_connections()


class TestDatabase:

    def test_product_catalog(self, load_env):
        db = SQLDatabase.from_uri(os.environ.get('DB_SQL_URL'))
        llm = ChatOpenAI(temperature=0, model_name=os.environ.get('MODEL_NAME'))
        db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
        response = db_chain.run('which product has the highest price and give me its description')
        assert response is not None, "Agent output cannot be None."

    @pytest.mark.asyncio
    async def test_product_catalog_async(self, load_env):
        """Async Test Hello World"""
        try:
            await init_db()
            conn = Tortoise.get_connection('default')
            values = await conn.execute_query('select * from product_catalog')
            print(values)
        finally:
            await db_close()
        assert "Hello World" is not None, "Agent output cannot be None."

    def test_document_load(self, load_env):
        llm = ChatOpenAI(temperature=0, model_name=os.environ.get('MODEL_NAME'))
        llmPredictor = LLMPredictor(llm=llm)
        textSplitter = SpacyTextSplitter(pipeline="zh_core_web_sm", chunk_size=2048)
        nodeParser = SimpleNodeParser(text_splitter=textSplitter)
        documents = SimpleDirectoryReader("./test_data/luxun").load_data()
        nodes = nodeParser.get_nodes_from_documents(documents)
        serviceContext = ServiceContext.from_defaults(llm_predictor=llmPredictor)
        url = make_url(os.environ.get('DB_SQL_URL'))
        vector_store = PGVectorStore.from_params(
            database='salesgpt',
            table_name="luxun_essay",
            host=url.host,
            password=url.password,
            port=url.port,
            user=url.username,
            embed_dim=1536,  # openai embedding dimension
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex(
            nodes=nodes,
            serviceContext=serviceContext,
            storage_context=storage_context,
            show_progress=True
        )
        assert index is not None, "Agent output cannot be None."

    def test_document_index(self, load_env):
        llm = ChatOpenAI(temperature=0, model_name=os.environ.get('MODEL_NAME'))
        llmPredictor = LLMPredictor(llm=llm)
        service_context = ServiceContext.from_defaults(llm_predictor=llmPredictor)
        url = make_url(os.environ.get('DB_SQL_URL'))
        vector_store = PGVectorStore.from_params(
            database='salesgpt',
            table_name="luxun_essay",
            host=url.host,
            password=url.password,
            port=url.port,
            user=url.username,
            embed_dim=1536,  # openai embedding dimension
        )
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        query_engine = index.as_query_engine(
            service_context=service_context,
            response_mode="tree_summarize",
            verbose=True,
        )
        response = query_engine.query('《藤野先生》的作者是谁?')
        print(str(response))
        assert str(response) is not None, "Agent output cannot be None."

