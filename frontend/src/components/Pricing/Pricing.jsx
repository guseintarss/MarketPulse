import Pricing_grid from "./Pricing_grid"

const Pricing = () => {
    return(
        <section className="pricing" id="pricing">
            <div className="container">
                <div className="text-center">
                    <span className="section-label">Тарифы</span>
                    <h2 className="section-title">Выберите свой <span className="text-gradient">план роста</span></h2>
                    <p className="section-subtitle">14 дней бесплатного trial на любом тарифе. Без привязки карты.</p>
                </div>
                <Pricing_grid />
            </div>
        </section>
    )  
}

export default Pricing