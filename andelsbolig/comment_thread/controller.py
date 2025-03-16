from fastapi import APIRouter, Depends, HTTPException

from andelsbolig.advertisement.repository import AdvertisementRepository
from andelsbolig.misc.logger import get_logger
from andelsbolig.security.service import is_authenticated, is_subscribed
from andelsbolig.comment_thread.model import CommentThread, CommentCreate, Comment
from andelsbolig.comment_thread.repository import ThreadRepository

router = APIRouter()
db = ThreadRepository()
advertisement_db = AdvertisementRepository()
logger = get_logger(__name__)


@router.get("/thread/{_id}")
def get_thread(_id: str, _=Depends(is_subscribed)) -> CommentThread:
    thread = db.read({"referenced_id": _id})
    if not thread:
        raise HTTPException(status_code=404, detail="thread not found")
    return thread


@router.post("/comment")
def post_comment(comment_create: CommentCreate, jwt=Depends(is_subscribed)):
    """Attach comment to a thread"""
    # Ensure advertisement exists
    advertisement = advertisement_db.read({"_id": comment_create.referenced_id})
    if advertisement is None:
        raise HTTPException(status_code=400, detail="Referenced object not found")

    # Ensure thread exists for this comment
    thread = db.read({"referenced_id": comment_create.referenced_id})
    if thread is None:
        db.create(CommentThread(referenced_id=comment_create.referenced_id))

    comment = Comment(user_id=jwt.sub, full_name=jwt.full_name, text=comment_create.text)
    db.update({"referenced_id": comment_create.referenced_id}, {"$push": {"comments": comment.model_dump()}})
    pass
