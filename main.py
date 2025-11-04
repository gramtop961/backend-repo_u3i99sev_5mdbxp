import os
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import Post as PostSchema, Project as ProjectSchema

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "DOT.BATAME API is running"}


@app.get("/test")
def test_database():
    info = {
        "backend": "running",
        "database": "connected" if db is not None else "not_connected",
        "collections": []
    }
    if db is not None:
        try:
            info["collections"] = db.list_collection_names()
        except Exception as e:
            info["collections_error"] = str(e)
    return info


# -------- Blog: Posts --------
class PostCreate(PostSchema):
    pass

class PostOut(PostSchema):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@app.get("/api/posts", response_model=List[PostOut])
def list_posts(limit: int = 12):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    docs = get_documents("post", {"published": True}, limit)
    # Sort newest first by created_at if available
    docs.sort(key=lambda d: d.get("created_at", datetime.min), reverse=True)
    # Convert ObjectId to string and map fields
    for d in docs:
        if "_id" in d:
            d["id"] = str(d.pop("_id"))
    return docs


@app.get("/api/posts/{slug}", response_model=PostOut)
def get_post(slug: str):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    docs = get_documents("post", {"slug": slug}, 1)
    if not docs:
        raise HTTPException(status_code=404, detail="Post not found")
    d = docs[0]
    d["id"] = str(d.pop("_id")) if "_id" in d else None
    return d


@app.post("/api/posts", response_model=str)
def create_post(payload: PostCreate):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    data = payload.model_dump()
    if data.get("published") and not data.get("published_at"):
        data["published_at"] = datetime.utcnow()
    new_id = create_document("post", data)
    return new_id


# -------- Portfolio: Projects --------
class ProjectCreate(ProjectSchema):
    pass

class ProjectOut(ProjectSchema):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@app.get("/api/projects", response_model=List[ProjectOut])
def list_projects(limit: int = 12):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    docs = get_documents("project", {}, limit)
    docs.sort(key=lambda d: d.get("created_at", datetime.min), reverse=True)
    for d in docs:
        if "_id" in d:
            d["id"] = str(d.pop("_id"))
    return docs


@app.get("/api/projects/{slug}", response_model=ProjectOut)
def get_project(slug: str):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    docs = get_documents("project", {"slug": slug}, 1)
    if not docs:
        raise HTTPException(status_code=404, detail="Project not found")
    d = docs[0]
    d["id"] = str(d.pop("_id")) if "_id" in d else None
    return d


@app.post("/api/projects", response_model=str)
def create_project(payload: ProjectCreate):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    data = payload.model_dump()
    new_id = create_document("project", data)
    return new_id


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
