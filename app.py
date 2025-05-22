import streamlit as st
import streamlit_lottie as st_lottie
from streamlit_option_menu import option_menu
import hydralit_components as hc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from numpy import isin
import json
import requests
from PIL import Image
import time
import base64
from pathlib import Path
import os

# Page configuration
st.set_page_config(
    page_title="CloudSphere Consulting",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Create directory for assets if it doesn't exist
Path("assets").mkdir(exist_ok=True)


def load_lottieurl(url):
    """
    Load Lottie animation from URL
    
    Args:
        url (str): URL of the Lottie animation JSON
        
    Returns:
        dict: Lottie animation JSON data or None if failed
    """
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def load_lottiefile(filepath):
    """
    Load Lottie animation from local file
    
    Args:
        filepath (str): Path to the Lottie animation JSON file
        
    Returns:
        dict: Lottie animation JSON data
    """
    with open(filepath, "r") as f:
        return json.load(f)

def local_css(file_name):
    """
    Load and apply local CSS file
    
    Args:
        file_name (str): Path to the CSS file
    """
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def add_bg_from_local(image_file):
    """
    Add background image from local file
    
    Args:
        image_file (str): Path to the image file
    """
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def add_animation_script():
    """
    Add custom JavaScript for animations and responsive behavior
    """
    st.markdown(
        """
        <script>
        // Intersection Observer for scroll animations
        document.addEventListener('DOMContentLoaded', function() {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animate');
                    }
                });
            }, {
                threshold: 0.1
            });
            
            // Observe all elements with animation classes
            document.querySelectorAll('.fade-in, .fade-in-up, .fade-in-left, .fade-in-right').forEach(el => {
                observer.observe(el);
            });
            
            // Number counter animation
            document.querySelectorAll('.stat-number').forEach(counter => {
                const target = parseInt(counter.innerText);
                const duration = 2000;
                const step = target / duration * 10;
                let current = 0;
                
                const updateCounter = () => {
                    current += step;
                    if (current < target) {
                        counter.innerText = Math.floor(current) + (counter.innerText.includes('%') ? '%' : '+');
                        setTimeout(updateCounter, 10);
                    } else {
                        counter.innerText = target + (counter.innerText.includes('%') ? '%' : '+');
                    }
                };
                
                updateCounter();
            });
            
            // Add scroll indicator
            const scrollIndicator = document.createElement('div');
            scrollIndicator.className = 'scroll-indicator';
            document.body.appendChild(scrollIndicator);
            
            window.addEventListener('scroll', () => {
                const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
                const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                const scrolled = (winScroll / height) * 100;
                scrollIndicator.style.width = scrolled + '%';
                
                // Show/hide scroll to top button
                const scrollToTopBtn = document.querySelector('.scroll-to-top');
                if (scrollToTopBtn) {
                    if (winScroll > 300) {
                        scrollToTopBtn.classList.add('visible');
                    } else {
                        scrollToTopBtn.classList.remove('visible');
                    }
                }
            });
            
            // Add scroll to top button
            const scrollToTopBtn = document.createElement('div');
            scrollToTopBtn.className = 'scroll-to-top';
            scrollToTopBtn.innerHTML = '↑';
            document.body.appendChild(scrollToTopBtn);
            
            scrollToTopBtn.addEventListener('click', () => {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
            
            // Add responsive menu toggle for mobile
            const addResponsiveMenu = () => {
                if (window.innerWidth <= 768) {
                    const menuItems = document.querySelectorAll('.nav-link');
                    const menuContainer = document.querySelector('.stHorizontalBlock');
                    
                    if (menuContainer) {
                        const menuToggle = document.createElement('div');
                        menuToggle.className = 'mobile-menu-toggle';
                        menuToggle.innerHTML = '☰';
                        menuContainer.parentNode.insertBefore(menuToggle, menuContainer);
                        
                        menuToggle.addEventListener('click', () => {
                            menuContainer.classList.toggle('show-mobile-menu');
                        });
                    }
                }
            };
            
            // Call responsive menu function
            addResponsiveMenu();
            
            // Handle window resize
            window.addEventListener('resize', () => {
                addResponsiveMenu();
            });
        });
        </script>
        
        <style>
        /* Mobile Menu Styles */
        .mobile-menu-toggle {
            display: none;
        }
        
        @media (max-width: 768px) {
            .mobile-menu-toggle {
                display: block;
                position: fixed;
                top: 15px;
                right: 15px;
                z-index: 1000;
                background: rgba(30, 136, 229, 0.8);
                color: white;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                cursor: pointer;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            }
            
            .stHorizontalBlock {
                display: none !important;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: auto;
                background: rgba(17, 34, 64, 0.95);
                z-index: 999;
                flex-direction: column !important;
                padding: 60px 20px 20px;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
            }
            
            .stHorizontalBlock.show-mobile-menu {
                display: flex !important;
            }
            
            .stHorizontalBlock > div {
                width: 100% !important;
                margin-bottom: 10px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def add_particles_background():
    """
    Add interactive particle background
    """
    st.markdown(
        """
        <div id="particles-js" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; z-index: -1;"></div>
        <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            particlesJS('particles-js', {
                "particles": {
                    "number": {
                        "value": 80,
                        "density": {
                            "enable": true,
                            "value_area": 800
                        }
                    },
                    "color": {
                        "value": "#1E88E5"
                    },
                    "shape": {
                        "type": "circle",
                        "stroke": {
                            "width": 0,
                            "color": "#000000"
                        },
                        "polygon": {
                            "nb_sides": 5
                        }
                    },
                    "opacity": {
                        "value": 0.3,
                        "random": false,
                        "anim": {
                            "enable": false,
                            "speed": 1,
                            "opacity_min": 0.1,
                            "sync": false
                        }
                    },
                    "size": {
                        "value": 3,
                        "random": true,
                        "anim": {
                            "enable": false,
                            "speed": 40,
                            "size_min": 0.1,
                            "sync": false
                        }
                    },
                    "line_linked": {
                        "enable": true,
                        "distance": 150,
                        "color": "#1E88E5",
                        "opacity": 0.2,
                        "width": 1
                    },
                    "move": {
                        "enable": true,
                        "speed": 2,
                        "direction": "none",
                        "random": false,
                        "straight": false,
                        "out_mode": "out",
                        "bounce": false,
                        "attract": {
                            "enable": false,
                            "rotateX": 600,
                            "rotateY": 1200
                        }
                    }
                },
                "interactivity": {
                    "detect_on": "canvas",
                    "events": {
                        "onhover": {
                            "enable": true,
                            "mode": "grab"
                        },
                        "onclick": {
                            "enable": true,
                            "mode": "push"
                        },
                        "resize": true
                    },
                    "modes": {
                        "grab": {
                            "distance": 140,
                            "line_linked": {
                                "opacity": 0.5
                            }
                        },
                        "bubble": {
                            "distance": 400,
                            "size": 40,
                            "duration": 2,
                            "opacity": 8,
                            "speed": 3
                        },
                        "repulse": {
                            "distance": 200,
                            "duration": 0.4
                        },
                        "push": {
                            "particles_nb": 4
                        },
                        "remove": {
                            "particles_nb": 2
                        }
                    }
                },
                "retina_detect": true
            });
        });
        </script>
        """,
        unsafe_allow_html=True
    )

def add_typing_animation(text, element_id):
    """
    Add typing animation effect
    
    Args:
        text (str): Text to animate
        element_id (str): HTML element ID
    """
    st.markdown(
        f"""
        <div id="{element_id}" class="typing-text"></div>
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const text = "{text}";
            const typingElement = document.getElementById("{element_id}");
            let i = 0;
            
            function typeWriter() {{
                if (i < text.length) {{
                    typingElement.innerHTML += text.charAt(i);
                    i++;
                    setTimeout(typeWriter, 50);
                }}
            }}
            
            typeWriter();
        }});
        </script>
        """,
        unsafe_allow_html=True
    )

def add_responsive_meta_tags():
    """
    Add responsive meta tags for better mobile experience
    """
    st.markdown(
        """
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        """,
        unsafe_allow_html=True
    )

def add_touch_support():
    """
    Add touch support for mobile devices
    """
    st.markdown(
        """
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Convert hover effects to touch events for mobile
            const touchElements = document.querySelectorAll('.service-card, .case-study-card, .team-card, .expert-card, .tilt-card');
            
            touchElements.forEach(el => {
                el.addEventListener('touchstart', () => {
                    el.classList.add('touch-active');
                });
                
                el.addEventListener('touchend', () => {
                    setTimeout(() => {
                        el.classList.remove('touch-active');
                    }, 300);
                });
            });
            
            // Add swipe support for carousels
            const carousel = document.querySelector('.carousel-items');
            if (carousel) {
                let startX, endX;
                
                carousel.addEventListener('touchstart', (e) => {
                    startX = e.touches[0].clientX;
                });
                
                carousel.addEventListener('touchend', (e) => {
                    endX = e.changedTouches[0].clientX;
                    
                    if (startX - endX > 50) {
                        // Swipe left - next slide
                        const nextBtn = document.querySelector('.carousel-next');
                        if (nextBtn) nextBtn.click();
                    } else if (endX - startX > 50) {
                        // Swipe right - previous slide
                        const prevBtn = document.querySelector('.carousel-prev');
                        if (prevBtn) prevBtn.click();
                    }
                });
            }
        });
        </script>
        
        <style>
        /* Touch active states for mobile */
        .touch-active {
            transform: translateY(-5px) !important;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3) !important;
            border-color: rgba(30, 136, 229, 0.5) !important;
        }
        
        /* Improved tap targets for mobile */
        @media (max-width: 768px) {
            .cta-button, .service-link, .case-study-link, button {
                padding: 12px 20px !important;
                min-height: 44px !important;
                min-width: 44px !important;
            }
            
            .team-social span {
                padding: 8px !important;
                margin: 0 5px !important;
                display: inline-block !important;
            }
            
            /* Adjust font sizes for mobile */
            .hero-text h1 {
                font-size: 2.2rem !important;
            }
            
            .page-title {
                font-size: 2.2rem !important;
            }
            
            .section-title {
                font-size: 1.8rem !important;
            }
            
            /* Stack columns on mobile */
            .mobile-stack {
                flex-direction: column !important;
            }
            
            .mobile-stack > div {
                width: 100% !important;
                margin-bottom: 20px !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def add_responsive_styles():
    """
    Add responsive styles for different screen sizes
    """
    st.markdown(
        """
        <style>
        /* Extra small devices (phones, 600px and down) */
        @media only screen and (max-width: 600px) {
            .hero-text h1 {
                font-size: 2rem !important;
            }
            
            .hero-text p {
                font-size: 1rem !important;
            }
            
            .page-title {
                font-size: 2rem !important;
            }
            
            .section-title {
                font-size: 1.6rem !important;
            }
            
            .cta-button {
                width: 100% !important;
                margin-bottom: 10px !important;
            }
            
            .stat-number {
                font-size: 2rem !important;
            }
            
            .stat-label {
                font-size: 0.9rem !important;
            }
            
            .service-card, .case-study-card, .team-card {
                height: auto !important;
                min-height: 200px !important;
            }
            
            .contact-method {
                flex-direction: column !important;
            }
            
            .contact-icon {
                margin-bottom: 10px !important;
            }
        }
        
        /* Small devices (portrait tablets and large phones, 600px and up) */
        @media only screen and (min-width: 600px) and (max-width: 768px) {
            .hero-text h1 {
                font-size: 2.5rem !important;
            }
            
            .service-card, .case-study-card, .team-card {
                height: auto !important;
                min-height: 250px !important;
            }
        }
        
        /* Medium devices (landscape tablets, 768px and up) */
        @media only screen and (min-width: 768px) and (max-width: 992px) {
            .hero-text h1 {
                font-size: 2.8rem !important;
            }
            
            .service-card, .case-study-card, .team-card {
                height: auto !important;
                min-height: 300px !important;
            }
        }
        
        /* Large devices (laptops/desktops, 992px and up) */
        @media only screen and (min-width: 992px) {
            /* Default styles apply */
        }
        
        /* Fix for Streamlit components on mobile */
        @media only screen and (max-width: 768px) {
            .stHorizontalBlock {
                flex-wrap: wrap !important;
            }
            
            .stHorizontalBlock > div {
                flex: 1 1 100% !important;
                width: 100% !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ============================================================================
# UI COMPONENT FUNCTIONS
# ============================================================================

def animated_progress_bar(label, percent, color="#1E88E5"):
    """
    Create an animated progress bar
    
    Args:
        label (str): Label for the progress bar
        percent (int): Percentage value (0-100)
        color (str, optional): Color of the progress bar. Defaults to "#1E88E5".
    """
    st.markdown(
        f"""
        <div class="progress-container">
            <div class="progress-label">{label} <span class="progress-percent">{percent}%</span></div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: 0%; background-color: {color};" data-width="{percent}%"></div>
            </div>
        </div>
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const progressBars = document.querySelectorAll('.progress-bar-fill');
            
            setTimeout(() => {{
                progressBars.forEach(bar => {{
                    const targetWidth = bar.getAttribute('data-width');
                    bar.style.width = targetWidth;
                }});
            }}, 300);
        }});
        </script>
        """,
        unsafe_allow_html=True
    )

def animated_counter(label, value, prefix="", suffix=""):
    """
    Create an animated counter
    
    Args:
        label (str): Label for the counter
        value (int): Target value to count to
        prefix (str, optional): Prefix for the value. Defaults to "".
        suffix (str, optional): Suffix for the value. Defaults to "".
    """
    st.markdown(
        f"""
        <div class="counter-container">
            <div class="counter-value" data-target="{value}">0</div>
            <div class="counter-label">{label}</div>
        </div>
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const counters = document.querySelectorAll('.counter-value');
            const speed = 200;
            
            counters.forEach(counter => {{
                const updateCount = () => {{
                    const target = +counter.getAttribute('data-target');
                    const count = +counter.innerText.replace(/[^0-9]/g, '');
                    const inc = target / speed;
                    
                    if (count < target) {{
                        counter.innerText = '{prefix}' + Math.ceil(count + inc) + '{suffix}';
                        setTimeout(updateCount, 1);
                    }} else {{
                        counter.innerText = '{prefix}' + target + '{suffix}';
                    }}
                }};
                
                updateCount();
            }});
        }});
        </script>
        """,
        unsafe_allow_html=True
    )

def animated_card_reveal(title, content, icon="☁️"):
    """
    Create an animated card with reveal effect
    
    Args:
        title (str): Card title
        content (str): Card content
        icon (str, optional): Icon for the card. Defaults to "☁️".
    """
    st.markdown(
        f"""
        <div class="reveal-card">
            <div class="reveal-card-icon">{icon}</div>
            <h3 class="reveal-card-title">{title}</h3>
            <p class="reveal-card-content">{content}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def tilt_card(title, content, image_url=None):
    """
    Create a card with 3D tilt effect
    
    Args:
        title (str): Card title
        content (str): Card content
        image_url (str, optional): URL for card image. Defaults to None.
    """
    st.markdown(
        f"""
        <div class="tilt-card-wrapper">
            <div class="tilt-card">
                {f'<div class="tilt-card-image" style="background-image: url({image_url});"></div>' if image_url else ''}
                <div class="tilt-card-content">
                    <h3>{title}</h3>
                    <p>{content}</p>
                </div>
            </div>
        </div>
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const cards = document.querySelectorAll('.tilt-card');
            
            cards.forEach(card => {{
                card.addEventListener('mousemove', e => {{
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    
                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;
                    
                    const rotateX = (y - centerY) / 10;
                    const rotateY = (centerX - x) / 10;
                    
                    card.style.transform = `perspective(1000px) rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg)`;
                }});
                
                card.addEventListener('mouseleave', () => {{
                    card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
                }});
            }});
        }});
        </script>
        """,
        unsafe_allow_html=True
    )

