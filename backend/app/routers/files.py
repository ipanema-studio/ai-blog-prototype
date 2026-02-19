import shutil
import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from .. import schemas, models, database
from .auth import get_current_user

router = APIRouter(
    prefix="/files",
    tags=["files"],
    dependencies=[Depends(get_current_user)]
)

UPLOAD_DIR = "static/uploads"

@router.post("/{notebook_id}/upload", response_model=schemas.SourceFile)
async def upload_file(
    notebook_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # Verify notebook ownership - No, allow anyone to upload
    notebook = db.query(models.Notebook).filter(models.Notebook.id == notebook_id).first()
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")

    # Ensure notebook directory exists
    notebook_dir = os.path.join(UPLOAD_DIR, str(notebook_id))
    os.makedirs(notebook_dir, exist_ok=True)

    # Save file
    file_path = os.path.join(notebook_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create DB record
    db_file = models.SourceFile(
        notebook_id=notebook_id,
        filename=file.filename,
        file_path=file_path,
        file_type=file.content_type
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

@router.get("/{notebook_id}", response_model=List[schemas.SourceFile])
def list_files(notebook_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
     # Verify notebook exists
    notebook = db.query(models.Notebook).filter(models.Notebook.id == notebook_id).first()
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    
    return db.query(models.SourceFile).filter(models.SourceFile.notebook_id == notebook_id).all()

@router.delete("/{file_id}")
def delete_file(file_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # Create query to check file exists
    db_file = db.query(models.SourceFile).query(models.SourceFile).filter(models.SourceFile.id == file_id).first()
    
    # Actually simpler:
    db_file = db.query(models.SourceFile).filter(models.SourceFile.id == file_id).first()

    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    # Remove from disk
    if os.path.exists(db_file.file_path):
        os.remove(db_file.file_path)

    db.delete(db_file)
    db.commit()
    return {"ok": True}
