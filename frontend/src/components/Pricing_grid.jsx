const Pricing_grid = () => {
    return(
        <div className="pricing-grid">
            <div className="price-card">
                <h3>Стартовый</h3>
                <p className="price-desc">Для начинающих продавцов</p>
                <div className="price-amount">0 ₽ <span>/ мес</span></div>
                <p className="price-period">Бесплатно навсегда</p>
                <ul className="price-features">
                    <li>До 50 товаров для мониторинга</li>
                    <li>2 маркетплейса</li>
                    <li>Обновление раз в сутки</li>
                    <li>Email-уведомления</li>
                    <li>Базовая аналитика</li>
                </ul>
                <a href="#" className="btn btn-outline">Начать бесплатно</a>
            </div>
            <div className="price-card popular">
                <h3>Профессиональный</h3>
                <p className="price-desc">Для активных продавцов</p>
                <div className="price-amount">2 990 ₽ <span>/ мес</span></div>
                <p className="price-period">При оплате за год — 1 990 ₽/мес</p>
                <ul className="price-features">
                    <li>До 2 000 товаров</li>
                    <li>Все маркетплейсы</li>
                    <li>Обновление каждые 15 минут</li>
                    <li>Telegram + Email алерты</li>
                    <li>Расширенная аналитика</li>
                    <li>Автоценообразование</li>
                    <li>Приоритетная поддержка</li>
                </ul>
                <a href="#" className="btn btn-primary">Попробовать 14 дней</a>
            </div>
            <div className="price-card">
                <h3>Корпоративный</h3>
                <p className="price-desc">Для крупных компаний</p>
                <div className="price-amount">9 990 ₽ <span>/ мес</span></div>
                <p className="price-period">Индивидуальные условия</p>
                <ul className="price-features">
                    <li>Безлимитные товары</li>
                    <li>Все площадки + доски объявлений</li>
                    <li>Обновление в реальном времени</li>
                    <li>Все виды уведомлений</li>
                    <li>API и вебхуки</li>
                    <li>Персональный менеджер</li>
                    <li>White-label отчёты</li>
                </ul>
                <a href="#" className="btn btn-outline">Связаться с нами</a>
            </div>
        </div>
    )
}

export default Pricing_grid