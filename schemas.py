from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field


class Post(BaseModel):
    title: str
    slug: str = Field(pattern=r"^[a-z0-9\-]+$")
    excerpt: Optional[str] = None
    content: str
    coverImage: Optional[HttpUrl] = None
    tags: List[str] = []
    area: Optional[str] = None
    published: bool = True


class Project(BaseModel):
    title: str
    slug: str = Field(pattern=r"^[a-z0-9\-]+$")
    summary: Optional[str] = None
    images: List[HttpUrl] = []
    client: Optional[str] = None
    year: Optional[int] = None
    category: Optional[str] = None
    featured: bool = False
