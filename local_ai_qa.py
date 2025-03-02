import os
import glob
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Define the knowledge base folder
KB_FOLDER = "kb"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Explicitly defining an embedding model


def load_pdfs(folder):
    """Loads all PDFs from the specified folder."""
    pdf_files = glob.glob(os.path.join(folder, "*.pdf"))
    documents = []
    
    for pdf in pdf_files:
        print(f"Loading {pdf}...")
        loader = PyPDFLoader(pdf)
        docs = loader.load()
        documents.extend(docs)
    
    return documents


def create_vector_store(documents):
    """Processes documents, splits them, and creates a FAISS vector store."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=100
    )
    texts = text_splitter.split_documents(documents)
    
    # Initialize embeddings with an explicitly defined model
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    vectorstore = FAISS.from_documents(texts, embeddings)
    vectorstore.save_local("faiss_index")
    return vectorstore


def main():
    print("Loading PDFs from 'kb' folder...")
    documents = load_pdfs(KB_FOLDER)
    
    if not documents:
        print("No documents found in kb folder.")
        return
    
    print("Creating FAISS vector database...")
    vectorstore = create_vector_store(documents)
    print("Vector database created and stored successfully!")


if __name__ == "__main__":
    main()
