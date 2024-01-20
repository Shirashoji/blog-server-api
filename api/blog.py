from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session


from api.dps import get_db
from api import auth
from common import schemas, crud

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/blog/", response_model=schemas.Blog, tags=["blog"], description="Create a new blog")
async def create_blog(
    blog: schemas.BlogCreate, db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = await auth.get_current_user(token, db)
    print("user_id: " + str(user.id))
    return crud.create_blog(db=db, blog=blog, owner_id=user.id)


@router.get("/blog/", response_model=list[schemas.BlogSummary], tags=["blog"], description="Returns a list of blog summaries.")
def read_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    blogs = crud.get_blogs(db, skip=skip, limit=limit)
    return blogs


@router.get("/blog/{id}", response_model=schemas.Blog, tags=["blog"], description="Returns a blog.")
def read_blog(id: int, db: Session = Depends(get_db)):
    db_blog = crud.get_blog_by_id(db, blog_id=id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return db_blog


@router.put("/blog/{id}", response_model=schemas.Blog, tags=["blog"], description="Updates a blog.")
async def update_blog(id: int, blog: schemas.BlogCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = await auth.get_current_user(token, db)
    db_blog = crud.get_blog_by_id(db, blog_id=id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    if db_blog.owner_id != user.id:
        raise HTTPException(
            status_code=405, detail="Not allowed! you are not the owner of this blog")

    db_blog = crud.update_blog(db, blog_id=id, blog=blog)
    return db_blog


@router.delete("/blog/{id}", response_model=schemas.Blog, tags=["blog"], description="Deletes a blog.")
async def delete_blog(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = await auth.get_current_user(token, db)
    db_blog = crud.get_blog_by_id(db, blog_id=id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    if db_blog.owner_id != user.id:
        raise HTTPException(
            status_code=405, detail="Not allowed! you are not the owner of this blog")

    db_blog = crud.delete_blog(db, blog_id=id)
    return db_blog
