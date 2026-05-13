import Hero_cont from "./Hero_cont"
import Hero_visual from "./Hero_visual"

const Hero = () => {
    return(
        <section className="hero">
            <div className="container">
                
                <Hero_cont />
                <Hero_visual />
            </div>
        </section>
    )
}

export default Hero