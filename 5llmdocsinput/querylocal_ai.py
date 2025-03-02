from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load the FAISS database
embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)


# Function to query the stored knowledge base
def ask_question(query):
    docs = vector_store.similarity_search(query, k=3)  # Retrieve top 3 similar results
    print("\n--- Answers from Knowledge Base ---\n")
    for i, doc in enumerate(docs, 1):
        print(f"Answer {i}: {doc.page_content}\n")

# Run the script
if __name__ == "__main__":
    while True:
        user_query = input("\nAsk a question (or type 'exit' to quit): ")
        if user_query.lower() == "exit":
            print("Goodbye!")
            break
        ask_question(user_query)
