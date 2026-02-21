import { Upload, FileText, ArrowLeft, Trash2 } from 'lucide-react';

export default function Sidebar({ files, onUpload, onDeleteFile, onSelectFile, onBack, notebookTitle, isOwner }) {
    const handleFileChange = (e) => {
        if (e.target.files[0]) {
            onUpload(e.target.files[0]);
        }
    };

    return (
        <div className="sidebar" style={{ padding: 16 }}>
            <div style={{ paddingBottom: 16, borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
                <h4 style={{ margin: 0, fontSize: 16, fontWeight: 600 }}>Sources</h4>
                {isOwner && (
                    <label className="btn btn-primary" style={{ cursor: 'pointer', padding: '6px 12px', fontSize: 14, borderRadius: 24, background: '#eef3fc', color: '#1a73e8', border: 'none', margin: 0 }}>
                        <Upload size={16} /> Add
                        <input type="file" style={{ display: 'none' }} onChange={handleFileChange} />
                    </label>
                )}
            </div>
            <div style={{ flex: 1, overflowY: 'auto' }}>
                <h4 style={{ margin: '0 0 12px 0', color: 'var(--text-secondary)', fontSize: 12, textTransform: 'uppercase' }}># of Sources: {files.length}</h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                    {files.map(f => (
                        <div
                            key={f.id}
                            className="card"
                            style={{ padding: 12, display: 'flex', alignItems: 'center', gap: 12, cursor: 'pointer', boxShadow: 'none', border: '1px solid transparent', position: 'relative' }}
                            onClick={() => onSelectFile(f)}
                            onMouseEnter={e => e.currentTarget.style.background = '#e8f0fe'}
                            onMouseLeave={e => e.currentTarget.style.background = 'white'}
                        >
                            <div style={{ width: 32, height: 32, background: '#f1f3f4', borderRadius: 4, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--primary)' }}>
                                <FileText size={18} />
                            </div>
                            <div style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', fontSize: 14 }}>
                                {f.filename}
                            </div>
                            {isOwner && (
                                <button
                                    className="delete-btn"
                                    onClick={(e) => onDeleteFile(e, f.id)}
                                    title="Delete File"
                                >
                                    <Trash2 size={14} />
                                </button>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
