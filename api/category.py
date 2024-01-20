from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session


from api.dps import get_db
from api import auth
from common import schemas, crud

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/category/", response_model=list[schemas.Category], tags=["category"], description="Returns a list of categories.")
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories


@router.get("/category/{id}", response_model=schemas.Category, tags=["category"], description="Returns a category.")
def read_category(id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_id(db, category_id=id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.get("/blog/{blog_id}/category/", response_model=list[schemas.Category], tags=["category"], description="Returns a list of blog categories.")
def read_category(blog_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_categories_by_blog_id(db, blog_id=blog_id)
    if db_category is None:
        raise HTTPException(
            status_code=204, detail="Category not defined for this blog")
    print(db_category)
    return db_category


@router.post("/blog/{blog_id}/category", response_model=schemas.BlogCategory, tags=["category"])
async def create_category_for_blog(
    blog_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = await auth.get_current_user(token, db)
    db_blog = crud.get_blog_by_id(db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    if db_blog.owner_id != user.id:
        raise HTTPException(
            status_code=405, detail="Not allowed! you are not the owner of this blog")
    db_category = crud.get_category_by_name(db, name=category.name)
    if db_category is None:
        db_category = crud.create_category(
            db=db, category=category)
    if crud.check_blog_category(db, blog_id, category_id=db_category.id):
        raise HTTPException(
            status_code=405, detail="This category already defined for this blog")
    return crud.add_blog_category(db=db, blog_id=blog_id, category_id=db_category.id)


@router.delete("/blog/{blog_id}/category/{category_id}", response_model=schemas.BlogCategory, tags=["category"])
async def delete_category_for_blog(
    blog_id: int, category_id: int, db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = await auth.get_current_user(token, db)
    db_blog = crud.get_blog_by_id(db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    if db_blog.owner_id != user.id:
        raise HTTPException(
            status_code=405, detail="Not allowed! you are not the owner of this blog")
    if not crud.check_blog_category(db, blog_id, category_id):
        raise HTTPException(
            status_code=405, detail="This category not found for this blog")
    return crud.delete_blog_category(db=db, blog_id=blog_id, category_id=category_id)
