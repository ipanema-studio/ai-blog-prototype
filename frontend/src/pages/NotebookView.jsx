import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Editor from '../components/Editor';
import NotePanel from '../components/NotePanel';
import api from '../api';

export default function NotebookView() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [notebook, setNotebook] = useState(null);
    const [files, setFiles] = useState([]);
    const [viewMode, setViewMode] = useState('overview'); // 'overview' or 'file'
    const [selectedFile, setSelectedFile] = useState(null);

    useEffect(() => {
        fetchData();
    }, [id]);

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

    if (!notebook) return <div>Loading...</div>;

    return (
        <div className="notebook-layout">
            {/* Left Column: Sources */}
            <Sidebar
                files={files}
                onUpload={handleUpload}
                onSelectFile={(f) => { setSelectedFile(f); setViewMode('file'); }}
                onBack={() => navigate('/')}
                notebookTitle={notebook.title}
            />

            {/* Center Column: Content */}
            <div className="main-content">
                <header style={{ padding: '16px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <h2 style={{ fontSize: 18, margin: 0 }}>
                        {viewMode === 'overview' ? 'Notebook Overview' : selectedFile?.filename}
                    </h2>
                    {viewMode === 'file' && (
                        <button className="btn" onClick={() => setViewMode('overview')}>Back to Overview</button>
                    )}
                </header>
                <div style={{ flex: 1, overflowY: 'auto', padding: 24 }}>
                    {viewMode === 'overview' ? (
                        <Editor notebookId={id} />
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
            </div>

            {/* Right Column: Notes */}
            <NotePanel notebookId={id} />
        </div>
    );
}
