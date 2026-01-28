from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, database
from .auth import get_current_user

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
    notebooks = db.query(models.Notebook).filter(models.Notebook.owner_id == current_user.id).offset(skip).limit(limit).all()
    return notebooks

@router.get("/{notebook_id}", response_model=schemas.Notebook)
def read_notebook(notebook_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    notebook = db.query(models.Notebook).filter(models.Notebook.id == notebook_id, models.Notebook.owner_id == current_user.id).first()
    if notebook is None:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return notebook

@router.delete("/{notebook_id}")
def delete_notebook(notebook_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    notebook = db.query(models.Notebook).filter(models.Notebook.id == notebook_id, models.Notebook.owner_id == current_user.id).first()
    if notebook is None:
        raise HTTPException(status_code=404, detail="Notebook not found")
    # Clean up files? (Ideally yes, but for now just DB)
    db.delete(notebook)
    db.commit()
    return {"ok": True}
