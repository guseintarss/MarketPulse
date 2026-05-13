import Testimonials_grid from "./Testimonials_grid"

const Testimonials = () => {
    return(
        <section className="testimonials">
            <div className="container">
                <div className="text-center">
                    <span className="section-label">Отзывы</span>
                    <h2 className="section-title">Что говорят наши <span className="text-gradient">клиенты</span></h2>
                    <p className="section-subtitle">Более 12 000 продавцов уже используют MarketPulse для роста продаж</p>
                </div>
                <Testimonials_grid />
            </div>
        </section>
    )
}

export default Testimonials