import csv
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 读取CSV并生成Document列表
def load_medical_data(csv_path):
    docs = []
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 将每条记录拼成一段文本
            text = (
                f"Patient ID: {row['patient_id']}\n"
                f"Age: {row['age']}\n"
                f"Gender: {row['gender']}\n"
                f"Blood Pressure: {row['blood_pressure']}\n"
                f"Blood Glucose: {row['blood_glucose']}\n"
                f"Cholesterol: {row['cholesterol']}\n"
                f"BMI: {row['BMI']}\n"
                f"Diagnosis: {row['diagnosis']}\n"
                f"Doctor Notes: {row['doctor_notes']}\n"
            )
            docs.append(Document(page_content=text, metadata=row))
    return docs

# 可选：进一步分块（如每条100-300字符）
def chunk_documents(docs, chunk_size=300, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunked_docs = []
    for doc in docs:
        chunked_docs.extend(splitter.split_documents([doc]))
    return chunked_docs

if __name__ == "__main__":
    csv_path = "synthetic_medical_data.csv"
    docs = load_medical_data(csv_path)
    chunked_docs = chunk_documents(docs)
    # print(f"total chunk: {len(chunked_docs)}")
    # print(chunked_docs[0].page_content)

    from langchain.vectorstores import FAISS
    from langchain.embeddings import HuggingFaceEmbeddings

    # 1. 初始化嵌入模型
    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")

    # 2. 构建FAISS向量库
    faiss_db = FAISS.from_documents(chunked_docs, embedding_model)

    # 3. 保存索引到本地
    faiss_db.save_local("faiss_medical_index")
    print("FAISS index saved to faiss_medical_index")

    query = "高血糖"
    results = faiss_db.similarity_search(query, k=1)
    print(results[0].page_content)