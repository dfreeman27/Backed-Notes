

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas.notes import NoteCreate, NoteResponse
from app.models.notes import Note
from app.database import get_db

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    """
    Creates a new note in the database.
    """
    db_note = Note(**note.model_dump())
    
    db.add(db_note)

    db.commit()
    
    db.refresh(db_note)
    
    return db_note



@router.get("/", response_model=list[NoteResponse])
def list_notes(
    category: Optional[str] = None,
    is_pinned: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """
    Returns notes, optionally filtered by category and/or pinned status.
    """
    query = db.query(Note)
    if category is not None:
        query = query.filter(Note.category == category)
    if is_pinned is not None:
        query = query.filter(Note.is_pinned == is_pinned)
    return query.all()


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    """
    Returns a single note by ID.
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Task not found")
    return note


@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """
    Deletes a note by ID.
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}