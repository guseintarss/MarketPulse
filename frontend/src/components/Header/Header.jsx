import Mobile_menu from './Mobile_menu'
import { useState, useEffect } from 'react';

const Header = (props) => {
    const [isScrolled, setIsScrolled] = useState(false);
    const brandName = 'MarketPulse'


    useEffect(() => {
        const handleScroll = () => {
        // Проверяем позицию скролла
        setIsScrolled(window.scrollY > 20);
        };

        // Добавляем слушатель
        window.addEventListener('scroll', handleScroll, { passive: true });
        
        // Проверяем при монтировании (если страница уже проскроллена)
        handleScroll();
        
        // Cleanup: убираем слушатель при размонтировании
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
                    <a href="#" className="logo">
                        <div className="logo-icon">⚡</div>
                        {brandName}
                    </a>
                    <ul className="nav-links">
                        <li><a href="#features">Возможности</a></li>
                        <li><a href="#how">Как работает</a></li>
                        <li><a href="#pricing">Тарифы</a></li>
                        <li><a href="#faq">FAQ</a></li>
                    </ul>
                    <div className="nav-cta">
                        <a href="#" className="btn btn-outline">Войти</a>
                        <a href="#pricing" className="btn btn-primary">Попробовать бесплатно</a>
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