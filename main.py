from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from api import auth, user, blog, comment, category

from common.database import engine
from common import models

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Please see `/docs` for usage."}


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(blog.router)
app.include_router(comment.router)
app.include_router(category.router)
