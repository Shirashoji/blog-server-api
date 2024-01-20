from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session


from api.dps import get_db
from api import auth
from common import schemas, crud

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/comment/", response_model=list[schemas.Comment], tags=["comment"])
def read_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = crud.get_comments(db, skip=skip, limit=limit)
    return comments


@router.get("/comment/{id}", response_model=schemas.Comment, tags=["comment"])
def read_comment(id: int, db: Session = Depends(get_db)):
    db_comment = crud.get_comment_by_id(db, comment_id=id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@router.put("/comment/{id}", response_model=schemas.Comment, tags=["comment"])
async def update_comment(id: int, comment: schemas.CommentCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = await auth.get_current_user(token, db)
    db_comment = crud.get_comment_by_id(db, comment_id=id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.user_id != user.id:
        raise HTTPException(
            status_code=405, detail="Not allowed! you are not the owner of this comment")

    db_comment = crud.update_comment(
        db, comment_id=id, comment=comment)
    return db_comment


@router.delete("/comment/{id}", response_model=schemas.Comment, tags=["comment"])
async def delete_comment(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = await auth.get_current_user(token, db)
    db_comment = crud.get_comment_by_id(db, comment_id=id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.user_id != user.id:
        raise HTTPException(
            status_code=405, detail="Not allowed! you are not the owner of this comment")

    db_comment = crud.delete_comment(db, comment_id=id)
    return db_comment


@router.get("/blog/{blog_id}/comment/", response_model=schemas.Comment, tags=["comment"])
def read_comments(blog_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = crud.get_comments_by_blog_id(
        db, blog_id=blog_id, skip=skip, limit=limit)
    return comments


@router.post("/blog/{blog_id}/comment/", response_model=schemas.Comment, tags=["comment"])
async def create_comment(blog_id: int, comment: schemas.CommentCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = await auth.get_current_user(token, db)
    db_blog = crud.get_blog_by_id(db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    db_comment = crud.create_comment(
        db=db, blog_id=blog_id, user_id=user.id, comment=comment)
    return db_comment
