from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
import os
from ingest import RepoIngestor
from rag import Rag
import traceback

app = FastAPI(title="GitHub RAG API", description="Ingest GitHub repos and query with RAG")

# Add CORS middleware for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class IngestRequest(BaseModel):
    github_url: str

class QueryRequest(BaseModel):
    query: str

class IngestResponse(BaseModel):
    success: bool
    message: str
    files_created: List[str] = []

class QueryResponse(BaseModel):
    response: str
    sources: List[str]

# Global instances
ingestor = RepoIngestor()
rag = Rag()

@app.get("/")
async def root():
    return {"message": "GitHub RAG API is running"}

@app.post("/ingest", response_model=IngestResponse)
async def ingest_repo(request: IngestRequest):
    """Ingest a GitHub repository"""
    try:
        github_url = request.github_url.strip()
        
        if not github_url:
            raise HTTPException(status_code=400, detail="GitHub URL is required")
        
        # Simple function call to ingest repo
        success = ingestor.ingest_repo(github_url)
        
        if not success:
            return IngestResponse(
                success=False,
                message="Failed to ingest repository. Please check the URL and try again."
            )
        
        # Get created filenames
        content_file = ingestor.get_filename(github_url)
        tree_file = ingestor.get_tree_filename(github_url)
        
        # Train the RAG model
        train_success = rag.train(github_url)
        
        if not train_success:
            return IngestResponse(
                success=False,
                message="Repository ingested but RAG training failed."
            )
        
        return IngestResponse(
            success=True,
            message=f"Successfully ingested and trained on repository: {github_url}",
            files_created=[content_file, tree_file]
        )
        
    except Exception as e:
        print(f"Error in ingest_repo: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """Query the RAG system"""
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query is required")
        
        # Check if RAG database exists
        if not os.path.exists(rag.chroma_dir):
            raise HTTPException(
                status_code=400, 
                detail="No knowledge base found. Please ingest a repository first."
            )
        
        # Simple function call to query - using the method that takes query_text parameter
        result = rag.search_and_answer(request.query)
        
        return QueryResponse(
            response=result["response"],
            sources=result["sources"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in query_rag: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/status")
async def get_status():
    """Get system status"""
    try:
        # Check if database exists
        db_exists = os.path.exists(rag.chroma_dir)
        
        # Get list of ingested repos
        ingested_repos = []
        if hasattr(ingestor, 'list_ingested_repos'):
            ingested_repos = ingestor.list_ingested_repos()
        
        return {
            "database_exists": db_exists,
            "ingested_repositories": ingested_repos,
            "total_repos": len(ingested_repos)
        }
    except Exception as e:
        print(f"Error in get_status: {str(e)}")
        return {
            "database_exists": False,
            "ingested_repositories": [],
            "total_repos": 0,
            "error": str(e)
        }

@app.delete("/reset")
async def reset_database():
    """Reset the entire database"""
    try:
        import shutil
        
        # Remove chroma database
        if os.path.exists(rag.chroma_dir):
            shutil.rmtree(rag.chroma_dir)
        
        # Remove processed files tracking
        if os.path.exists(rag.processed_files_path):
            os.remove(rag.processed_files_path)
        
        return {"message": "Database reset successfully"}
        
    except Exception as e:
        print(f"Error in reset_database: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to reset database: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)