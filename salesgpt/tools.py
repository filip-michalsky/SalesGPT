import os
from langchain.agents import Tool
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain


def setup_knowledge_base(product_catalog: str = None):

    if os.path.exists(product_catalog):
        return setup_knowledge_base_from_text(product_catalog)
    else:
        return setup_knowledge_base_from_db()


def setup_knowledge_base_from_text(product_catalog: str):
    """
    We assume that the product catalog is simply a text string.
    """
    # load product catalog
    with open(product_catalog, "r") as f:
        product_catalog = f.read()

    text_splitter = CharacterTextSplitter(chunk_size=1024, chunk_overlap=32)
    texts = text_splitter.split_text(product_catalog)

    llm = ChatOpenAI(temperature=0, model_name=os.environ.get('MODEL_NAME'))
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_texts(
        texts, embeddings, collection_name="product-knowledge-base"
    )

    knowledge_base = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=docsearch.as_retriever()
    )
    return knowledge_base


def setup_knowledge_base_from_db():
    db = SQLDatabase.from_uri(os.environ.get('DB_SQL_URL'))
    llm = ChatOpenAI(temperature=0, model_name=os.environ.get('MODEL_NAME'))
    knowledge_base = SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=True)
    return knowledge_base


def get_tools(knowledge_base):
    # we only use one tool for now, but this is highly extensible!
    tools = [
        Tool(
            name="ProductSearch",
            func=knowledge_base.run,
            description="useful for when you need to answer questions about product information",
        )
    ]

    return tools
