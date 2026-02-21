import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Editor from '../components/Editor';
import NotePanel from '../components/NotePanel';
import api from '../api';
import { ArrowLeft, Settings, X } from 'lucide-react';

export default function NotebookView() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [notebook, setNotebook] = useState(null);
    const [files, setFiles] = useState([]);
    const [viewMode, setViewMode] = useState('overview'); // 'overview', 'file', 'note'
    const [selectedFile, setSelectedFile] = useState(null);
    const [activeNote, setActiveNote] = useState(null);
    const [currentUser, setCurrentUser] = useState(null);

    // Settings state
    const [showSettings, setShowSettings] = useState(false);
    const fileInputRef = useRef(null);

    useEffect(() => {
        fetchData();
        fetchUser();
        // Reset view when ID changes
        setViewMode('overview');
        setActiveNote(null);
    }, [id]);

    const fetchUser = async () => {
        try {
            const res = await api.get('/users/me');
            setCurrentUser(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    const fetchData = async () => {
        try {
            const nbRes = await api.get(`/notebooks/${id}`);
            setNotebook(nbRes.data);
            const filesRes = await api.get(`/files/${id}`);
            setFiles(filesRes.data);
        } catch (err) {
            console.error(err);
            navigate('/');
        }
    };

    const handleUpload = async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        try {
            await api.post(`/files/${id}/upload`, formData);
            fetchData();
        } catch (err) {
            alert('Upload failed');
        }
    };

    const handleDeleteFile = async (e, fileId) => {
        e.stopPropagation();
        if (!confirm('Are you sure you want to delete this file?')) return;
        try {
            await api.delete(`/files/${fileId}`);
            if (selectedFile && selectedFile.id === fileId) {
                setSelectedFile(null);
                setViewMode('overview');
            }
            fetchData();
        } catch (err) {
            alert('Failed to delete file');
        }
    };

    // Handler when a note is clicked in NotePanel
    const handleNoteSelect = (note) => {
        setActiveNote(note);
        setViewMode('note');
    };

    const handleCreateNote = () => {
        setActiveNote(null); // Null means new/empty note
        setViewMode('note');
    }

    const handleUpdateTitle = async () => {
        const newTitle = prompt("Enter new title:", notebook.title);
        if (newTitle && newTitle !== notebook.title) {
            try {
                await api.put(`/notebooks/${id}`, { title: newTitle });
                fetchData();
            } catch (err) {
                alert('Failed to update title');
            }
        }
    };

    const handleThumbnailUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            await api.post(`/notebooks/${id}/thumbnail`, formData);
            fetchData();
            alert('Thumbnail updated!');
        } catch (err) {
            alert('Failed to upload thumbnail');
        }
    };

    if (!notebook) return <div>Loading...</div>;

    // Allow everyone to edit
    const isOwner = true;

    return (
        <div className="notebook-layout">
            <header className="notebook-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                    <button
                        onClick={() => navigate('/')}
                        style={{
                            background: 'none',
                            border: 'none',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            color: 'var(--text-main)',
                            padding: '8px',
                            borderRadius: '50%'
                        }}
                        onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'rgba(0,0,0,0.05)'}
                        onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
                    >
                        <ArrowLeft size={20} /> {/* We can change this icon later if needed, mimicking Google style back or home icon */}
                    </button>
                    <h1 style={{ fontSize: '1.25rem', fontWeight: 600, margin: 0, color: 'var(--text-main)' }}>
                        {notebook.title}
                    </h1>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                    {isOwner && (
                        <div style={{ position: 'relative' }}>
                            <button className="btn" onClick={() => setShowSettings(!showSettings)} title="Notebook Settings">
                                <Settings size={16} /> <span style={{ marginLeft: 4 }}>Settings</span>
                            </button>
                            {showSettings && (
                                <div className="card" style={{ position: 'absolute', top: '100%', right: 0, marginTop: 8, width: 200, zIndex: 100, padding: 8, boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
                                    <div
                                        style={{ padding: '10px 12px', cursor: 'pointer', fontSize: 14, borderRadius: 8 }}
                                        onClick={() => { setShowSettings(false); handleUpdateTitle(); }}
                                        onMouseEnter={(e) => e.currentTarget.style.background = '#f0f4f9'}
                                        onMouseLeave={(e) => e.currentTarget.style.background = 'white'}
                                    >
                                        Rename Notebook
                                    </div>
                                    <div
                                        style={{ padding: '10px 12px', cursor: 'pointer', fontSize: 14, borderRadius: 8 }}
                                        onClick={() => { setShowSettings(false); fileInputRef.current.click(); }}
                                        onMouseEnter={(e) => e.currentTarget.style.background = '#f0f4f9'}
                                        onMouseLeave={(e) => e.currentTarget.style.background = 'white'}
                                    >
                                        Change Thumbnail
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                    <input
                        type="file"
                        ref={fileInputRef}
                        style={{ display: 'none' }}
                        accept="image/*"
                        onChange={handleThumbnailUpload}
                    />
                </div>
            </header>

            <div className="notebook-content">
                {/* Left Column: Sources */}
                <Sidebar
                    files={files}
                    onUpload={handleUpload}
                    onDeleteFile={handleDeleteFile}
                    onSelectFile={(f) => { setSelectedFile(f); setViewMode('file'); }}
                    isOwner={isOwner}
                />

                {/* Center Column: Content */}
                <div className="main-content" style={{ padding: 16 }}>
                    {viewMode === 'file' ? (
                        <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                            <header style={{ paddingBottom: 16, borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
                                <h4 style={{ margin: 0, fontSize: 16, fontWeight: 600 }}>{selectedFile?.filename}</h4>
                                <button className="btn" style={{ padding: '6px', fontSize: 14, borderRadius: 24, border: 'none' }} onClick={() => { setViewMode('overview'); setActiveNote(null); }}>
                                    <X size={20} />
                                </button>
                            </header>
                            <div style={{ flex: 1, overflowY: 'auto' }}>
                                <div style={{ background: '#f8f9fa', minHeight: '100%', borderRadius: 12, padding: 24, display: 'flex', flexDirection: 'column', boxSizing: 'border-box' }}>
                                    <h3 style={{ marginTop: 0 }}>File Preview: {selectedFile?.filename}</h3>
                                    <p style={{ color: 'var(--text-secondary)' }}>File type: {selectedFile?.file_type}</p>
                                    <a href={`http://localhost:8000/${selectedFile?.file_path}`} target="_blank" rel="noreferrer" style={{ color: 'var(--primary)', textDecoration: 'none', fontWeight: 500, display: 'inline-block', marginBottom: 16 }}>
                                        Download / Open Original
                                    </a>
                                    <iframe src={`http://localhost:8000/${selectedFile?.file_path}`} style={{ width: '100%', flex: 1, border: '1px solid var(--border)', borderRadius: 8, background: '#fff' }}></iframe>
                                </div>
                            </div>
                        </div>
                    ) : viewMode === 'overview' ? (
                        <Editor notebookId={id} type="overview" readOnly={!isOwner} />
                    ) : (
                        <Editor notebookId={id} type="note" initialNote={activeNote} onClose={() => { setViewMode('overview'); setActiveNote(null); }} onSave={() => { /* triggers refresh in right panel? */ }} readOnly={!isOwner} />
                    )}
                </div>

                {/* Right Column: Notes */}
                <NotePanel notebookId={id} onSelectNote={handleNoteSelect} onCreateNote={handleCreateNote} isOwner={isOwner} />
            </div>
        </div>
    );
}
