import os
from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import PyPDFLoader , TextLoader

file_path = "sample_text.txt"

if file_path.endswith(".pdf"):
    laoder = PyPDFLoader(file_path)
elif file_path.endswith(".txt"):
    loader = TextLoader(file_path,encoding="utf-8")

document = loader.load()
print("file loaded successfully")

# step 1 - Text splitting

from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50
)

chunks = splitter.split_documents(document)

print(f"Splitting is done total chunks are {len(chunks)}")

# Step 2 - Generating embeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model is ready")

# Step 3 - Vector Stores

from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(chunks,embeddings)

# Step 4 - Retrievers

retriever = vectorstore.as_retriever(
    search_type = "similarity",
    search_kwargs = {"k":3}
)

# Now finally connecting everything

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system","you are a helpful AI assistant , Use the context below to answer users questions."),
    ("human","Context : {context},\n Question : {question}")
])

llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    temperature= 0,
    api_key=os.getenv("GROQ_API_KEY")
)

chain = prompt | llm

# Intraction wit everything

print("RAG system is ready Ask any questions related to Document")

while True:
    question = input("Your Question :- ")

    if question == "":
        continue
    elif question == "quit":
        break

    retrieved_chunks = retriever.invoke(question)

    context = "\n".join([doc.page_content for doc in retrieved_chunks])

    response = chain.invoke({"context" : context , "question" : question})

    print(f"Answer: \n {response.content}")