from typing import Any, Dict, List, Optional
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import Post, Project
from database import create_document, get_documents, get_collection

app = FastAPI(title="DOT.BATAME API")

# CORS
origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test")
def test() -> Dict[str, Any]:
    # simple db check
    try:
        get_collection("post").estimated_document_count()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@app.get("/api/posts")
def list_posts(limit: int = 6) -> List[Dict[str, Any]]:
    return get_documents("post", {}, limit)


@app.post("/api/posts", status_code=201)
def create_post(post: Post) -> Dict[str, Any]:
    data = post.model_dump()
    try:
        return create_document("post", data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/projects")
def list_projects(limit: int = 6) -> List[Dict[str, Any]]:
    return get_documents("project", {}, limit)


@app.post("/api/projects", status_code=201)
def create_project(project: Project) -> Dict[str, Any]:
    data = project.model_dump()
    try:
        return create_document("project", data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
