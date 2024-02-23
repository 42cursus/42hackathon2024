import os
from anthropic import Anthropic

from langchain.llms.openai import OpenAIChat
from langchain_community.chat_models import ChatAnthropic
from langchain.chains import RetrievalQA
from langchain.callbacks import StdOutCallbackHandler


from langchain_community.document_loaders import WebBaseLoader

cultural_dataset_loader = WebBaseLoader("https://zenodo.org/records/5225053/files/CrossCulturalData.csv").load()


from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50,
    length_function = len
)

dataset_chunking = text_splitter.transform_documents(cultural_dataset_loader)


from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.storage import LocalFileStore

store = LocalFileStore("./cachce/")

# create an embedder
core_embeddings_model = OpenAIEmbeddings()

embedder = CacheBackedEmbeddings.from_bytes_store(
    core_embeddings_model,
    store,
    namespace = core_embeddings_model.model
)

# store embeddings in vector store
vectorstore = FAISS.from_documents(cultural_dataset_loader, embedder)

vectorstore.add_documents(cultural_dataset_loader)

vectorstore.add_documents(dataset_chunking)

# instantiate a retriever
retriever = vectorstore.as_retriever()


client = Anthropic(
    # This is the default and can be omitted
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

llm = ChatAnthropic()
handler = StdOutCallbackHandler()

qa_with_sources_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    callbacks=[handler],
    return_source_documents=True
)


def main():
    print("Hello");
    response = qa_with_sources_chain({
        "query": "From an expert Cultural advisor what is the tradition in London ?"
    })
    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "What are the content inside the document ? ",
            }
        ],
        model="claude-2.1",
    )
    print(response.values())


# [START run]
if __name__ == '__main__':
    main()

# [END run]
