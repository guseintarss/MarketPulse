import Feat_grid from './Feat_grid'

const Features = () => {
    return(
        <section className="features" id="features">
            <div className="container">
                <div className="text-center">
                    <span className="section-label">Возможности</span>
                    <h2 className="section-title">Всё, что нужно для <span className="text-gradient">лидерства</span> на рынке</h2>
                    <p className="section-subtitle">Мощные инструменты аналитики, которые помогут вам опередить конкурентов и максимизировать прибыль</p>
                </div>
                <Feat_grid />
            </div>
        </section>
    )
}

export default Features