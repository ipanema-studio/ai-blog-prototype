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
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
            <div className="card" style={{ width: 300 }}>
                <h2>{isRegister ? 'Register' : 'Login'}</h2>
                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
                    <input
                        className="input"
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={e => setUsername(e.target.value)}
                    />
                    <input
                        className="input"
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                    />
                    <button className="btn btn-primary" type="submit">
                        {isRegister ? 'Sign Up' : 'Log In'}
                    </button>
                </form>
                {/* <p style={{ marginTop: 16, textAlign: 'center', cursor: 'pointer', color: 'var(--primary)' }} onClick={() => setIsRegister(!isRegister)}>
                    {isRegister ? 'Already have an account? Login' : 'Need an account? Register'}
                </p> */}
            </div>
        </div>
    );
}
