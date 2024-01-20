from datetime import datetime
from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    pass


class CommentCreate(CommentBase):
    content: str = Field(..., example="とても素晴らしいブログでした．面白かったです！！")


class Comment(CommentBase):
    id: int = Field(..., example=1)
    content: str = Field(..., example="とても素晴らしいブログでした．面白かったです！！")
    blog_id: int = Field(..., example=1)
    user_id: int = Field(..., example=1)
    created_at: datetime = Field(..., example="2021-01-01T00:00:00.000000")
    updated_at: datetime = Field(..., example="2021-01-01T00:00:00.000000")

    class Config:
        orm_mode = True


class CommentSummary(CommentBase):
    id: int = Field(..., example=1)
    user_id: int = Field(..., example=1)
    content: str = Field(..., example="とても素晴らしいブログでした．面白かったです！！")
    updated_at: datetime = Field(..., example="2021-01-01T00:00:00.000000")

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    name: str = Field(..., example="Python")


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int = Field(..., example=1)

    class Config:
        orm_mode = True


class BlogCategoryBase(BaseModel):
    pass


class BlogCategory(BlogCategoryBase):
    blog_id: int = Field(..., example=1)
    category_id: int = Field(..., example=1)

    class Config:
        orm_mode = True


class BlogBase(BaseModel):
    title: str = Field(..., example="Pythonの基礎")
    description: str = Field(..., example="Pythonの基礎を説明しています！")


class BlogCreate(BlogBase):
    content: str = Field(
        ..., example="#Pythonってなに？  Pythonとは，テレビ番組の「モンティ・パイソン」に由来するプログラミング言語です．開発者は，Guido van Rossum氏です．")
    pass


class Blog(BlogBase):
    id: int = Field(..., example=1)
    owner_id: int = Field(..., example=1)
    content: str = Field(
        ..., example="#Pythonってなに？  Pythonとは，テレビ番組の「モンティ・パイソン」に由来するプログラミング言語です．開発者は，Guido van Rossum氏です．")
    created_at: datetime = Field(..., example="2021-01-01T00:00:00.000000")
    updated_at: datetime = Field(..., example="2021-01-01T00:00:00.000000")
    comments: list[CommentSummary] = []

    class Config:
        orm_mode = True


class BlogSummary(BlogBase):
    id: int
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    username: str
    joined_at: datetime | None = None
    blogs: list[BlogSummary] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
