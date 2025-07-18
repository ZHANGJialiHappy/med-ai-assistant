import os
from fastapi import FastAPI, File, UploadFile, Form
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import PyPDF2
from backend.schemas import QueryRequest
from backend.openrouter_client import ask_model

app = FastAPI()
index_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Document handler/faiss_medical_index"))

embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")
faiss_db = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)


@app.post("/rag_query")
async def rag_query(req: QueryRequest):

    results = faiss_db.similarity_search(req.query, k=req.top_k)
    retrieved_texts = [doc.page_content for doc in results]

    prompt = f"User Query: {req.query}\n"
    prompt += f"User Age: {req.age}\n" if req.age else ""
    prompt += f"User Gender: {req.gender}\n" if req.gender else ""
    if req.indicators:
        prompt += f"User Indicators: {req.indicators}\n"
    prompt += "Relevant Medical Texts:\n" + "\n---\n".join(retrieved_texts)
    prompt += "\nBased on the above information, please provide an interpretation of the medical report and personalized health advice."

    result = ask_model(prompt)
    return {"result": result}
    # return {"result": "12"}


@app.post("/analyze_report")
async def analyze_report(
    file: UploadFile = File(...),
    age: int = Form(...),
    gender: str = Form(...)
):
    pdf_reader = PyPDF2.PdfReader(file.file)
    pdf_text = "\n".join(page.extract_text() or "" for page in pdf_reader.pages)

    prompt = f"Medical Report Content:\n{pdf_text}\n"
    prompt += f"User Age: {age}\n"
    prompt += f"User Gender: {gender}\n"
    prompt += "\nBased on the above information, please provide an interpretation of the medical report and personalized health advice."

    result = ask_model(prompt)
    return {"result": result}
