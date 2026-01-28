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
    # Verify notebook ownership
    notebook = db.query(models.Notebook).filter(models.Notebook.id == notebook_id, models.Notebook.owner_id == current_user.id).first()
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
     # Verify notebook ownership
    notebook = db.query(models.Notebook).filter(models.Notebook.id == notebook_id, models.Notebook.owner_id == current_user.id).first()
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    
    return db.query(models.SourceFile).filter(models.SourceFile.notebook_id == notebook_id).all()
