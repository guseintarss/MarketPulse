import FAQ_list from "./FAQ_list"

const FAQ = () =>{
    return(
        <section className="faq" id="faq">
            <div className="container">
                <div className="text-center">
                    <span className="section-label">FAQ</span>
                    <h2 className="section-title">Частые <span className="text-gradient">вопросы</span></h2>
                    <p className="section-subtitle">Ответы на самые популярные вопросы о MarketPulse</p>
                </div>
                <FAQ_list />
            </div>
        </section>
    )
}

export default FAQ