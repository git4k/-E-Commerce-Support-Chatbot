from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

# Cache embeddings model globally
_embeddings = None
_vectorstore = None

def get_embeddings():
    """Get cached embeddings model"""
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
    return _embeddings

def build_vectorstore():
    """Build FAISS index from policy docs - RUN ONCE"""
    loader = DirectoryLoader(
        "data/policies/", 
        glob="*.md",
        show_progress=False
    )
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, 
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)
    
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("faiss_index")
    print(f"✅ Vectorstore saved! {len(chunks)} chunks indexed")
    return vectorstore

def load_vectorstore():
    """Load existing FAISS index with caching"""
    global _vectorstore
    if _vectorstore is None:
        embeddings = get_embeddings()
        _vectorstore = FAISS.load_local(
            "faiss_index", 
            embeddings,
            allow_dangerous_deserialization=True
        )
    return _vectorstore

def search_policy_docs(query: str, k=2) -> str:
    """Search policies - MAIN FUNCTION (optimized)"""
    try:
        vs = load_vectorstore()
        results = vs.similarity_search(query, k=k)
        return "\n\n".join([doc.page_content for doc in results])
    except Exception as e:
        print(f"❌ Error loading: {e}. Building new vectorstore...")
        build_vectorstore()
        return search_policy_docs(query)
