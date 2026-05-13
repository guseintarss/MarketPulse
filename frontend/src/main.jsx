import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import Header from './components/Header/Header.jsx'
import Hero from './components/Hero/Hero.jsx'
import './style.css'
import Platforms from './components/Platforms/Platformfs.jsx'
import FAQ from './components/FAQ/FAQ.jsx'
import Features from './components/Features/Features.jsx'
import How_it_works from './components/How_it_works/How_it_works.jsx'
import Pricing from './components/Pricing/Pricing.jsx'
import Testimonials from './components/Testimonials/Testimonials.jsx'
import CTA from './components/CTA/CTA.jsx'
import Footer from './components/Footer/Footer.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Header />
    <Hero />
    <Platforms />
    <Features />
    <How_it_works />
    <Pricing />
    <Testimonials />
    <FAQ />
    <CTA />
    <Footer />
  </StrictMode>,
)
