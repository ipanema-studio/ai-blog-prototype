import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

export default function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isRegister, setIsRegister] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (isRegister) {
                await api.post('/register', { username, password });
                alert('Registration successful! Please login.');
                setIsRegister(false);
            } else {
                const formData = new FormData();
                formData.append('username', username);
                formData.append('password', password);
                const res = await api.post('/token', formData);
                localStorage.setItem('token', res.data.access_token);
                navigate('/');
            }
        } catch (err) {
            alert('Error: ' + (err.response?.data?.detail || err.message));
        }
    };

    return (
        <div style={{
            display: 'flex',
            minHeight: '100vh',
            backgroundImage: 'url(/login_bg.jpg)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            fontFamily: '"Inter", "Roboto", sans-serif'
        }}>
            {/* Left Side: Title */}
            <div style={{
                flex: 1,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
            }}>
                <h1 style={{
                    color: '#fff',
                    fontSize: '3rem',
                    fontWeight: 'bold',
                    // textShadow: '0 4px 6px rgba(0,0,0,0.5)',
                    letterSpacing: '1px'
                }}>
                    AMS SW Archive
                </h1>
            </div>

            {/* Right Side: Login Panel */}
            <div style={{
                flex: 1,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
            }}>
                <div className="card" style={{
                    width: '100%',
                    maxWidth: '400px',
                    padding: '40px',
                    borderRadius: '8px',
                    boxShadow: '0 12px 24px rgba(0,0,0,0.2)',
                    backgroundColor: '#fff'
                }}>
                    <h2 style={{ fontSize: '1.75rem', fontWeight: 'bold', marginBottom: '40px', color: '#111' }}>
                        {isRegister ? 'Register' : 'Sign In'}
                    </h2>

                    {/* <p style={{ color: '#666', fontSize: '0.9rem', marginBottom: '24px' }}>
                        {isRegister ? 'Already have an account?' : 'New user?'} {' '}
                        <span
                            style={{ color: '#0057ff', cursor: 'pointer', textDecoration: 'underline' }}
                            onClick={() => setIsRegister(!isRegister)}
                        >
                            {isRegister ? 'Sign in' : 'Create an account'}
                        </span>
                    </p> */}

                    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                            <label style={{ fontSize: '0.85rem', color: '#333', fontWeight: 'bold' }}>Username</label>
                            <input
                                className="input"
                                type="text"
                                style={{ padding: '12px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem', width: '100%', boxSizing: 'border-box' }}
                                value={username}
                                onChange={e => setUsername(e.target.value)}
                            />
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                            <label style={{ fontSize: '0.85rem', color: '#333', fontWeight: 'bold' }}>Password</label>
                            <input
                                className="input"
                                type="password"
                                style={{ padding: '12px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem', width: '100%', boxSizing: 'border-box' }}
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                            />
                        </div>
                        <button className="btn btn-primary" type="submit" style={{ alignSelf: 'flex-end', padding: '14px', borderRadius: '24px', fontWeight: 'bold', marginTop: '16px', backgroundColor: '#0057ff', color: '#fff', border: 'none', cursor: 'pointer', fontSize: '1rem' }}>
                            {isRegister ? 'Sign Up' : 'Continue'}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}
