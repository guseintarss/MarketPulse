import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import Header from './components/Header.jsx'
import Hero from './components/Hero.jsx'
import './style.css'
import Platforms from './components/Platformfs.jsx'
import FAQ from './components/FAQ.jsx'
import Features from './components/Features.jsx'
import How_it_works from './components/How_it_works.jsx'
import Pricing from './components/Pricing.jsx'
import Testimonials from './components/Testimonials.jsx'
import CTA from './components/CTA.jsx'
import Footer from './components/Footer.jsx'

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
