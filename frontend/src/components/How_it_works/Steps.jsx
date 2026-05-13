const Steps = () => {
    return(
        <div className="steps">
            <div className="step">
                <div className="step-number">1</div>
                <h3>Добавьте товары конкурентов</h3>
                <p>Укажите ссылки на товары конкурентов или выберите категорию — мы найдём ключевых игроков автоматически.</p>
            </div>
            <div className="step">
                <div className="step-number">2</div>
                <h3>Настройте правила</h3>
                <p>Задайте параметры отслеживания: какие цены мониторить, какие уведомления получать и как часто.</p>
            </div>
            <div className="step">
                <div className="step-number">3</div>
                <h3>Получайте инсайты</h3>
                <p>Анализируйте данные в реальном времени, получайте рекомендации и адаптируйте стратегию продаж.</p>
            </div>
        </div>
    )
}

export default Steps