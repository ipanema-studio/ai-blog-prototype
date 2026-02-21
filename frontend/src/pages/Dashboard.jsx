import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Search, Book, Trash2, LogOut } from 'lucide-react';
import api from '../api';

export default function Dashboard() {
    const [notebooks, setNotebooks] = useState([]);
    const [search, setSearch] = useState('');
    const navigate = useNavigate();
    const [currentUser, setCurrentUser] = useState(null);

    useEffect(() => {
        fetchNotebooks();
        fetchUser();
    }, []);

    const fetchUser = async () => {
        try {
            const res = await api.get('/users/me');
            setCurrentUser(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    const fetchNotebooks = async () => {
        try {
            const res = await api.get('/notebooks/');
            setNotebooks(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    const createNotebook = async () => {
        const title = prompt('Enter Notebook Title:');
        if (!title) return;
        try {
            await api.post('/notebooks/', { title });
            fetchNotebooks();
        } catch (err) {
            alert('Failed to create notebook');
        }
    };

    const deleteNotebook = async (e, id) => {
        e.stopPropagation();
        if (!confirm('Are you sure you want to delete this notebook? This action cannot be undone.')) return;
        try {
            await api.delete(`/notebooks/${id}`);
            fetchNotebooks();
        } catch (err) {
            alert('Failed to delete notebook');
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    const filtered = notebooks.filter(n => n.title.toLowerCase().includes(search.toLowerCase()));

    return (
        <div className="dashboard-layout">
            <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 32 }}>
                <h1 style={{ fontSize: '3em' }}>AMS SW Archive</h1>
                <div style={{ display: 'flex', gap: 16, alignItems: 'center' }}>
                    {currentUser && (
                        <span style={{ marginRight: 16, fontWeight: 600 }}>
                            Hello, {currentUser.username}
                        </span>
                    )}
                    <div style={{ position: 'relative' }}>
                        <Search size={18} style={{ position: 'absolute', left: 10, top: 12, color: 'var(--text-secondary)' }} />
                        <input
                            className="input"
                            style={{ paddingLeft: 36 }}
                            placeholder="Search notebooks..."
                            value={search}
                            onChange={e => setSearch(e.target.value)}
                        />
                    </div>
                    <button className="btn btn-primary" onClick={createNotebook}>
                        <Plus size={18} />
                        New Notebook
                    </button>
                    <button className="btn" onClick={handleLogout} style={{ color: 'var(--text-secondary)' }}>
                        <LogOut size={18} />
                        Log Out
                    </button>
                </div>
            </header>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: 24 }}>
                {filtered.map(nb => (
                    <div key={nb.id} className="card" style={{ cursor: 'pointer', transition: 'transform 0.2s', position: 'relative' }} onClick={() => navigate(`/notebook/${nb.id}`)}>
                        <div style={{
                            height: 120,
                            background: nb.thumbnail_url
                                ? `url(http://localhost:8000/${nb.thumbnail_url}) center/cover no-repeat`
                                : 'linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)',
                            borderRadius: '8px 8px 0 0',
                            margin: '-16px -16px 16px -16px'
                        }}></div>
                        <h3 style={{ margin: '0 0 8px 0' }}>{nb.title}</h3>
                        <p style={{ margin: 0, color: 'var(--text-secondary)', fontSize: 12 }}>
                            Created {new Date(nb.created_at).toLocaleDateString()}
                        </p>
                        <button
                            className="delete-btn"
                            onClick={(e) => deleteNotebook(e, nb.id)}
                            title="Delete Notebook"
                        >
                            <Trash2 size={16} />
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}
