import { useState, useEffect, useRef } from 'react';
import Quill from 'quill';
import 'quill/dist/quill.snow.css';
import api from '../api';

export default function Editor({ notebookId }) {
    const [noteId, setNoteId] = useState(null);
    const [saving, setSaving] = useState(false);

    const editorRef = useRef(null);
    const quillInstance = useRef(null);

    useEffect(() => {
        if (editorRef.current && !quillInstance.current) {
            quillInstance.current = new Quill(editorRef.current, {
                theme: 'snow',
                modules: {
                    toolbar: [
                        [{ 'header': [1, 2, false] }],
                        ['bold', 'italic', 'underline', 'strike', 'blockquote'],
                        [{ 'list': 'ordered' }, { 'list': 'bullet' }, { 'indent': '-1' }, { 'indent': '+1' }],
                        ['link', 'image'],
                        ['clean']
                    ]
                }
            });
        }
    }, []);

    useEffect(() => {
        fetchOverview();
    }, [notebookId]);

    const fetchOverview = async () => {
        try {
            const res = await api.get(`/notes/${notebookId}`);
            const overview = res.data.find(n => n.type === 'overview');
            if (overview) {
                setNoteId(overview.id);
                if (quillInstance.current) {
                    // Check if content is different to avoid cursor jump? 
                    // For simple implementation, just set it.
                    // Quill's dangerous pasteHTML is deprecated in v2? No, `clipboard.dangerouslyPasteHTML` or `root.innerHTML`.
                    // Let's use clipboard.
                    quillInstance.current.clipboard.dangerouslyPasteHTML(overview.content);
                }
            } else {
                setNoteId(null);
                if (quillInstance.current) {
                    quillInstance.current.setText('');
                }
            }
        } catch (err) {
            console.error(err);
        }
    };

    const handleSave = async () => {
        if (!quillInstance.current) return;
        setSaving(true);
        const content = quillInstance.current.root.innerHTML;

        try {
            // Re-using the same logic: create if not exists
            // If we had an "update" endpoint this would be cleaner.
            // For now, always append a new "overview" note. 
            // Ideally backend should return the LATEST overview.
            // (The backend implementation was simplistic, it just GETs all notes).

            // Let's just Post.
            await api.post(`/notes/`, { content, type: 'overview' }, { params: { notebook_id: notebookId } });

            // Update local state if needed (not strictly needed since we just saved what we have)
            fetchOverview();
        } catch (err) {
            console.error(err);
        } finally {
            setSaving(false);
        }
    };

    return (
        <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <div style={{ marginBottom: 10, display: 'flex', justifyContent: 'flex-end' }}>
                <button className="btn btn-primary" onClick={handleSave} disabled={saving}>
                    {saving ? 'Saving...' : 'Save Overview'}
                </button>
            </div>
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                <div ref={editorRef} style={{ flex: 1 }}></div>
            </div>
        </div>
    );
}
