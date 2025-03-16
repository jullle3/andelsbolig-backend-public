import time
from typing import List

from bson import ObjectId
from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    """
    User facing model for creating a new comment .
    """

    text: str
    referenced_id: str  # ID of the object being commented on


class Comment(BaseModel):
    """
    Model representing a comment.
    """

    user_id: str  # ID of the user who made the comment
    full_name: str  # Name of the user who made the comment
    text: str
    timestamp: int = Field(default_factory=lambda: int(time.time()))


class CommentThread(BaseModel):
    """
    Model representing a thread of comments.
    """

    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    referenced_id: str  # ID of the object being commented on
    comments: List[Comment] = []
