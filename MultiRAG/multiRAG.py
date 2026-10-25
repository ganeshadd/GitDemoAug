## Start local LLM
## PDF,Doc,txt,md reader
## PDF Chunking
## Embeddings : Convert thext into numbers in semantic pattern
## Vector Data base: Store these numbers and find similar context based on the search
## LLM for processing the information
## Conversation loop

import os
from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFLoader,TextLoader,UnstructuredWordDocumentLoader,UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage,AIMessage


##1. Start Local LLM
llm =ChatOllama(
    model="llama3.2:3b",
    base_url="http://localhost:11434"
)
print("Local LLM started")

## Load all the files in the folder
DATA_PATH="./knowledge"
documents=[]
for file in os.listdir(DATA_PATH):
    print(f"Processing File: {file}")

    if file.endswith(".pdf"):
        loader=PyPDFLoader(os.path.join((DATA_PATH),file))
        documents.extend(loader.load())

    elif file.endswith(".txt"):
        loader=TextLoader(os.path.join((DATA_PATH),file))
        documents.extend(loader.load())

    elif file.endswith(".docx"):
        loader=UnstructuredWordDocumentLoader(os.path.join((DATA_PATH),file))
        documents.extend(loader.load()) 

    elif file.endswith(".md"):
        loader=UnstructuredFileLoader(os.path.join((DATA_PATH),file))
        documents.extend(loader.load())

    else:
        print("Unsupported file format: {file}")   

## 3. Chunking
text_splitter= RecursiveCharacterTextSplitter(chunk_size =100,chunk_overlap=10)
chunks =text_splitter.split_documents(documents)
print(f"Total chunks created: {len(chunks)}")   

## 4. Embeddings exit
embeddings=OllamaEmbeddings(model="nomic-embed-text")

## 5. Vector Data base
vectorstore = Chroma.from_documents(documents=chunks,embedding=embeddings,persist_directory="./MultifileRAG_db")
retriever =vectorstore.as_retriever(search_kwargs={"k":1})
print("Vector DB Created")

## 6. LLM for processing the information

prompt =ChatPromptTemplate.from_messages([
    ("system","You are a helpful assistant.You must give the infomation from the uploaded document and do not provide any information outside of the given document ."),
    ("system","{history}"),
    ("system","{context}"),
    ("human","{input}")
])

chat_history=[]
print("\n Multifile conversational RAG,(Type 'exit' to end the convesation)\n")
    
## 7.Conversation loop
while True:
    user_input=input("User Input::")
    if user_input.lower()=="exit":
        print("Conversation Ended.")
        break

    retrieved_docs= retriever.invoke(user_input)
    context="\n".join([doc.page_content for doc in retrieved_docs])
    print(f"Retrieved context: \n {context} \n")

    chat_history.append(HumanMessage(content=user_input))
    response= llm.invoke(prompt.format(history=chat_history,context=context,input=user_input))
    chat_history.append(AIMessage(content=response.content))
    print(f"AI Response::{response.content} \n")