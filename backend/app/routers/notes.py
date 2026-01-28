from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, database
from .auth import get_current_user

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, notebook_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # Verify notebook ownership
    notebook = db.query(models.Notebook).filter(models.Notebook.id == notebook_id, models.Notebook.owner_id == current_user.id).first()
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
        
    db_note = models.Note(
        notebook_id=notebook_id,
        content=note.content,
        type=note.type
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/{notebook_id}", response_model=List[schemas.Note])
def read_notes(notebook_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # Verify notebook ownership
    notebook = db.query(models.Notebook).filter(models.Notebook.id == notebook_id, models.Notebook.owner_id == current_user.id).first()
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    
    return db.query(models.Note).filter(models.Note.notebook_id == notebook_id).all()
