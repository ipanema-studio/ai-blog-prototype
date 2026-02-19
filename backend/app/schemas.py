from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# User
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

# Note
class NoteBase(BaseModel):
    title: str = "Untitled Note"
    content: str
    type: str = "note"

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    notebook_id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

# Source File
class SourceFileBase(BaseModel):
    filename: str
    file_type: str

class SourceFile(SourceFileBase):
    id: int
    notebook_id: int
    file_path: str
    uploaded_at: datetime
    class Config:
        from_attributes = True

# Notebook
class NotebookBase(BaseModel):
    title: str

class NotebookCreate(NotebookBase):
    pass

class NotebookUpdate(NotebookBase):
    pass

class Notebook(NotebookBase):
    id: int
    owner_id: int
    thumbnail_url: Optional[str] = None
    created_at: datetime
    sources: List[SourceFile] = []
    notes: List[Note] = []
    class Config:
        from_attributes = True