def floating_element(content, delay=0):
    """
    Create a floating animation effect for content
    
    Args:
        content (str): HTML content to animate
        delay (int, optional): Animation delay in seconds. Defaults to 0.
    """
    st.markdown(
        f"""
        <div class="floating-element" style="animation-delay: {delay}s;">
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )

def gradient_button(label, key=None):
    """
    Create an animated gradient button
    
    Args:
        label (str): Button label
        key (str, optional): Unique key for the button. Defaults to None.
        
    Returns:
        bool: True if button was clicked, False otherwise
    """
    button_id = key if key else f"gradient-btn-{label.replace(' ', '-').lower()}"
    clicked = st.markdown(
        f"""
        <button id="{button_id}" class="gradient-button">
            <span>{label}</span>
        </button>
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const button = document.getElementById('{button_id}');
            button.addEventListener('click', function() {{
                const event = new CustomEvent('streamlit:buttonClicked', {{ detail: {{ key: '{button_id}' }} }});
                window.dispatchEvent(event);
            }});
        }});
        </script>
        """,
        unsafe_allow_html=True
    )
    
    # Check if button was clicked using session state
    if button_id not in st.session_state:
        st.session_state[button_id] = False
    
    # Use a placeholder to detect clicks
    placeholder = st.empty()
    if placeholder.button("Hidden Button", key=f"hidden-{button_id}", help="This is a hidden button"):
        st.session_state[button_id] = True
    
    # Hide the placeholder
    st.markdown(
        """
        <style>
        [data-testid="stButton"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    return st.session_state[button_id]

def wave_divider():
    """
    Create an animated wave divider
    """
    st.markdown(
        """
        <div class="wave-divider">
            <svg viewBox="0 0 1200 120" preserveAspectRatio="none">
                <path d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z" class="wave-fill"></path>
            </svg>
        </div>
        """,
        unsafe_allow_html=True
    )

def number_counter(start_value, end_value, prefix="", suffix="", duration=2000):
    """
    Create an animated number counter
    
    Args:
        start_value (int): Starting value
        end_value (int): Ending value
        prefix (str, optional): Prefix for the value. Defaults to "".
        suffix (str, optional): Suffix for the value. Defaults to "".
        duration (int, optional): Animation duration in milliseconds. Defaults to 2000.
    """
    counter_id = f"counter-{end_value}"
    st.markdown(
        f"""
        <div id="{counter_id}" class="number-counter">{prefix}{start_value}{suffix}</div>
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const counter = document.getElementById('{counter_id}');
            const startValue = {start_value};
            const endValue = {end_value};
            const duration = {duration};
            const step = (endValue - startValue) / (duration / 10);
            let current = startValue;
            
            const updateCounter = () => {{
                current += step;
                if (current < endValue) {{
                    counter.innerText = '{prefix}' + Math.floor(current) + '{suffix}';
                    setTimeout(updateCounter, 10);
                }} else {{
                    counter.innerText = '{prefix}' + endValue + '{suffix}';
                }}
            }};
            
            updateCounter();
        }});
        </script>
        """,
        unsafe_allow_html=True
    )

def skill_bars():
    """
    Create animated skill bars for cloud expertise
    """
    skills = [
        {"name": "Cloud Migration", "percentage": 95, "color": "#1E88E5"},
        {"name": "Cloud Security", "percentage": 90, "color": "#42A5F5"},
        {"name": "Multi-Cloud Management", "percentage": 85, "color": "#64B5F6"},
        {"name": "Cloud Cost Optimization", "percentage": 92, "color": "#90CAF9"},
        {"name": "Cloud Architecture", "percentage": 88, "color": "#BBDEFB"}
    ]
    
    for skill in skills:
        animated_progress_bar(skill["name"], skill["percentage"], skill["color"])

def animated_timeline(events):
    """
    Create an animated timeline
    
    Args:
        events (list): List of timeline events with date, title, and description
    """
    timeline_html = '<div class="timeline">'
    
    for i, event in enumerate(events):
        timeline_html += f"""
        <div class="timeline-item {'left' if i % 2 == 0 else 'right'}">
            <div class="timeline-content">
                <div class="timeline-date">{event['date']}</div>
                <h3 class="timeline-title">{event['title']}</h3>
                <p class="timeline-description">{event['description']}</p>
            </div>
        </div>
        """
    
    timeline_html += '</div>'
    
    st.markdown(timeline_html, unsafe_allow_html=True)


def download_lottie_animations():
    """
    Download and cache Lottie animations
    """
    # Create animations directory if it doesn't exist
    Path("assets/animations").mkdir(exist_ok=True, parents=True)
    
    # List of animations to download
    animations = [
        {
            "name": "cloud_computing",
            "url": "https://assets5.lottiefiles.com/packages/lf20_rjn0esjh.json"
        },
        {
            "name": "cloud_security",
            "url": "https://assets5.lottiefiles.com/packages/lf20_q77qtrkv.json"
        },
        {
            "name": "data_analytics",
            "url": "https://assets5.lottiefiles.com/packages/lf20_qp1q7sce.json"
        },
        {
            "name": "cloud_migration",
            "url": "https://assets5.lottiefiles.com/packages/lf20_yd8fbnml.json"
        },
        {
            "name": "success",
            "url": "https://assets5.lottiefiles.com/packages/lf20_atippmse.json"
        }
    ]
    
    # Download animations
    for animation in animations:
        file_path = f"assets/animations/{animation['name']}.json"
        if not os.path.exists(file_path):
            try:
                lottie_json = load_lottieurl(animation["url"])
                if lottie_json:
                    with open(file_path, "w") as f:
                        json.dump(lottie_json, f)
            except Exception as e:
                print(f"Error downloading animation {animation['name']}: {e}")

def show_home_page():
    """
    Display the home page content
    """
    # Hero section with animation
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="hero-text">
            <h1>Transform Your Business with Cloud Innovation</h1>
            <p>CloudSphere delivers cutting-edge cloud solutions that drive digital transformation and business growth.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Call-to-action buttons with hover effects
        st.markdown("""
        <div class="cta-container">
            <button class="cta-button primary">Get Started</button>
            <button class="cta-button secondary">Learn More</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Load Lottie animation
        if os.path.exists("assets/animations/cloud_computing.json"):
            lottie_json = load_lottiefile("assets/animations/cloud_computing.json")
            st_lottie.st_lottie(lottie_json, height=400, key="hero_animation", speed=1, loop=True, quality="high")
        else:
            # Fallback to URL if file doesn't exist
            lottie_url = "https://assets5.lottiefiles.com/packages/lf20_rjn0esjh.json"
            lottie_json = load_lottieurl(lottie_url)
            if lottie_json:
                st_lottie.st_lottie(lottie_json, height=400, key="hero_animation", speed=1, loop=True, quality="high")
    
    # Wave divider
    wave_divider()
    
    # Why Choose Us section
    st.markdown("<h2 class='section-title'>Why Choose CloudSphere?</h2>", unsafe_allow_html=True)
    
    # Animated stats counters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        number_counter(0, 500, suffix="+", duration=2000)
        st.markdown("""
        <div style="text-align: center; margin-top: -20px;">
            <div class="stat-label">Clients Worldwide</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        number_counter(0, 1200, suffix="+", duration=2500)
        st.markdown("""
        <div style="text-align: center; margin-top: -20px;">
            <div class="stat-label">Projects Completed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        number_counter(0, 40, suffix="%", duration=1800)
        st.markdown("""
        <div style="text-align: center; margin-top: -20px;">
            <div class="stat-label">Average Cost Savings</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        number_counter(0, 50, suffix="+", duration=1500)
        st.markdown("""
        <div style="text-align: center; margin-top: -20px;">
            <div class="stat-label">Cloud Experts</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Wave divider
    wave_divider()
    
    # Featured services preview
    st.markdown("<h2 class='section-title'>Our Services</h2>", unsafe_allow_html=True)
    
    # Service cards with animations
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        animated_card_reveal(
            "Cloud Migration",
            "Seamlessly transition your infrastructure to the cloud with our expert migration services.",
            "☁️"
        )
    
    with col2:
        animated_card_reveal(
            "Cloud Security",
            "Protect your cloud assets with our comprehensive security solutions and best practices.",
            "🔒"
        )
    
    with col3:
        animated_card_reveal(
            "Cloud Analytics",
            "Unlock the power of your data with our advanced cloud analytics and visualization tools.",
            "📊"
        )
    
    # Wave divider
    wave_divider()
    
    # Testimonials section with carousel effect
    st.markdown("<h2 class='section-title'>What Our Clients Say</h2>", unsafe_allow_html=True)
    
    # Testimonial carousel using hydralit components
    testimonials = [
        {
            "name": "Sarah Johnson",
            "position": "CTO, TechVision Inc.",
            "image": "https://randomuser.me/api/portraits/women/1.jpg",
            "text": "CloudSphere transformed our IT infrastructure, reducing costs by 35% while improving performance. Their team's expertise was invaluable throughout our digital transformation journey."
        },
        {
            "name": "Michael Chen",
            "position": "Director of IT, Global Retail Solutions",
            "image": "https://randomuser.me/api/portraits/men/2.jpg",
            "text": "The cloud migration strategy developed by CloudSphere helped us modernize our legacy systems with zero downtime. Their ongoing support has been exceptional."
        },
        {
            "name": "Emily Rodriguez",
            "position": "VP of Operations, FinTech Innovations",
            "image": "https://randomuser.me/api/portraits/women/3.jpg",
            "text": "CloudSphere's security solutions gave us peace of mind during our multi-cloud deployment. Their team's proactive approach to compliance saved us countless hours."
        }
    ]
    
    testimonial_cards = []
    for t in testimonials:
        testimonial_cards.append(
            hc.info_card(
                title=t["name"],
                content=t["text"],
                image=t["image"],
                sentiment="good",
                bar_value=100,
                key=t["name"]
            )
        )
    
    # Display testimonials in a carousel
    with st.container():
        st.write("")
        carousel_testimonials = hc.carousel_items(testimonial_cards, height=250)
    
    # Wave divider
    wave_divider()
    
    # Our expertise section
    st.markdown("<h2 class='section-title'>Our Expertise</h2>", unsafe_allow_html=True)
    
    # Skill bars
    skill_bars()
    
    # Wave divider
    wave_divider()
    
    # Call to action section
    st.markdown("""
    <div style="text-align: center; animation: fadeInUp 1s ease-in-out;">
        <h2>Ready to Transform Your Cloud Infrastructure?</h2>
        <p style="margin-bottom: 30px;">Get in touch with our experts today and discover how we can help your business thrive in the cloud.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <button class="cta-button primary" style="font-size: 1.2rem; padding: 15px 30px;">Schedule a Consultation</button>
        </div>
        """, unsafe_allow_html=True)

def show_services_page():
    """
    Display the services page content
    """
    st.markdown("<h1 class='page-title'>Our Cloud Services</h1>", unsafe_allow_html=True)
    
    # Service categories with tabs
    tabs = hc.tab_bar(["Cloud Strategy", "Cloud Migration", "Cloud Security", "Cloud Optimization", "Cloud Analytics"], 
                      icons=["cloud-check", "arrow-right-circle", "shield-check", "gear", "graph-up"], 
                      default_choice="Cloud Strategy")
    
    if tabs == "Cloud Strategy":
        show_cloud_strategy()
    elif tabs == "Cloud Migration":
        show_cloud_migration()
    elif tabs == "Cloud Security":
        show_cloud_security()
    elif tabs == "Cloud Optimization":
        show_cloud_optimization()
    elif tabs == "Cloud Analytics":
        show_cloud_analytics()

def show_cloud_strategy():
    """
    Display the cloud strategy service content
    """
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="service-detail">
            <h2>Cloud Strategy & Consulting</h2>
            <p>Our expert consultants work with you to develop a comprehensive cloud strategy aligned with your business goals.</p>
            <ul class="service-features">
                <li>Cloud Readiness Assessment</li>
                <li>Multi-Cloud Strategy Development</li>
                <li>Cloud Governance Framework</li>
                <li>ROI Analysis & Business Case Development</li>
                <li>Cloud Roadmap Planning</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Timeline of strategy development process
        st.markdown("<h3 style='margin-top: 30px;'>Our Strategy Development Process</h3>", unsafe_allow_html=True)
        
        timeline_events = [
            {
                "date": "Week 1",
                "title": "Discovery & Assessment",
                "description": "We analyze your current infrastructure, applications, and business requirements."
            },
            {
                "date": "Week 2-3",
                "title": "Strategy Development",
                "description": "Our team develops a tailored cloud strategy aligned with your business objectives."
            },
            {
                "date": "Week 4",
                "title": "Roadmap Creation",
                "description": "We create a detailed implementation roadmap with clear milestones and timelines."
            },
            {
                "date": "Week 5-6",
                "title": "Implementation Planning",
                "description": "Detailed planning for the execution phase, including resource allocation and risk mitigation."
            }
        ]
        
        animated_timeline(timeline_events)
    
    with col2:
        # Load Lottie animation
        if os.path.exists("assets/animations/cloud_computing.json"):
            lottie_json = load_lottiefile("assets/animations/cloud_computing.json")
            st_lottie.st_lottie(lottie_json, height=300, key="strategy_animation", speed=1, loop=True, quality="high")
        
        # Strategy visualization
        fig = go.Figure(go.Sunburst(
            labels=["Cloud Strategy", "Assessment", "Planning", "Governance", "Implementation", "Optimization",
                   "Technical", "Business", "Security", "Roadmap", "Architecture", "Training", "Support"],
            parents=["", "Cloud Strategy", "Cloud Strategy", "Cloud Strategy", "Cloud Strategy", "Cloud Strategy",
                    "Assessment", "Assessment", "Planning", "Planning", "Implementation", "Implementation", "Optimization"],
            values=[10, 5, 5, 5, 5, 5, 2, 3, 2, 3, 2, 3, 5],
            branchvalues="total",
            marker=dict(
                colors=["#1E88E5", "#42A5F5", "#64B5F6", "#90CAF9", "#BBDEFB", "#E3F2FD",
                       "#0D47A1", "#1565C0", "#1976D2", "#1E88E5", "#2196F3", "#42A5F5", "#64B5F6"],
                line=dict(color='#FFFFFF', width=1)
            ),
        ))
        
        fig.update_layout(
            margin=dict(t=0, l=0, r=0, b=0),
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Case study preview
        tilt_card(
            "Success Story: Global Financial Institution",
            "We helped a leading financial institution develop a comprehensive cloud strategy that reduced their IT costs by 40% while improving security and compliance.",
            "https://images.unsplash.com/photo-1563986768609-322da13575f3?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
        )

def show_cloud_migration():
    """
    Display the cloud migration service content
    """
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="service-detail">
            <h2>Cloud Migration Services</h2>
            <p>Our cloud migration experts help you seamlessly transition your applications and infrastructure to the cloud with minimal disruption.</p>
            <ul class="service-features">
                <li>Application Portfolio Assessment</li>
                <li>Migration Strategy & Planning</li>
                <li>Lift & Shift Migration</li>
                <li>Re-platforming & Modernization</li>
                <li>Data Migration & Validation</li>
                <li>Post-Migration Support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Load Lottie animation
        if os.path.exists("assets/animations/cloud_migration.json"):
            lottie_json = load_lottiefile("assets/animations/cloud_migration.json")
            st_lottie.st_lottie(lottie_json, height=300, key="migration_animation", speed=1, loop=True, quality="high")
        
        # Migration approach visualization
        migration_data = pd.DataFrame({
            'Approach': ['Rehost', 'Replatform', 'Refactor', 'Repurchase', 'Retire', 'Retain'],
            'Complexity': [2, 4, 8, 5, 1, 1],
            'Business Value': [3, 6, 9, 7, 2, 1]
        })
        
        fig = px.scatter(
            migration_data, 
            x='Complexity', 
            y='Business Value', 
            size='Complexity', 
            color='Approach',
            size_max=20,
            color_discrete_sequence=px.colors.sequential.Blues_r,
            labels={'Complexity': 'Implementation Complexity', 'Business Value': 'Business Value'},
            title='Cloud Migration Approaches'
        )
        
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(17,34,64,0.3)',
            font=dict(color='white'),
            title_font_color='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_cloud_security():
    """
    Display the cloud security service content
    """
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="service-detail">
            <h2>Cloud Security Services</h2>
            <p>Our comprehensive cloud security solutions help you protect your cloud infrastructure, applications, and data from evolving threats.</p>
            <ul class="service-features">
                <li>Cloud Security Assessment</li>
                <li>Security Architecture Design</li>
                <li>Identity & Access Management</li>
                <li>Data Protection & Encryption</li>
                <li>Threat Detection & Response</li>
                <li>Compliance Management</li>
                <li>Security Monitoring & Reporting</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Load Lottie animation
        if os.path.exists("assets/animations/cloud_security.json"):
            lottie_json = load_lottiefile("assets/animations/cloud_security.json")
            st_lottie.st_lottie(lottie_json, height=300, key="security_animation", speed=1, loop=True, quality="high")
        
        # Security framework visualization
        security_data = {
            'Category': ['Identity', 'Network', 'Data', 'Applications', 'Monitoring', 'Compliance'],
            'Implementation': [85, 90, 95, 80, 88, 92]
        }
        
        df = pd.DataFrame(security_data)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=df['Implementation'],
            theta=df['Category'],
            fill='toself',
            line=dict(color='#1E88E5'),
            fillcolor='rgba(30, 136, 229, 0.3)',
            name='Security Framework'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_cloud_optimization():
    """
    Display the cloud optimization service content
    """
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="service-detail">
            <h2>Cloud Optimization Services</h2>
            <p>Our cloud optimization services help you maximize the performance and cost-efficiency of your cloud environment.</p>
            <ul class="service-features">
                <li>Cost Optimization Analysis</li>
                <li>Resource Rightsizing</li>
                <li>Reserved Instance Planning</li>
                <li>Performance Optimization</li>
                <li>Automated Scaling Solutions</li>
                <li>Multi-Cloud Management</li>
                <li>FinOps Implementation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Cost savings visualization
        st.markdown("<h3 style='margin-top: 30px;'>Typical Cost Savings</h3>", unsafe_allow_html=True)
        
        optimization_data = {
            'Category': ['Resource Rightsizing', 'Reserved Instances', 'Storage Optimization', 'Unused Resources', 'Licensing Optimization'],
            'Savings': [25, 40, 30, 20, 15]
        }
        
        df = pd.DataFrame(optimization_data)
        
        fig = px.bar(
            df, 
            x='Category', 
            y='Savings',
            color='Savings',
            color_continuous_scale=px.colors.sequential.Blues,
            labels={'Savings': 'Average Savings (%)'},
            text='Savings'
        )
        
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        
        fig.update_layout(
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(17,34,64,0.3)',
            font=dict(color='white'),
            coloraxis_showscale=False,
            xaxis=dict(title=''),
            yaxis=dict(title='Average Savings (%)')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Optimization process visualization
        st.markdown("<h3>Our Optimization Process</h3>", unsafe_allow_html=True)
        
        # Animated process steps
        steps = [
            {"title": "Assessment", "description": "Comprehensive analysis of your current cloud environment and spending patterns."},
            {"title": "Recommendations", "description": "Detailed recommendations for cost and performance optimization."},
            {"title": "Implementation", "description": "Execution of optimization strategies with minimal disruption."},
            {"title": "Automation", "description": "Implementation of automated scaling and optimization tools."},
            {"title": "Monitoring", "description": "Continuous monitoring and refinement of optimization strategies."}
        ]
        
        for i, step in enumerate(steps):
            st.markdown(f"""
            <div class="process-step" style="animation-delay: {i * 0.2}s;">
                <div class="process-number">{i+1}</div>
                <div class="process-content">
                    <h4>{step['title']}</h4>
                    <p>{step['description']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # ROI calculator
        st.markdown("<h3 style='margin-top: 30px;'>Cloud Optimization ROI Calculator</h3>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("""
            <div style="background: rgba(17, 34, 64, 0.6); border-radius: 10px; padding: 20px; border: 1px solid rgba(30, 136, 229, 0.2);">
                <p style="color: #e0e0e0;">Estimate your potential savings with our cloud optimization services.</p>
            </div>
            """, unsafe_allow_html=True)
            
            current_spend = st.slider("Current Monthly Cloud Spend ($)", 1000, 100000, 10000, step=1000)
            
            # Calculate estimated savings
            total_savings = current_spend * 0.35
            
            # Display results
            st.markdown(f"""
            <div style="background: rgba(17, 34, 64, 0.6); border-radius: 10px; padding: 20px; border: 1px solid rgba(30, 136, 229, 0.2); margin-top: 20px; animation: fadeInUp 1s ease-in-out;">
                <h4 style="color: #ffffff; margin-bottom: 15px;">Estimated Annual Savings</h4>
                <div style="color: #1E88E5; font-size: 2rem; font-weight: bold; margin-bottom: 15px;">${total_savings * 12:,.2f}</div>
                <p style="color: #e0e0e0;">Based on industry averages, our optimization services could help you save approximately 35% on your cloud spending.</p>
            </div>
            """, unsafe_allow_html=True)

def show_cloud_analytics():
    """
    Display the cloud analytics service content
    """
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="service-detail">
            <h2>Cloud Analytics Services</h2>
            <p>Our cloud analytics services help you harness the power of your data to gain valuable insights and drive business decisions.</p>
            <ul class="service-features">
                <li>Data Warehouse Implementation</li>
                <li>Business Intelligence Solutions</li>
                <li>Big Data Processing</li>
                <li>Machine Learning & AI Integration</li>
                <li>Real-time Analytics</li>
                <li>Data Visualization</li>
                <li>Predictive Analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Load Lottie animation
        if os.path.exists("assets/animations/data_analytics.json"):
            lottie_json = load_lottiefile("assets/animations/data_analytics.json")
            st_lottie.st_lottie(lottie_json, height=300, key="analytics_animation", speed=1, loop=True, quality="high")
        
        # Analytics capabilities visualization
        st.markdown("<h3>Our Analytics Capabilities</h3>", unsafe_allow_html=True)
        
        # Sample data for visualization
        np.random.seed(42)
        dates = pd.date_range(start='2023-01-01', periods=90, freq='D')
        data = np.cumsum(np.random.randn(90)) + 50
        trend = np.linspace(0, 15, 90)
        data = data + trend
        
        df = pd.DataFrame({
            'Date': dates,
            'Value': data
        })
        
        # Create interactive chart
        fig = px.line(
            df, 
            x='Date', 
            y='Value',
            labels={'Value': 'Performance Metric', 'Date': 'Time Period'},
            title='Interactive Data Visualization Example'
        )
        
        # Add prediction area
        future_dates = pd.date_range(start=dates[-1] + pd.Timedelta(days=1), periods=30, freq='D')
        last_value = data[-1]
        slope = (data[-1] - data[-30]) / 30
        future_values = [last_value + slope * (i+1) + np.random.randn() * 2 for i in range(30)]
        
        fig.add_trace(
            go.Scatter(
                x=future_dates,
                y=future_values,
                mode='lines',
                line=dict(color='rgba(100, 181, 246, 0.8)', dash='dash'),
                name='Prediction'
            )
        )
        
        # Add confidence interval
        upper_bound = [v + 5 for v in future_values]
        lower_bound = [v - 5 for v in future_values]
        
        fig.add_trace(
            go.Scatter(
                x=future_dates.tolist() + future_dates.tolist()[::-1],
                y=upper_bound + lower_bound[::-1],
                fill='toself',
                fillcolor='rgba(100, 181, 246, 0.2)',
                line=dict(color='rgba(0,0,0,0)'),
                name='Confidence Interval'
            )
        )
        
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(17,34,64,0.3)',
            font=dict(color='white'),
            title_font_color='white',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_case_studies_page():
    """
    Display the case studies page content
    """
    st.markdown("<h1 class='page-title'>Case Studies</h1>", unsafe_allow_html=True)
    
    # Filter options
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        industry = st.selectbox("Industry", ["All Industries", "Finance", "Healthcare", "Retail", "Manufacturing", "Technology"])
    
    with col2:
        service = st.selectbox("Service Type", ["All Services", "Cloud Migration", "Cloud Security", "Cloud Optimization", "Cloud Analytics"])
    
    with col3:
        sort_by = st.selectbox("Sort By", ["Most Recent", "Most Popular", "ROI Impact"])
    
    # Case study cards with animation delay for staggered appearance
    case_studies = [
        {
            "title": "Global Bank Reduces Infrastructure Costs by 40%",
            "industry": "Finance",
            "service": "Cloud Migration",
            "image": "https://images.unsplash.com/photo-1563986768609-322da13575f3?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "description": "A leading global bank transformed their legacy infrastructure with our cloud migration strategy, achieving 40% cost reduction and improved performance."
        },
        {
            "title": "Healthcare Provider Enhances Data Security",
            "industry": "Healthcare",
            "service": "Cloud Security",
            "image": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "description": "A major healthcare provider implemented our comprehensive cloud security solution to protect sensitive patient data while maintaining compliance."
        },
        {
            "title": "Retail Chain Optimizes Multi-Cloud Environment",
            "industry": "Retail",
            "service": "Cloud Optimization",
            "image": "https://images.unsplash.com/photo-1534452203293-494d7ddbf7e0?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "description": "A national retail chain optimized their multi-cloud environment, reducing operational overhead by 30% and improving application performance."
        },
        {
            "title": "Manufacturing Company Leverages IoT Analytics",
            "industry": "Manufacturing",
            "service": "Cloud Analytics",
            "image": "https://images.unsplash.com/photo-1507646227500-4d389b0012be?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "description": "A global manufacturing company implemented our IoT analytics solution to monitor equipment performance and predict maintenance needs."
        },
        {
            "title": "Tech Startup Scales Infrastructure Seamlessly",
            "industry": "Technology",
            "service": "Cloud Migration",
            "image": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "description": "A fast-growing tech startup migrated to a scalable cloud infrastructure that supported their rapid growth without service disruptions."
        },
        {
            "title": "Financial Services Firm Achieves Compliance",
            "industry": "Finance",
            "service": "Cloud Security",
            "image": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "description": "A financial services firm implemented our cloud security framework to achieve regulatory compliance while improving operational efficiency."
        }
    ]
    
    # Filter case studies based on selection
    filtered_studies = case_studies
    if industry != "All Industries":
        filtered_studies = [cs for cs in filtered_studies if cs["industry"] == industry]
    if service != "All Services":
        filtered_studies = [cs for cs in filtered_studies if cs["service"] == service]
    
    # Display case studies with animation delay
    if not filtered_studies:
        st.markdown("""
        <div style="text-align: center; padding: 50px; background: rgba(17, 34, 64, 0.6); border-radius: 10px; animation: fadeIn 1s ease-in-out;">
            <h3>No case studies match your filter criteria</h3>
            <p>Please try different filter options.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i in range(0, len(filtered_studies), 2):
            col1, col2 = st.columns(2, gap="large")
            
            with col1:
                if i < len(filtered_studies):
                    cs = filtered_studies[i]
                    st.markdown(f"""
                    <div class="case-study-card" style="animation-delay: {i * 0.2}s;">
                        <div class="case-study-image" style="background-image: url('{cs["image"]}');">
                            <div class="case-study-overlay">
                                <span class="case-study-tag">{cs["industry"]}</span>
                                <span class="case-study-tag">{cs["service"]}</span>
                            </div>
                        </div>
                        <div class="case-study-content">
                            <h3>{cs["title"]}</h3>
                            <p>{cs["description"]}</p>
                            <div class="case-study-link">Read Full Case Study →</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                if i + 1 < len(filtered_studies):
                    cs = filtered_studies[i + 1]
                    st.markdown(f"""
                    <div class="case-study-card" style="animation-delay: {(i+1) * 0.2}s;">
                        <div class="case-study-image" style="background-image: url('{cs["image"]}');">
                            <div class="case-study-overlay">
                                <span class="case-study-tag">{cs["industry"]}</span>
                                <span class="case-study-tag">{cs["service"]}</span>
                            </div>
                        </div>
                        <div class="case-study-content">
                            <h3>{cs["title"]}</h3>
                            <p>{cs["description"]}</p>
                            <div class="case-study-link">Read Full Case Study →</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

def show_team_page():
    """
    Display the team page content
    """
    st.markdown("<h1 class='page-title'>Our Team</h1>", unsafe_allow_html=True)
    
    # Team introduction
    st.markdown("""
    <div class="team-intro">
        <h2>Meet the Experts Behind CloudSphere</h2>
        <p>Our team of cloud specialists brings decades of combined experience in cloud architecture, security, and optimization to help your business thrive in the digital era.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Leadership team with animated cards
    st.markdown("<h2 class='section-title'>Leadership Team</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div class="team-card" style="animation-delay: 0.2s;">
            <div class="team-image" style="background-image: url('https://randomuser.me/api/portraits/men/32.jpg');"></div>
            <h3>David Mitchell</h3>
            <div class="team-position">CEO & Founder</div>
            <p>Former AWS Solutions Architect with 15+ years of experience in cloud technologies and digital transformation.</p>
            <div class="team-social">
                <span>LinkedIn</span>
                <span>Twitter</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="team-card" style="animation-delay: 0.4s;">
            <div class="team-image" style="background-image: url('https://randomuser.me/api/portraits/women/44.jpg');"></div>
            <h3>Jennifer Lee</h3>
            <div class="team-position">CTO</div>
            <p>Cloud architecture expert with background in Google Cloud and Microsoft Azure. Led cloud transformations for Fortune 500 companies.</p>
            <div class="team-social">
                <span>LinkedIn</span>
                <span>Twitter</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="team-card" style="animation-delay: 0.6s;">
            <div class="team-image" style="background-image: url('https://randomuser.me/api/portraits/men/22.jpg');"></div>
            <h3>Robert Garcia</h3>
            <div class="team-position">VP of Cloud Security</div>
            <p>Certified security expert with specialization in cloud security frameworks and compliance standards across industries.</p>
            <div class="team-social">
                <span>LinkedIn</span>
                <span>Twitter</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Cloud experts
    st.markdown("<h2 class='section-title'>Our Cloud Experts</h2>", unsafe_allow_html=True)
    
    # Expert categories with tabs
    expert_tabs = hc.tab_bar(["Cloud Architects", "Security Specialists", "Data Engineers", "DevOps Engineers"], 
                      icons=["building", "shield", "database", "gear"], 
                      default_choice="Cloud Architects")
    
    if expert_tabs == "Cloud Architects":
        # Display cloud architects with staggered animation
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="expert-card" style="animation-delay: 0.2s;">
                <div class="expert-image" style="background-image: url('https://randomuser.me/api/portraits/women/28.jpg');"></div>
                <h4>Sophia Williams</h4>
                <div class="expert-specialty">AWS Specialist</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="expert-card" style="animation-delay: 0.4s;">
                <div class="expert-image" style="background-image: url('https://randomuser.me/api/portraits/men/45.jpg');"></div>
                <h4>James Chen</h4>
                <div class="expert-specialty">Azure Architect</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="expert-card" style="animation-delay: 0.6s;">
                <div class="expert-image" style="background-image: url('https://randomuser.me/api/portraits/women/36.jpg');"></div>
                <h4>Olivia Martinez</h4>
                <div class="expert-specialty">GCP Specialist</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="expert-card" style="animation-delay: 0.8s;">
                <div class="expert-image" style="background-image: url('https://randomuser.me/api/portraits/men/57.jpg');"></div>
                <h4>Daniel Kim</h4>
                <div class="expert-specialty">Multi-Cloud Architect</div>
            </div>
            """, unsafe_allow_html=True)
    
    elif expert_tabs == "Security Specialists":
        # Display security specialists
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="expert-card" style="animation-delay: 0.2s;">
                <div class="expert-image" style="background-image: url('https://randomuser.me/api/portraits/men/33.jpg');"></div>
                <h4>Michael Johnson</h4>
                <div class="expert-specialty">Security Architect</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="expert-card" style="animation-delay: 0.4s;">
                <div class="expert-image" style="background-image: url('https://randomuser.me/api/portraits/women/54.jpg');"></div>
                <h4>Emily Rodriguez</h4>
                <div class="expert-specialty">Compliance Specialist</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="expert-card" style="animation-delay: 0.6s;">
                <div class="expert-image" style="background-image: url('https://randomuser.me/api/portraits/men/76.jpg');"></div>
                <h4>Thomas Wilson</h4>
                <div class="expert-specialty">Threat Intelligence</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="expert-card" style="animation-delay: 0.8s;">
                <div class="expert-image" style="background-image: url('https://randomuser.me/api/portraits/women/67.jpg');"></div>
                <h4>Sarah Thompson</h4>
                <div class="expert-specialty">Identity Management</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Team culture section with animated elements
    st.markdown("<h2 class='section-title' style='margin-top: 50px;'>Our Team Culture</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div style="animation: fadeInLeft 1s ease-in-out;">
            <h3>What Makes Us Different</h3>
            <p>At CloudSphere, we believe that our team culture is the foundation of our success. We foster an environment of continuous learning, collaboration, and innovation.</p>
            
            <div class="culture-value">
                <h4>Expertise</h4>
                <p>Our team consists of certified cloud experts with extensive experience across all major cloud platforms.</p>
            </div>
            
            <div class="culture-value">
                <h4>Client-Centric Approach</h4>
                <p>We prioritize understanding our clients' unique business needs to deliver tailored cloud solutions.</p>
            </div>
            
            <div class="culture-value">
                <h4>Innovation</h4>
                <p>We continuously explore emerging technologies and best practices to provide cutting-edge solutions.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Team stats with animated counters
        st.markdown("""
        <div style="background: rgba(17, 34, 64, 0.6); border-radius: 10px; padding: 25px; border: 1px solid rgba(30, 136, 229, 0.2); animation: fadeInRight 1s ease-in-out;">
            <h3 style="text-align: center; margin-bottom: 20px;">Team by the Numbers</h3>
            
            <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
                <div style="text-align: center;">
                    <div class="stat-number" id="team-size">50+</div>
                    <div class="stat-label">Team Members</div>
                </div>
                
                <div style="text-align: center;">
                    <div class="stat-number" id="certifications">200+</div>
                    <div class="stat-label">Cloud Certifications</div>
                </div>
            </div>
            
            <div style="display: flex; justify-content: space-between;">
                <div style="text-align: center;">
                    <div class="stat-number" id="experience">12+</div>
                    <div class="stat-label">Avg. Years Experience</div>
                </div>
                
                <div style="text-align: center;">
                    <div class="stat-number" id="countries">15+</div>
                    <div class="stat-label">Countries</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Team values visualization
        st.markdown("<h3 style='margin-top: 30px;'>Our Values</h3>", unsafe_allow_html=True)
        
        values_data = {
            'Value': ['Excellence', 'Innovation', 'Integrity', 'Collaboration', 'Client Focus'],
            'Score': [95, 90, 100, 85, 95]
        }
        
        df = pd.DataFrame(values_data)
        
        fig = px.bar(
            df, 
            x='Value', 
            y='Score',
            color='Score',
            color_continuous_scale=px.colors.sequential.Blues,
            labels={'Score': 'Importance'},
            text='Score'
        )
        
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        
        fig.update_layout(
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(17,34,64,0.3)',
            font=dict(color='white'),
            coloraxis_showscale=False,
            xaxis=dict(title=''),
            yaxis=dict(title='', range=[0, 110])
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_contact_page():
    """
    Display the contact page content
    """
    st.markdown("<h1 class='page-title'>Contact Us</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="contact-info">
            <h2>Get in Touch</h2>
            <p>Ready to transform your business with cloud technology? Our team of experts is here to help you navigate your cloud journey.</p>
            
            <div class="contact-method">
                <div class="contact-icon">📍</div>
                <div class="contact-text">
                    <h4>Visit Us</h4>
                    <p>123 Tech Plaza, Suite 500<br>San Francisco, CA 94105</p>
                </div>
            </div>
            
            <div class="contact-method">
                <div class="contact-icon">📞</div>
                <div class="contact-text">
                    <h4>Call Us</h4>
                    <p>+1 (555) 123-4567</p>
                </div>
            </div>
            
            <div class="contact-method">
                <div class="contact-icon">✉️</div>
                <div class="contact-text">
                    <h4>Email Us</h4>
                    <p>info@cloudsphere.tech</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Global presence map
        st.markdown("<h3 style='margin-top: 30px;'>Our Global Presence</h3>", unsafe_allow_html=True)
        
        # Sample data for office locations
        locations = pd.DataFrame({
            'city': ['San Francisco', 'New York', 'London', 'Singapore', 'Sydney', 'Tokyo'],
            'lat': [37.7749, 40.7128, 51.5074, 1.3521, -33.8688, 35.6762],
            'lon': [-122.4194, -74.0060, -0.1278, 103.8198, 151.2093, 139.6503],
            'size': [20, 15, 15, 12, 10, 10]
        })
        
        fig = px.scatter_geo(
            locations,
            lat='lat',
            lon='lon',
            size='size',
            text='city',
            color_discrete_sequence=['#1E88E5'],
            projection='natural earth'
        )
        
        fig.update_traces(
            marker=dict(
                line=dict(width=1, color='#ffffff'),
                sizemode='diameter',
                sizemin=5
            ),
            selector=dict(mode='markers+text'),
            textposition='bottom center'
        )
        
        fig.update_layout(
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            geo=dict(
                showland=True,
                landcolor='rgba(17, 34, 64, 0.6)',
                countrycolor='rgba(30, 136, 229, 0.3)',
                coastlinecolor='rgba(30, 136, 229, 0.5)',
                showocean=True,
                oceancolor='rgba(17, 34, 64, 0.8)',
                showlakes=False,
                showrivers=False,
                showcountries=True,
                bgcolor='rgba(0,0,0,0)'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Contact form with animation
        st.markdown("<div class='contact-form-container'>", unsafe_allow_html=True)
        st.markdown("<h2>Send Us a Message</h2>", unsafe_allow_html=True)
        
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        company = st.text_input("Company Name")
        service = st.selectbox("Service of Interest", ["Cloud Strategy", "Cloud Migration", "Cloud Security", "Cloud Optimization", "Cloud Analytics", "Other"])
        message = st.text_area("Your Message")
        
        # Submit button with animation
        if st.button("Send Message", key="contact_submit"):
            # Simulate form submission with loading animation
            with st.spinner("Sending your message..."):
                time.sleep(2)
                
                # Load success animation
                if os.path.exists("assets/animations/success.json"):
                    lottie_json = load_lottiefile("assets/animations/success.json")
                    st_lottie.st_lottie(lottie_json, height=200, key="success_animation", speed=1, loop=False, quality="high")
                
                st.success("Message sent successfully! We'll get back to you within 24 hours.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # FAQ section with animated accordion
        st.markdown("<h3 style='margin-top: 30px;'>Frequently Asked Questions</h3>", unsafe_allow_html=True)
        
        faqs = [
            {
                "question": "What cloud platforms do you support?",
                "answer": "We support all major cloud platforms including AWS, Microsoft Azure, Google Cloud Platform, and Oracle Cloud, as well as multi-cloud and hybrid cloud environments."
            },
            {
                "question": "How long does a typical cloud migration take?",
                "answer": "The duration of a cloud migration depends on the complexity and size of your infrastructure. A small to medium-sized migration typically takes 2-3 months, while larger enterprise migrations may take 6-12 months."
            },
            {
                "question": "Do you offer ongoing support after migration?",
                "answer": "Yes, we offer comprehensive managed services and support options to ensure your cloud environment remains optimized, secure, and aligned with your business needs."
            },
            {
                "question": "How do you ensure security during cloud migrations?",
                "answer": "We implement a security-first approach with comprehensive risk assessments, encryption, identity management, and compliance controls throughout the migration process."
            }
        ]
        
        # Create FAQ accordion
        for i, faq in enumerate(faqs):
            with st.expander(faq["question"]):
                st.markdown(f"<p style='color: #e0e0e0;'>{faq['answer']}</p>", unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """
    Main application entry point
    """
    # Load CSS
    if Path("style.css").exists():
        local_css("style.css")
    
    # Add responsive meta tags
    add_responsive_meta_tags()
    
    # Add touch support for mobile devices
    add_touch_support()
    
    # Add responsive styles
    add_responsive_styles()
    
    # Add animation scripts
    add_animation_script()
    add_particles_background()
    
    # Download Lottie animations
    download_lottie_animations()
    
    # Navigation menu with animation
    with st.container():
        selected = option_menu(
            menu_title=None,
            options=["Home", "Services", "Case Studies", "Team", "Contact"],
            icons=["house", "cloud-fill", "briefcase", "people", "envelope"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "rgba(0,0,0,0.8)"},
                "icon": {"color": "#1E88E5", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "center",
                    "margin": "0px",
                    "padding": "10px",
                    "--hover-color": "rgba(30, 136, 229, 0.2)",
                },
                "nav-link-selected": {"background-color": "rgba(30, 136, 229, 0.3)"},
            },
        )
    
    # Content based on selected menu item
    if selected == "Home":
        show_home_page()
    elif selected == "Services":
        show_services_page()
    elif selected == "Case Studies":
        show_case_studies_page()
    elif selected == "Team":
        show_team_page()
    elif selected == "Contact":
        show_contact_page()

# Run the application
if __name__ == "__main__":
    main()
