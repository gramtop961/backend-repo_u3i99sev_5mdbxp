"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
Each Pydantic model represents a collection in your database.
Class name lowercased becomes the collection name.

Example: class Post(BaseModel) -> collection "post"
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import datetime


class Post(BaseModel):
    """
    Blog posts about Batam's hidden gems, cafes, guides, etc.
    Collection name: "post"
    """
    title: str = Field(..., description="Post title")
    slug: str = Field(..., description="URL-friendly unique slug")
    excerpt: Optional[str] = Field(None, description="Short summary for cards and SEO")
    content: Optional[str] = Field(None, description="Rich text/markdown content")
    cover_image: Optional[HttpUrl] = Field(None, description="Hero/cover image URL")
    tags: List[str] = Field(default_factory=list, description="Topic tags like cafe, guide, hidden-gem")
    area: Optional[str] = Field(None, description="Neighborhood/area e.g., Barelang, Nagoya")
    published: bool = Field(default=True, description="Whether visible on site")
    published_at: Optional[datetime] = Field(None, description="Publish timestamp")


class Project(BaseModel):
    """
    Portfolio / curation projects and brand features.
    Collection name: "project"
    """
    title: str = Field(..., description="Project title")
    slug: str = Field(..., description="URL-friendly unique slug")
    summary: Optional[str] = Field(None, description="Short description for cards")
    images: List[HttpUrl] = Field(default_factory=list, description="Image gallery URLs")
    client: Optional[str] = Field(None, description="Client or brand name")
    year: Optional[int] = Field(None, description="Year of project")
    category: Optional[str] = Field(None, description="Type e.g., editorial, branding, curation")
    featured: bool = Field(default=False, description="Whether to highlight on home")


# You can add more collections later (e.g., place, stay, dine) following the same pattern.
