import { useAnimateOnScroll } from '../../hooks/useAnimateOnScroll';

const Feat_grid = (props) =>{

    const ref = useAnimateOnScroll({
        threshold: 0.1,
        animateClass: 'is-visible',
        // Опционально: задержка для каскадной анимации
    });


    return(
        <div className="features-grid">
            <div className="feature-card">
                <div className="feature-icon purple">📊</div>
                <h3>Мониторинг цен 24/7</h3>
                <p>Автоматическое отслеживание цен конкурентов на всех подключённых площадках с обновлением каждые 15 минут.</p>
            </div>
            <div className="feature-card">
                <div className="feature-icon green">🔔</div>
                <h3>Умные уведомления</h3>
                <p>Мгновенные алерты при изменении цен, появлении новых конкурентов или изменении остатков на складах.</p>
            </div>
            <div className="feature-card">
                <div className="feature-icon blue">📈</div>
                <h3>Аналитика и отчёты</h3>
                <p>Наглядные графики и дашборды с историей цен, динамикой продаж и рекомендациями по ценообразованию.</p>
            </div>
            <div className="feature-card">
                <div className="feature-icon orange">🎯</div>
                <h3>Анализ ассортимента</h3>
                <p>Сравнивайте свой ассортимент с конкурентами, находите ниши и новые товары для расширения каталога.</p>
            </div>
            <div className="feature-card">
                <div className="feature-icon pink">⚡</div>
                <h3>Автоценообразование</h3>
                <p>Настраивайте правила автоматического изменения ваших цен на основе стратегии конкурентов.</p>
            </div>
            <div className="feature-card">
                <div className="feature-icon teal">🔗</div>
                <h3>API и интеграции</h3>
                <p>Подключайте MarketPulse к вашим CRM, ERP и другим системам через удобный REST API.</p>
            </div>
        </div>
    )
}

export default Feat_grid