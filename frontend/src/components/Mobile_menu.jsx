const Mobile_menu = () => {

    const mobiClose = () =>{
        mobileMenu.classList.remove('open')
    }

    return(
        <div className="mobile-menu" id="mobileMenu">
            <a onClick={mobiClose} href="#features">Возможности</a>
            <a onClick={mobiClose} href="#how">Как работает</a>
            <a onClick={mobiClose} href="#pricing">Тарифы</a>
            <a onClick={mobiClose} href="#faq">FAQ</a>
            <a onClick={mobiClose} href="#" className="btn btn-primary" style={{textAlign:'center', marginTop:8, }}>Попробовать бесплатно</a>
        </div>
    )
}

export default Mobile_menu