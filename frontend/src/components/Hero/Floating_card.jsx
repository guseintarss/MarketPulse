const Floating_card = () => {
    return(
        <>
            <div className="floating-card floating-card-1">
                <div className="fc-icon" style={{background:'rgba(239,68,68,0.1)'}}>📉</div>
                <div className="fc-num" style={{color:'#ef4444'}}>−18%</div>
                <div className="fc-label">Цена конкурента</div>
            </div>
            <div className="floating-card floating-card-2">
                <div className="fc-icon" style={{background:'rgba(6,214,160,0.1)'}}>🔔</div>
                <div className="fc-num" style={{color: '#22c55e'}}>+24%</div>
                <div className="fc-label">Рост продаж</div>
            </div>
        </>
    )
}

export default Floating_card