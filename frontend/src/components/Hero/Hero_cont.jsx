

const Hero_cont = () => {
    return(
        <div className="hero-content">
                    <div className="hero-badge">
                        <span className="dot"></span>
                        Мониторинг в реальном времени
                    </div>
                    <h1>
                        Знайте всё о <span className="text-gradient">ценах конкурентов</span> на маркетплейсах
                    </h1>
                    <p>
                        MarketPulse отслеживает цены, наличие и ассортимент ваших конкурентов на Wildberries, Ozon, Avito и других площадках. Принимайте решения на основе данных, а не догадок.
                    </p>
                    <div className="hero-buttons">
                        <a href="#pricing" className="btn btn-primary">
                            🚀 Начать бесплатно
                        </a>
                        <a href="#how" className="btn btn-outline">
                            ▶ Как это работает
                        </a>
                    </div>
                    <div className="hero-stats">
                        <div>
                            <div className="hero-stat-num">12 000+</div>
                            <div className="hero-stat-label">Активных продавцов</div>
                        </div>
                        <div>
                            <div className="hero-stat-num">50M+</div>
                            <div className="hero-stat-label">Товаров отслеживается</div>
                        </div>
                        <div>
                            <div className="hero-stat-num">99.8%</div>
                            <div className="hero-stat-label">Uptime сервиса</div>
                        </div>
                    </div>
                </div>
    )
}

export default Hero_cont