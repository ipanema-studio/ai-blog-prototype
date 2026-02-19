import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Editor from '../components/Editor';
import NotePanel from '../components/NotePanel';
import api from '../api';
import { Settings } from 'lucide-react';

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
            {/* Left Column: Sources */}
            <Sidebar
                files={files}
                onUpload={handleUpload}
                onDeleteFile={handleDeleteFile}
                onSelectFile={(f) => { setSelectedFile(f); setViewMode('file'); }}
                onBack={() => navigate('/')}
                notebookTitle={notebook.title}
                isOwner={isOwner}
            />

            {/* Center Column: Content */}
            <div className="main-content">
                <header style={{ padding: '16px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                        <h2 style={{ fontSize: 18, margin: 0 }}>
                            {viewMode === 'overview' ? 'Notebook Overview' :
                                viewMode === 'file' ? selectedFile?.filename :
                                    activeNote ? activeNote.title : 'New Note'}
                        </h2>
                        {viewMode === 'overview' && isOwner && (
                            <div style={{ position: 'relative' }}>
                                <button className="btn" onClick={() => setShowSettings(!showSettings)} title="Notebook Settings">
                                    <Settings size={16} />
                                </button>
                                {showSettings && (
                                    <div className="card" style={{ position: 'absolute', top: '100%', left: 0, marginTop: 8, width: 200, zIndex: 100, padding: 8 }}>
                                        <div
                                            style={{ padding: '8px', cursor: 'pointer', fontSize: 14 }}
                                            onClick={() => { setShowSettings(false); handleUpdateTitle(); }}
                                            onMouseEnter={(e) => e.currentTarget.style.background = '#f1f3f4'}
                                            onMouseLeave={(e) => e.currentTarget.style.background = 'white'}
                                        >
                                            Rename Notebook
                                        </div>
                                        <div
                                            style={{ padding: '8px', cursor: 'pointer', fontSize: 14 }}
                                            onClick={() => { setShowSettings(false); fileInputRef.current.click(); }}
                                            onMouseEnter={(e) => e.currentTarget.style.background = '#f1f3f4'}
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
                    {viewMode !== 'overview' && (
                        <button className="btn" onClick={() => { setViewMode('overview'); setActiveNote(null); }}>Back to Overview</button>
                    )}
                </header>
                <div style={{ flex: 1, overflowY: 'auto', padding: 24 }}>
                    {viewMode === 'overview' ? (
                        <Editor notebookId={id} type="overview" readOnly={!isOwner} />
                    ) : viewMode === 'note' ? (
                        <Editor notebookId={id} type="note" initialNote={activeNote} onSave={() => { /* triggers refresh in right panel? */ }} readOnly={!isOwner} />
                    ) : (
                        <div style={{ background: '#f1f3f4', height: '100%', borderRadius: 8, padding: 20 }}>
                            {/* Simple file viewer placeholder */}
                            <h3>File Preview: {selectedFile?.filename}</h3>
                            <p>File type: {selectedFile?.file_type}</p>
                            <a href={`http://localhost:8000/${selectedFile?.file_path}`} target="_blank" rel="noreferrer">Download / Open Original</a>
                            <iframe src={`http://localhost:8000/${selectedFile?.file_path}`} style={{ width: '100%', height: '80%', border: 'none', marginTop: 10 }}></iframe>
                        </div>
                    )}
                </div>
            </div >

            {/* Right Column: Notes */}
            < NotePanel notebookId={id} onSelectNote={handleNoteSelect} onCreateNote={handleCreateNote} isOwner={isOwner} />
        </div >
    );
}
