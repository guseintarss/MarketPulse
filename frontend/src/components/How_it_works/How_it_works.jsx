import Steps from "./Steps"

const How_it_works = () =>{
    return(
        <section className="how-it-works" id="how">
            <div className="container">
                <div className="text-center">
                    <span className="section-label">Как это работает</span>
                    <h2 className="section-title">Три шага к <span className="text-gradient">полному контролю</span></h2>
                    <p className="section-subtitle">Начните мониторинг за считанные минуты — без сложных настроек и технических знаний</p>
                </div>
                <Steps />
            </div>
        </section>
    )
}

export default How_it_works