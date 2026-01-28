import { useState, useEffect } from 'react';
import { Plus, MessageSquare } from 'lucide-react';
import api from '../api';

export default function NotePanel({ notebookId }) {
    const [notes, setNotes] = useState([]);
    const [newNote, setNewNote] = useState('');

    useEffect(() => {
        fetchNotes();
    }, [notebookId]);

    const fetchNotes = async () => {
        try {
            const res = await api.get(`/notes/${notebookId}`);
            // Filter out 'overview' type
            setNotes(res.data.filter(n => n.type !== 'overview'));
        } catch (err) {
            console.error(err);
        }
    };

    const addNote = async () => {
        if (!newNote.trim()) return;
        try {
            await api.post(`/notes/`, { content: newNote, type: 'note' }, { params: { notebook_id: notebookId } });
            setNewNote('');
            fetchNotes();
        } catch (err) {
            alert('Failed to add note');
        }
    };

    return (
        <div className="right-panel">
            <div style={{ padding: 16, borderBottom: '1px solid var(--border)' }}>
                <h4 style={{ margin: 0 }}>Saved Responses & Notes</h4>
            </div>

            <div style={{ flex: 1, overflowY: 'auto', padding: 16, display: 'flex', flexDirection: 'column', gap: 16 }}>
                {notes.map(note => (
                    <div key={note.id} className="card" style={{ padding: 12 }}>
                        <div style={{ display: 'flex', gap: 8, marginBottom: 8, alignItems: 'center', color: 'var(--primary)' }}>
                            <MessageSquare size={14} />
                            <span style={{ fontSize: 12, fontWeight: 600 }}>{note.type.toUpperCase()}</span>
                        </div>
                        <div style={{ fontSize: 14, whiteSpace: 'pre-wrap' }}>{note.content}</div>
                    </div>
                ))}
                {notes.length === 0 && (
                    <div style={{ textAlign: 'center', color: 'var(--text-secondary)', fontSize: 14, marginTop: 20 }}>
                        No notes yet. Add one below!
                    </div>
                )}
            </div>

            <div style={{ padding: 16, borderTop: '1px solid var(--border)', background: 'white' }}>
                <textarea
                    className="input"
                    style={{ width: '100%', boxSizing: 'border-box', minHeight: 80, resize: 'vertical', fontFamily: 'inherit' }}
                    placeholder="Add a note or key takeaway..."
                    value={newNote}
                    onChange={e => setNewNote(e.target.value)}
                    onKeyDown={e => { if (e.ctrlKey && e.key === 'Enter') addNote(); }}
                />
                <button className="btn btn-primary" style={{ marginTop: 8, width: '100%', justifyContent: 'center' }} onClick={addNote}>
                    <Plus size={16} />
                    Add Note
                </button>
            </div>
        </div>
    );
}
