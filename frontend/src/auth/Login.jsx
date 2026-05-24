import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { login, getMe } from '../api';
import { useAuth } from './AuthContext';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { setUser } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const data = await login(username, password);
      localStorage.setItem('token', data.access_token);
      const user = await getMe();
      setUser(user);
      navigate('/');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#fafafa' }}>
      <form onSubmit={handleSubmit} style={{ background: 'white', padding: 40, borderRadius: 16, boxShadow: '0 4px 24px rgba(108,58,237,0.1)', width: 400, maxWidth: '90%' }}>
        <div style={{ textAlign: 'center', marginBottom: 24 }}>
          <Link to="/" style={{ fontSize: '1.4rem', fontWeight: 800, color: '#1a1a2e', textDecoration: 'none' }}>⚡ MarketPulse</Link>
          <h2 style={{ marginTop: 16, fontSize: '1.5rem' }}>Вход</h2>
        </div>
        {error && <div style={{ color: '#ef4444', marginBottom: 16, fontSize: '0.9rem', textAlign: 'center' }}>{error}</div>}
        <div style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', marginBottom: 6, fontWeight: 600, fontSize: '0.9rem' }}>Имя пользователя</label>
          <input value={username} onChange={e => setUsername(e.target.value)} required
            style={{ width: '100%', padding: '12px 16px', border: '1px solid #c4c4d4', borderRadius: 8, fontSize: '1rem' }} />
        </div>
        <div style={{ marginBottom: 24 }}>
          <label style={{ display: 'block', marginBottom: 6, fontWeight: 600, fontSize: '0.9rem' }}>Пароль</label>
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} required
            style={{ width: '100%', padding: '12px 16px', border: '1px solid #c4c4d4', borderRadius: 8, fontSize: '1rem' }} />
        </div>
        <button type="submit" className="btn btn-primary" style={{ width: '100%', justifyContent: 'center' }}>Войти</button>
        <p style={{ textAlign: 'center', marginTop: 16, fontSize: '0.9rem', color: '#7c7c9a' }}>
          Нет аккаунта? <Link to="/register" style={{ color: '#6C3AED', fontWeight: 600 }}>Зарегистрироваться</Link>
        </p>
      </form>
    </div>
  );
}
