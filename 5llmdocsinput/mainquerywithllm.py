from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import GPT4All  # Ensure GPT4All is correctly installed

# Load FAISS database
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # Replace with your chosen model
vector_store_path = "faiss_index"  # Ensure this file exists from previous indexing

# Load embeddings model
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)


# Load LLM
llm = GPT4All(model="D:/hermes3llama3/H3Ll323BQ4KM.gguf")  # Update path to your model

def query_knowledge_base(question):
    """
    Queries FAISS for relevant document chunks and passes them to LLM for an answer.
    """
    print("🔍 Searching FAISS for relevant chunks...")
    docs = vector_store.similarity_search(question, k=5)  # Retrieve more chunks
    retrieved_text = " ".join([doc.page_content for doc in docs])

    # First attempt to answer
    prompt = f"""You are an AI assistant. Answer the question based on the document below:
    
    Document: {retrieved_text}
    
    Question: {question}
    Answer:"""
    response = llm.invoke(prompt)

    # If response lacks context, retrieve more
    if "Not enough context" in response:
        print("🔄 Re-querying FAISS for additional context...")
        docs = vector_store.similarity_search(question, k=10)  # Retrieve more chunks
        retrieved_text = " ".join([doc.page_content for doc in docs])
        response = llm.invoke(f"{retrieved_text}\n\nQuestion: {question}\nAnswer:")
    
    return response

if __name__ == "__main__":
    while True:
        user_query = input("Ask a question (or type 'exit' to quit): ")
        if user_query.lower() == "exit":
            break
        answer = query_knowledge_base(user_query)
        print("\n🤖 AI Response:", answer)
