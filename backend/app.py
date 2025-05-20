from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from rag import RAGSystem

app = FastAPI(title="RAG System API")

# CORS for multipf application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# Instance of rag class from rag.py
rag_system = RAGSystem()
# data model (pydantic) for validation
class QueryRequest(BaseModel):
    query: str

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file to the RAG system"""
    
    # Check if file is a supported type
    if not (file.filename.endswith('.txt') or 
            file.filename.endswith('.pdf') or 
            file.filename.endswith('.docx')):
        raise HTTPException(
            status_code=400, 
            detail="Only .txt, .pdf, and .docx files are supported"
        )
    
    # Read file content
    content = await file.read()
    
    # For text files, decode as utf-8
    if file.filename.endswith('.txt'):
        content_str = content.decode('utf-8')
    else:
        # For binary files (pdf, docx), write as bytes
        content_str = content
    
    # Save the file
    file_path = rag_system.save_file(content_str, file.filename)
    
    return {"message": f"File '{file.filename}' uploaded successfully", "file_path": file_path}

@app.post("/train")
async def train_system():
    """Train the RAG system on uploaded documents
       load docs -> chunk -> create vector db    
        
    """
    
    success = rag_system.train()
    if success:
        return {"message": "RAG system trained successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to train RAG system")

@app.post("/query")
async def query_system(query_request: QueryRequest):
    """Query the RAG system"""
    
    result = rag_system.query(query_request.query)
    return result

@app.post("/clear")
async def clear_data():
    """Clear all data files and the vector database"""
    
    success = rag_system.clear_data()
    if success:
        return {"message": "All data cleared successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to clear data")
    
@app.get("/status")
async def check_status():
    """Check if the RAG system is ready"""
    
    # Check if the vector database exists
    if os.path.exists(rag_system.chroma_path):
        return {"status": "ready", "message": "RAG system is ready"}
    else:
        return {"status": "not_ready", "message": "RAG system needs training"}

if __name__ == "__main__":
    print("Starting RAG API server on http://localhost:8000")
    print("Run the Streamlit client with: streamlit run client.py")
    uvicorn.run(app, host="localhost", port=8000)