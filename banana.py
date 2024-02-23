import os
from anthropic import Anthropic

from langchain.llms.openai import OpenAIChat
from langchain_community.chat_models import ChatAnthropic
from langchain.chains import RetrievalQA
from langchain.callbacks import StdOutCallbackHandler


from langchain_community.document_loaders import WebBaseLoader

yolo_nas_loader = WebBaseLoader("https://deci.ai/blog/yolo-nas-object-detection-foundation-model/").load()

decicoder_loader = WebBaseLoader("https://deci.ai/blog/decicoder-efficient-and-accurate-code-generation-llm/#:~:text=DeciCoder's%20unmatched%20throughput%20and%20low,re%20obsessed%20with%20AI%20efficiency.").load()

yolo_newsletter_loader = WebBaseLoader("https://deeplearningdaily.substack.com/p/unleashing-the-power-of-yolo-nas").load()


from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50,
    length_function = len
)

yolo_nas_chunks = text_splitter.transform_documents(yolo_nas_loader)

decicoder_chunks = text_splitter.transform_documents(decicoder_loader)

yolo_newsletter_chunks = text_splitter.transform_documents(yolo_newsletter_loader)


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
vectorstore = FAISS.from_documents(yolo_nas_chunks, embedder)

vectorstore.add_documents(decicoder_chunks)

vectorstore.add_documents(yolo_newsletter_chunks)

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
    response = qa_with_sources_chain({"query":"What does Neural Architecture Search have to do with how Deci creates its models?"})
    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "What is going on in london  23 of Feb 2024?",
            }
        ],
        model="claude-2.1",
    )
    print(response.values())


# [START run]
if __name__ == '__main__':
    main()

# [END run]
