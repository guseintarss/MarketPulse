import Footer_bottom from "./Footer_bottom"
import Footer_grid from "./Footer_grid"

const Footer = () =>{
    return(
        <footer className="footer">
            <div className="container">
                <Footer_grid />
                <Footer_bottom />
            </div>
        </footer>
    )
}

export default Footer