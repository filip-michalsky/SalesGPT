from langchain.agents import Tool
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma


def setup_knowledge_base(product_catalog: str = None):
    """
    We assume that the product catalog is simply a text string.
    """
    # load product catalog
    with open(product_catalog, "r") as f:
        product_catalog = f.read()

    text_splitter = CharacterTextSplitter(chunk_size=10, chunk_overlap=0)
    texts = text_splitter.split_text(product_catalog)

    llm = OpenAI(temperature=0)
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_texts(
        texts, embeddings, collection_name="product-knowledge-base"
    )

    knowledge_base = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=docsearch.as_retriever()
    )
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
