import { useState, useEffect, useRef } from 'react';
import Quill from 'quill';
import 'quill/dist/quill.snow.css';
import BlotFormatter from 'quill-blot-formatter';
import api from '../api';
import { ArrowLeft, Settings, X } from 'lucide-react';

Quill.register('modules/blotFormatter', BlotFormatter);

export default function Editor({ notebookId, type = 'overview', initialNote = null, onSave, onClose, readOnly = false }) {
    // If type is overview, we fetch it. If type is note, we use initialNote or blank.
    const [noteId, setNoteId] = useState(null);
    const [title, setTitle] = useState('');
    const [saving, setSaving] = useState(false);

    // Local edit state for "Safe Mode"
    const [isEditing, setIsEditing] = useState(false);

    const editorRef = useRef(null);
    const quillInstance = useRef(null);

    useEffect(() => {
        if (editorRef.current && !quillInstance.current) {
            quillInstance.current = new Quill(editorRef.current, {
                theme: 'snow',
                readOnly: true, // Start read-only
                modules: {
                    blotFormatter: {},
                    toolbar: !readOnly ? [
                        [{ 'header': [1, 2, false] }],
                        ['bold', 'italic', 'underline', 'strike', 'blockquote'],
                        [{ 'list': 'ordered' }, { 'list': 'bullet' }, { 'indent': '-1' }, { 'indent': '+1' }],
                        ['link', 'image'],
                        ['clean']
                    ] : false
                }
            });

            // Initial toolbar hide
            const toolbarContainer = editorRef.current.parentElement.querySelector('.ql-toolbar');
            if (toolbarContainer) toolbarContainer.style.display = 'none';
        }
    }, [type]);

    useEffect(() => {
        if (quillInstance.current) {
            const shouldBeEditable = !readOnly && isEditing;
            quillInstance.current.enable(shouldBeEditable);

            // Toggle toolbar visibility
            const toolbarContainer = editorRef.current.parentElement.querySelector('.ql-toolbar');
            if (toolbarContainer) {
                toolbarContainer.style.display = shouldBeEditable ? 'block' : 'none';
            }
        }
    }, [readOnly, isEditing]);

    useEffect(() => {
        loadContent();
    }, [notebookId, type, initialNote]);

    const loadContent = async () => {
        if (!quillInstance.current) return;

        if (type === 'overview') {
            setTitle('Notebook Overview');
            // Fetch Overview Logic
            try {
                const res = await api.get(`/notes/${notebookId}`);
                const overviews = res.data.filter(n => n.type === 'overview');
                const overview = overviews.sort((a, b) => b.id - a.id)[0];

                if (overview) {
                    setNoteId(overview.id);
                    quillInstance.current.clipboard.dangerouslyPasteHTML(overview.content);
                } else {
                    setNoteId(null);
                    quillInstance.current.setText('');
                }
            } catch (err) {
                console.error(err);
            }
        } else {
            // Note Mode
            if (initialNote) {
                setNoteId(initialNote.id);
                setTitle(initialNote.title || '');
                quillInstance.current.clipboard.dangerouslyPasteHTML(initialNote.content);
            } else {
                setNoteId(null);
                setTitle('');
                quillInstance.current.setText('');
            }
        }
    };

    const handleSave = async () => {
        if (!quillInstance.current) return;
        if (type !== 'overview' && !title.trim()) {
            alert("Please enter a title");
            return;
        }

        setSaving(true);
        const content = quillInstance.current.root.innerHTML;

        try {
            if (noteId) {
                await api.put(`/notes/${noteId}`, { title: type === 'overview' ? 'Notebook Overview' : title, content, type });
            } else {
                const res = await api.post(`/notes/`, { title: type === 'overview' ? 'Notebook Overview' : title, content, type }, { params: { notebook_id: notebookId } });
                setNoteId(res.data.id);
            }
            if (onSave) onSave();
        } catch (err) {
            console.error(err);
            alert('Failed to save');
        } finally {
            setSaving(false);
        }
    };

    return (
        <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <div style={{ paddingBottom: type === 'overview' ? 16 : 16, borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: type === 'overview' ? 16 : 16 }}>
                {type === 'note' ? (
                    <input
                        className="input"
                        style={{ flex: 1, fontWeight: 600, boxSizing: 'border-box', marginRight: 16 }}
                        placeholder="Note Title"
                        value={title}
                        onChange={e => setTitle(e.target.value)}
                        disabled={!isEditing || readOnly}
                    />
                ) : (
                    <h4 style={{ margin: 0, fontSize: 16, fontWeight: 600 }}>Overview</h4>
                )}

                <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                    {!readOnly && (
                        <div style={{ display: 'flex', gap: 8 }}>
                            {isEditing && (
                                <button className="btn btn-primary" style={{ padding: '6px 12px', fontSize: 13, borderRadius: 24, background: '#1a73e8', color: '#fff', border: 'none' }} onClick={handleSave} disabled={saving}>
                                    {saving ? 'Saving...' : 'Save'}
                                </button>
                            )}
                            <button
                                className="btn"
                                onClick={() => setIsEditing(!isEditing)}
                                style={{
                                    padding: '6px 12px',
                                    fontSize: 13,
                                    borderRadius: 24,
                                    background: isEditing ? '#f1f3f4' : '#fff',
                                    border: '1px solid var(--border)',
                                    color: 'var(--text-main)',
                                    cursor: 'pointer'
                                }}
                            >
                                {isEditing ? 'Cancel' : 'Edit'}
                            </button>
                        </div>
                    )}
                    {
                        onClose && (
                            <button className="btn" style={{ padding: '6px', fontSize: 14, borderRadius: 24, border: 'none' }} onClick={onClose}>
                                <X size={20} />
                            </button>
                        )
                    }
                </div>
            </div>

            <div
                style={{
                    overflowY: 'auto',
                    flex: 1,
                    display: 'flex',
                    flexDirection: 'column',
                    // Apply conditional class to hide borders if not editing
                }}
                className={!isEditing && readOnly ? "hide-editor-border" : (isEditing ? "" : "hide-editor-border")}
            >
                {/* We rely on CSS/JS to hide toolbar in useEffect */}
                <div ref={editorRef} style={{ flex: 1, border: (!isEditing && type === 'overview') ? 'none' : undefined }}></div>
            </div>
        </div>
    );
}
