from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    notebooks = relationship("Notebook", back_populates="owner")

class Notebook(Base):
    __tablename__ = "notebooks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    thumbnail_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="notebooks")
    sources = relationship("SourceFile", back_populates="notebook")
    notes = relationship("Note", back_populates="notebook")

class SourceFile(Base):
    __tablename__ = "source_files"

    id = Column(Integer, primary_key=True, index=True)
    notebook_id = Column(Integer, ForeignKey("notebooks.id"))
    filename = Column(String)
    file_path = Column(String) # Relative path to storage
    file_type = Column(String) # pdf, txt, md, image
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    notebook = relationship("Notebook", back_populates="sources")

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    notebook_id = Column(Integer, ForeignKey("notebooks.id"))
    title = Column(String, default="Untitled Note")
    content = Column(Text, default="")
    type = Column(String, default="note") # 'overview', 'note', 'summary'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    notebook = relationship("Notebook", back_populates="notes")
