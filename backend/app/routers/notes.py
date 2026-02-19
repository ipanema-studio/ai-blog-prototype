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
    # Verify notebook exists
    notebook = db.query(models.Notebook).filter(models.Notebook.id == notebook_id).first()
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
        
    db_note = models.Note(
        notebook_id=notebook_id,
        title=note.title,
        content=note.content,
        type=note.type
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.put("/{note_id}", response_model=schemas.Note)
def update_note(note_id: int, note: schemas.NoteCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()

    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db_note.title = note.title
    db_note.content = note.content
    # db_note.type = note.type # Usually type doesn't change, but could if needed
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/{notebook_id}", response_model=List[schemas.Note])
def read_notes(notebook_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # Verify notebook exists
    notebook = db.query(models.Notebook).filter(models.Notebook.id == notebook_id).first()
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    
    return db.query(models.Note).filter(models.Note.notebook_id == notebook_id).all()

@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()

    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(db_note)
    db.commit()
    return {"ok": True}
