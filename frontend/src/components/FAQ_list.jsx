const FAQ_list = (props) =>{

    // const {

    // } = props

    const handleClick = () => {
        
    }

    return(
        <div className="faq-list">
            <div className="faq-item">
                <button
                    onClick={handleClick}
                    className="faq-question"
                    >
                    Какие площадки поддерживает MarketPulse?
                    <span className="faq-icon">+</span>
                </button>
                <div className="faq-answer">
                    <p>Мы поддерживаем Wildberries, Ozon, Avito, Яндекс Маркет, AliExpress, MegaMarket, а также ряд региональных маркетплейсов и досок объявлений. Список площадок постоянно расширяется.</p>
                </div>
            </div>
            <div className="faq-item">
                <button className="faq-question">
                    Как часто обновляются данные?
                    <span className="faq-icon">+</span>
                </button>
                <div className="faq-answer">
                    <p>Частота обновления зависит от тарифа: на бесплатном — раз в сутки, на Профессиональном — каждые 15 минут, на Корпоративном — в реальном времени.</p>
                </div>
            </div>
            <div className="faq-item">
                <button className="faq-question">
                    Нужно ли подключать мои магазины?
                    <span className="faq-icon">+</span>
                </button>
                <div className="faq-answer">
                    <p>Нет, для базового мониторинга конкурентов подключение вашего магазина не требуется. Вы просто указываете товары или категории, которые хотите отслеживать. Подключение нужно только для функции автоценообразования.</p>
                </div>
            </div>
            <div className="faq-item">
                <button className="faq-question">
                    Есть ли бесплатный тариф?
                    <span className="faq-icon">+</span>
                </button>
                <div className="faq-answer">
                    <p>Да! Стартовый тариф полностью бесплатный и позволяет отслеживать до 50 товаров на 2 маркетплейсах. Кроме того, на платных тарифах доступен 14-дневный бесплатный trial.</p>
                </div>
            </div>
            <div className="faq-item">
                <button className="faq-question">
                    Могу ли я интегрировать MarketPulse с моей CRM?
                    <span className="faq-icon">+</span>
                </button>
                <div className="faq-answer">
                    <p>Да, на тарифах Профессиональный и Корпоративный доступен REST API и вебхуки. Мы также имеем готовые интеграции с популярными CRM-системами и сервисами аналитики.</p>
                </div>
            </div>
        </div>
    )
} 

export default FAQ_list