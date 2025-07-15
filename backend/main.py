import os
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from typing import Optional
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import PyPDF2

app = FastAPI()
index_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Document handler/faiss_medical_index"))

embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")
faiss_db = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)

class QueryRequest(BaseModel):
    query: str
    age: Optional[int] = None
    gender: Optional[str] = None
    indicators: Optional[dict] = None
    top_k: int = 3

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

    # 3. 发送给LLM（此处留接口，可对接OpenRouter等）
    # response = call_llm_api(prompt)
    response = "[此处为LLM生成的解释和建议]"

    return {"prompt": prompt, "llm_response": response}


@app.post("/analyze_report")
async def analyze_report(
    file: UploadFile = File(...),
    age: int = Form(...),
    gender: str = Form(...)
):
    # 读取PDF内容
    pdf_reader = PyPDF2.PdfReader(file.file)
    pdf_text = "\n".join(page.extract_text() or "" for page in pdf_reader.pages)

    # 构建英文prompt
    prompt = f"Medical Report Content:\n{pdf_text}\n"
    prompt += f"User Age: {age}\n"
    prompt += f"User Gender: {gender}\n"
    prompt += "\nBased on the above information, please provide an interpretation of the medical report and personalized health advice."

    # response = call_llm_api(prompt)
    response = "[LLM analysis result here]"
    return {"prompt": prompt, "llm_response": response}
