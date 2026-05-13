const Dashboard = () => {
    return(
        <div className="dashboard-mockup">
            <div className="mockup-row">
                <div className="mockup-product">
                    <div className="mockup-avatar" style={{background:'rgba(108,58,237,0.1)'}}>🎧</div>
                    <div>
                        <div className="mockup-name">Наушники Pro X1</div>
                        <div className="mockup-platform">Wildberries</div>
                    </div>
                </div>
                <div className="mockup-price">2 490 ₽</div>
                <div className="mockup-change down">−12%</div>
            </div>
            <div className="mockup-row">
                <div className="mockup-product">
                    <div className="mockup-avatar" style={{background:'rgba(6,214,160,0.1)'}}>📱</div>
                    <div>
                        <div className="mockup-name">Чехол iPhone 15</div>
                        <div className="mockup-platform">Ozon</div>
                    </div>
                </div>
                <div className="mockup-price">890 ₽</div>
                <div className="mockup-change up">+5%</div>
            </div>
            <div className="mockup-row">
                <div className="mockup-product">
                    <div className="mockup-avatar" style={{background:'rgba(59,130,246,0.1)'}}>⌚</div>
                    <div>
                        <div className="mockup-name">Смарт-часы FitBand</div>
                        <div className="mockup-platform">Avito</div>
                    </div>
                </div>
                <div className="mockup-price">3 200 ₽</div>
                <div className="mockup-change down">−8%</div>
            </div>
            <div className="mockup-row">
                <div className="mockup-product">
                    <div className="mockup-avatar" style={{background:'rgba(251,146,60,0.1)'}}>💡</div>
                    <div>
                        <div className="mockup-name">LED-лампа Smart</div>
                        <div className="mockup-platform">Я.Маркет</div>
                    </div>
                </div>
                <div className="mockup-price">1 190 ₽</div>
                <div className="mockup-change up">+3%</div>
            </div>
        </div>
    )
}

export default Dashboard