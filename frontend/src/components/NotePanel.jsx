import { useState, useEffect } from 'react';
import { Plus, MessageSquare, Trash2 } from 'lucide-react';
import api from '../api';

export default function NotePanel({ notebookId, onSelectNote, onCreateNote, isOwner }) {
    const [notes, setNotes] = useState([]);

    // Poll for updates every few seconds to keep list fresh? Or just re-fetch on mount?
    // For now simple effect.
    useEffect(() => {
        fetchNotes();
        // Set up an interval or expose a refresh method? 
        // Let's just poll for simplicity since we don't have global state management (Redux/Context) set up for this yet.
        const interval = setInterval(fetchNotes, 2000);
        return () => clearInterval(interval);
    }, [notebookId]);

    const fetchNotes = async () => {
        try {
            const res = await api.get(`/notes/${notebookId}`);
            setNotes(res.data.filter(n => n.type !== 'overview'));
        } catch (err) {
            console.error(err);
        }
    };

    const deleteNote = async (e, id) => {
        e.stopPropagation();
        if (!confirm('Are you sure you want to delete this note?')) return;
        try {
            await api.delete(`/notes/${id}`);
            fetchNotes(); // Immediate refresh
        } catch (err) {
            alert('Failed to delete note');
        }
    };

    return (
        <div className="right-panel">
            <div style={{ padding: 16, borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h4 style={{ margin: 0 }}>Saved Notes</h4>
                {isOwner && (
                    <button className="btn btn-primary" style={{ padding: '4px 12px', fontSize: 12 }} onClick={onCreateNote}>
                        <Plus size={14} /> New
                    </button>
                )}
            </div>

            <div style={{ flex: 1, overflowY: 'auto', padding: 16, display: 'flex', flexDirection: 'column', gap: 12 }}>
                {notes.map(note => (
                    <div
                        key={note.id}
                        className="card"
                        style={{ padding: 12, cursor: 'pointer', transition: 'background 0.2s', position: 'relative' }}
                        onClick={() => onSelectNote(note)}
                        onMouseEnter={e => e.currentTarget.style.background = '#f1f3f4'}
                        onMouseLeave={e => e.currentTarget.style.background = 'white'}
                    >
                        <div style={{ display: 'flex', gap: 8, marginBottom: 4, alignItems: 'center', color: 'var(--primary)' }}>
                            <MessageSquare size={14} />
                            <span style={{ fontSize: 12, fontWeight: 600 }}>{note.type.toUpperCase()}</span>
                        </div>
                        <div style={{ fontWeight: 600, fontSize: 14, marginBottom: 4 }}>
                            {note.title || "Untitled Note"}
                        </div>
                        <div style={{ fontSize: 12, color: 'var(--text-secondary)', overflow: 'hidden', whiteSpace: 'nowrap', textOverflow: 'ellipsis' }}>
                            {/* Strip HTML tags for preview roughly */}
                            {note.content.replace(/<[^>]*>?/gm, '')}
                        </div>

                        {isOwner && (
                            <button
                                className="delete-btn"
                                onClick={(e) => deleteNote(e, note.id)}
                                title="Delete Note"
                            >
                                <Trash2 size={14} />
                            </button>
                        )}
                    </div>
                ))}
                {notes.length === 0 && (
                    <div style={{ textAlign: 'center', color: 'var(--text-secondary)', fontSize: 14, marginTop: 20 }}>
                        No notes yet. Click New to add one.
                    </div>
                )}
            </div>
        </div>
    );
}
