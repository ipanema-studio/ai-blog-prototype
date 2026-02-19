import { useState, useEffect, useRef } from 'react';
import Quill from 'quill';
import 'quill/dist/quill.snow.css';
import BlotFormatter from 'quill-blot-formatter';
import api from '../api';

Quill.register('modules/blotFormatter', BlotFormatter);

export default function Editor({ notebookId, type = 'overview', initialNote = null, onSave, readOnly = false }) {
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
            <div style={{ marginBottom: 16, display: 'flex', gap: 16, alignItems: 'center' }}>
                {type === 'note' && (
                    <input
                        className="input"
                        style={{ flex: 1, fontWeight: 600 }}
                        placeholder="Note Title"
                        value={title}
                        onChange={e => setTitle(e.target.value)}
                        disabled={!isEditing || readOnly}
                    />
                )}
                {!readOnly && (
                    <div style={{ flex: type === 'overview' ? 1 : 0, display: 'flex', justifyContent: 'flex-end', gap: 8 }}>
                        <button
                            className="btn"
                            onClick={() => setIsEditing(!isEditing)}
                            style={{
                                background: isEditing ? '#f1f3f4' : 'transparent',
                                border: '1px solid var(--border)'
                            }}
                        >
                            {isEditing ? 'Done Editing' : 'Edit'}
                        </button>

                        {isEditing && (
                            <button className="btn btn-primary" onClick={handleSave} disabled={saving}>
                                {saving ? 'Saving...' : 'Save'}
                            </button>
                        )}
                    </div>
                )}
            </div>
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                {/* We rely on CSS/JS to hide toolbar in useEffect */}
                <div ref={editorRef} style={{ flex: 1 }}></div>
            </div>
        </div>
    );
}
