import Mobile_menu from './Mobile_menu'
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../auth/AuthContext';

const Header = (props) => {
    const [isScrolled, setIsScrolled] = useState(false);
    const { user, logout } = useAuth();
    const brandName = 'MarketPulse'

    useEffect(() => {
        const handleScroll = () => {
        setIsScrolled(window.scrollY > 20);
        };
        window.addEventListener('scroll', handleScroll, { passive: true });
        handleScroll();
        return () => {
        window.removeEventListener('scroll', handleScroll);
        };
    }, []);

    const mobileClick = () =>{
        mobileMenu.classList.toggle('open');
    }

    return(
        <header className="header" id="header">
            <div className="container">
                <nav className="nav">
                    <Link to="/" className="logo">
                        <div className="logo-icon">⚡</div>
                        {brandName}
                    </Link>
                    <ul className="nav-links">
                        <li><a href="/#features">Возможности</a></li>
                        <li><a href="/#how">Как работает</a></li>
                        <li><a href="/#pricing">Тарифы</a></li>
                        <li><a href="/#faq">FAQ</a></li>
                        {user && <li><Link to="/dashboard">Дашборд</Link></li>}
                    </ul>
                    <div className="nav-cta">
                        {user ? (
                            <>
                                <span style={{ fontWeight: 600, color: '#6C3AED' }}>{user.username}</span>
                                <button onClick={logout} className="btn btn-outline" style={{ padding: '8px 20px', fontSize: '0.9rem', cursor: 'pointer' }}>Выйти</button>
                            </>
                        ) : (
                            <>
                                <Link to="/login" className="btn btn-outline">Войти</Link>
                                <Link to="/register" className="btn btn-primary">Регистрация</Link>
                            </>
                        )}
                    </div>
                    <button className="hamburger" id="hamburger" onClick={mobileClick} aria-label="Меню">
                        <span></span><span></span><span></span>
                    </button>
                    <Mobile_menu />
                </nav>
            </div>
        </header>
    )
}

export default Header
