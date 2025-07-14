from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

if __name__ == "__main__":

    from langchain.vectorstores import FAISS


    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")
    faiss_db = FAISS.load_local("faiss_medical_index", embedding_model, allow_dangerous_deserialization=True)


    query = "高血糖"
    results = faiss_db.similarity_search(query, k=1)
    print(results[0].page_content)