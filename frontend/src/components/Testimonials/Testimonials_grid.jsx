const Testimonials_grid = () => {
    return(
        <div className="testimonials-grid">
            <div className="testimonial-card">
                <div className="testimonial-stars">★★★★★</div>
                <p className="testimonial-text">«Благодаря MarketPulse мы за месяц скорректировали цены на 300+ товаров и увеличили маржу на 18%. Теперь мы всегда в курсе, что делают конкуренты.»</p>
                <div className="testimonial-author">
                    <div className="testimonial-avatar" style={{background:'var(--primary)'}}>АК</div>
                    <div>
                        <div className="testimonial-name">Алексей Козлов</div>
                        <div className="testimonial-role">Директор, TechStore</div>
                    </div>
                </div>
            </div>
            <div className="testimonial-card">
                <div className="testimonial-stars">★★★★★</div>
                <p className="testimonial-text">«Раньше мы тратили часы на ручной мониторинг цен. MarketPulse сделал это автоматически. Экономим 20 часов в неделю и реагируем на изменения мгновенно.»</p>
                <div className="testimonial-author">
                    <div className="testimonial-avatar" style={{background:'var(--accent)'}}>МС</div>
                    <div>
                        <div className="testimonial-name">Мария Соколова</div>
                        <div className="testimonial-role">E-commerce менеджер, StyleBox</div>
                    </div>
                </div>
            </div>
            <div className="testimonial-card">
                <div className="testimonial-stars">★★★★★</div>
                <p className="testimonial-text">«Функция автоценообразования — это просто магия. Настроили один раз правила, и система сама держит наши цены конкурентоспособными. Продажи выросли на 35%.»</p>
                <div className="testimonial-author">
                    <div className="testimonial-avatar" style={{background:'#f97316'}}>ДВ</div>
                    <div>
                        <div className="testimonial-name">Дмитрий Волков</div>
                        <div className="testimonial-role">Владелец, HomeGoods</div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Testimonials_grid