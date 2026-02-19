from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from .. import schemas, models, database
from .auth import get_current_user
import shutil
import os

router = APIRouter(
    prefix="/notebooks",
    tags=["notebooks"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas.Notebook)
def create_notebook(notebook: schemas.NotebookCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_notebook = models.Notebook(title=notebook.title, owner_id=current_user.id)
    db.add(db_notebook)
    db.commit()
    db.refresh(db_notebook)
    return db_notebook

@router.get("/", response_model=List[schemas.Notebook])
def read_notebooks(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # Allow viewing all notebooks
    notebooks = db.query(models.Notebook).offset(skip).limit(limit).all()
    return notebooks

@router.get("/{notebook_id}", response_model=schemas.Notebook)
def read_notebook(notebook_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # Allow viewing any notebook
    notebook = db.query(models.Notebook).filter(models.Notebook.id == notebook_id).first()
    if notebook is None:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return notebook

@router.put("/{notebook_id}", response_model=schemas.Notebook)
def update_notebook(notebook_id: int, notebook_update: schemas.NotebookUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_notebook = db.query(models.Notebook).filter(models.Notebook.id == notebook_id).first()
    if not db_notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    
    db_notebook.title = notebook_update.title
    db.commit()
    db.refresh(db_notebook)
    return db_notebook

@router.post("/{notebook_id}/thumbnail", response_model=schemas.Notebook)
def upload_thumbnail(notebook_id: int, file: UploadFile = File(...), db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    print(f"DEBUG: upload_thumbnail called for notebook_id={notebook_id}")
    print(f"DEBUG: filename={file.filename}")
    
    db_notebook = db.query(models.Notebook).filter(models.Notebook.id == notebook_id).first()
    if not db_notebook:
        print("DEBUG: Notebook not found")
        raise HTTPException(status_code=404, detail="Notebook not found")
    
    upload_dir = f"static/uploads/{notebook_id}"
    os.makedirs(upload_dir, exist_ok=True)
    
    file_extension = os.path.splitext(file.filename)[1]
    file_path = f"{upload_dir}/thumbnail{file_extension}"
    print(f"DEBUG: Saving to {file_path}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    db_notebook.thumbnail_url = file_path
    db.commit()
    db.refresh(db_notebook)
    return db_notebook

@router.delete("/{notebook_id}")
def delete_notebook(notebook_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    notebook = db.query(models.Notebook).filter(models.Notebook.id == notebook_id).first()
    if notebook is None:
        raise HTTPException(status_code=404, detail="Notebook not found")
    
    # Clean up files
    import shutil
    import os
    notebook_dir = f"static/uploads/{notebook_id}"
    if os.path.exists(notebook_dir):
        shutil.rmtree(notebook_dir)

    db.delete(notebook)
    db.commit()
    return {"ok": True}
