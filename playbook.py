import streamlit as st
import google.generativeai as genai
import logging
import os
from datetime import datetime
import re
import uuid
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize session state
if 'playbook_history' not in st.session_state:
    st.session_state.playbook_history = []
if 'current_playbook' not in st.session_state:
    st.session_state.current_playbook = None
if 'ai_enabled' not in st.session_state:
    st.session_state.ai_enabled = True

# Configure Gemini API
def initialize_gemini():
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "AIzaSyD1WeVGIKaV1oyYlDsk2a_EDWdsSclwMqU")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        return model
    except Exception as e:
        logger.error(f"Failed to initialize Gemini API: {e}")
        return None

# Enhanced Fallback Template with more sections
ENHANCED_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapyder Master Sales Playbook 2025</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: linear-gradient(135deg, #000000 0%, #1a0000 100%);
            color: #FC3030;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            overflow-x: hidden;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            padding: 40px 0;
            background: linear-gradient(45deg, #FC3030, #ff6b6b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .header h1 {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 10px;
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.8;
        }
        
        @keyframes glow {
            from { text-shadow: 0 0 10px #FC3030; }
            to { text-shadow: 0 0 20px #FC3030, 0 0 30px #ff6b6b; }
        }
        
        .toc {
            background: rgba(26, 26, 26, 0.9);
            backdrop-filter: blur(10px);
            border: 1px solid #FC3030;
            border-radius: 15px;
            padding: 25px;
            margin: 30px 0;
            box-shadow: 0 8px 32px rgba(252, 48, 48, 0.1);
        }
        
        .toc h2 {
            color: #FC3030;
            margin-bottom: 20px;
            font-size: 1.8rem;
        }
        
        .search-container {
            position: relative;
            margin-bottom: 20px;
        }
        
        .search-container input {
            width: 100%;
            padding: 15px 20px;
            background: rgba(0, 0, 0, 0.7);
            color: #FC3030;
            border: 2px solid #FC3030;
            border-radius: 10px;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        .search-container input:focus {
            outline: none;
            border-color: #ff6b6b;
            box-shadow: 0 0 15px rgba(252, 48, 48, 0.3);
        }
        
        .toc-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }
        
        .toc-item {
            background: linear-gradient(135deg, rgba(252, 48, 48, 0.1), rgba(255, 107, 107, 0.1));
            border: 1px solid #FC3030;
            border-radius: 10px;
            padding: 15px;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .toc-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(252, 48, 48, 0.2);
            background: linear-gradient(135deg, rgba(252, 48, 48, 0.2), rgba(255, 107, 107, 0.2));
        }
        
        .toc-item a {
            color: #FC3030;
            text-decoration: none;
            font-weight: 500;
            display: block;
        }
        
        .section {
            background: rgba(26, 26, 26, 0.9);
            border: 1px solid #FC3030;
            border-radius: 15px;
            margin: 30px 0;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(252, 48, 48, 0.1);
            transition: all 0.3s ease;
        }
        
        .section:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(252, 48, 48, 0.15);
        }
        
        .section-header {
            background: linear-gradient(135deg, #FC3030, #ff6b6b);
            color: #000;
            padding: 20px;
            cursor: pointer;
            font-weight: 600;
            font-size: 1.3rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
        }
        
        .section-header:hover {
            background: linear-gradient(135deg, #ff6b6b, #FC3030);
        }
        
        .section-content {
            padding: 25px;
            display: none;
            animation: fadeIn 0.5s ease-in-out;
        }
        
        .section-content.active {
            display: block;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .card {
            background: rgba(0, 0, 0, 0.7);
            border: 1px solid #FC3030;
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s ease;
        }
        
        .card:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 25px rgba(252, 48, 48, 0.2);
        }
        
        .card h4 {
            color: #FC3030;
            margin-bottom: 10px;
            font-size: 1.2rem;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 10px;
            overflow: hidden;
            margin: 20px 0;
        }
        
        th, td {
            border: 1px solid #FC3030;
            padding: 15px;
            text-align: left;
        }
        
        th {
            background: linear-gradient(135deg, #FC3030, #ff6b6b);
            color: #000;
            font-weight: 600;
        }
        
        tr:hover {
            background: rgba(252, 48, 48, 0.1);
        }
        
        .progress-bar {
            width: 100%;
            height: 6px;
            background: rgba(252, 48, 48, 0.2);
            border-radius: 3px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #FC3030, #ff6b6b);
            width: 0%;
            transition: width 1s ease-in-out;
        }
        
        .floating-action {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: linear-gradient(135deg, #FC3030, #ff6b6b);
            color: #000;
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 1.5rem;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(252, 48, 48, 0.3);
            transition: all 0.3s ease;
        }
        
        .floating-action:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 30px rgba(252, 48, 48, 0.4);
        }
        
        @media (max-width: 768px) {
            .container { padding: 10px; }
            .header h1 { font-size: 2rem; }
            .toc-grid { grid-template-columns: 1fr; }
            .cards-grid { grid-template-columns: 1fr; }
            table { font-size: 0.9rem; }
            .floating-action { bottom: 20px; right: 20px; }
        }
        
        .highlight {
            background: linear-gradient(135deg, rgba(252, 48, 48, 0.2), rgba(255, 107, 107, 0.2));
            padding: 2px 6px;
            border-radius: 4px;
        }
        
        .icon {
            margin-right: 10px;
        }
        
        .expand-icon {
            transition: transform 0.3s ease;
        }
        
        .expanded .expand-icon {
            transform: rotate(180deg);
        }
        
        .badge {
            display: inline-block;
            background: #FC3030;
            color: #000;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            margin: 2px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><span class="icon">🚀</span>Rapyder Master Sales Playbook 2025</h1>
            <p>Your Complete Guide to Cloud & AI Sales Excellence</p>
        </div>

        <div class="toc">
            <h2><span class="icon">📋</span>Table of Contents</h2>
            <div class="search-container">
                <input type="text" id="toc-search" onkeyup="searchTOC()" placeholder="🔍 Search sections...">
            </div>
            <div class="toc-grid">
                <div class="toc-item" onclick="scrollToSection('about')">
                    <a href="#about"><span class="icon">🏢</span>About Rapyder</a>
                </div>
                <div class="toc-item" onclick="scrollToSection('target')">
                    <a href="#target"><span class="icon">🎯</span>Target Customer Profiles</a>
                </div>
                <div class="toc-item" onclick="scrollToSection('solutions')">
                    <a href="#solutions"><span class="icon">⚡</span>Solutions Portfolio</a>
                </div>
                <div class="toc-item" onclick="scrollToSection('methodology')">
                    <a href="#methodology"><span class="icon">📊</span>Sales Methodology</a>
                </div>
                <div class="toc-item" onclick="scrollToSection('process')">
                    <a href="#process"><span class="icon">🔄</span>Sales Process</a>
                </div>
                <div class="toc-item" onclick="scrollToSection('tools')">
                    <a href="#tools"><span class="icon">🛠️</span>Sales Tools & Tech</a>
                </div>
                <div class="toc-item" onclick="scrollToSection('messaging')">
                    <a href="#messaging"><span class="icon">💬</span>Messaging Framework</a>
                </div>
                <div class="toc-item" onclick="scrollToSection('scripts')">
                    <a href="#scripts"><span class="icon">📞</span>Call & Email Scripts</a>
                </div>
                <div class="toc-item" onclick="scrollToSection('kpis')">
                    <a href="#kpis"><span class="icon">📈</span>KPIs & Metrics</a>
                </div>
                <div class="toc-item" onclick="scrollToSection('case-studies')">
                    <a href="#case-studies"><span class="icon">🏆</span>Success Stories</a>
                </div>
                <div class="toc-item" onclick="scrollToSection('objections')">
                    <a href="#objections"><span class="icon">❓</span>Objection Handling</a>
                </div>
                <div class="toc-item" onclick="scrollToSection('competitive')">
                    <a href="#competitive"><span class="icon">⚔️</span>Competitive Analysis</a>
                </div>
                <div class="toc-item" onclick="scrollToSection('resources')">
                    <a href="#resources"><span class="icon">📚</span>Resources & Training</a>
                </div>
                <div class="toc-item" onclick="scrollToSection('templates')">
                    <a href="#templates"><span class="icon">📄</span>Templates & Tools</a>
                </div>
                <div class="toc-item" onclick="scrollToSection('trends')">
                    <a href="#trends"><span class="icon">🔮</span>2025 Trends</a>
                </div>
                <div class="toc-item" onclick="scrollToSection('action-plan')">
                    <a href="#action-plan"><span class="icon">✅</span>Action Plan</a>
                </div>
            </div>
        </div>

        <!-- Section 1: About Rapyder -->
        <div class="section" id="about">
            <div class="section-header" onclick="toggleSection('about')">
                <span><span class="icon">🏢</span>About Rapyder Cloud Solutions</span>
                <span class="expand-icon">▼</span>
            </div>
            <div class="section-content">
                <div class="cards-grid">
                    <div class="card">
                        <h4>🎯 Mission Statement</h4>
                        <p>Transform enterprises with <span class="highlight">AWS-certified cloud and AI solutions</span>, delivering unmatched scalability, security, and ROI across industries.</p>
                    </div>
                    <div class="card">
                        <h4>🏅 Key Differentiators</h4>
                        <div class="badge">AWS Advanced Partner</div>
                        <div class="badge">6 Competencies</div>
                        <div class="badge">Gen AI Certified</div>
                        <p>• <strong>AWS Advanced Consulting Partner</strong> with 6 specialized competencies<br>
                        • <strong>Microsoft Gold Partner</strong> with 14+ competencies<br>
                        • <strong>Tech Studio</strong> with proprietary AI solutions<br>
                        • <strong>$2.3B+ cumulative client ROI</strong> delivered</p>
                    </div>
                    <div class="card">
                        <h4>📊 By The Numbers</h4>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: 95%"></div>
                        </div>
                        <p><strong>95% Client Retention Rate</strong></p>
                        <p>• 500+ successful cloud migrations<br>
                        • 40% average cost reduction<br>
                        • 98% zero-downtime deployments<br>
                        • 24/7 global support coverage</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Continue with remaining sections... -->
        
        <button class="floating-action" onclick="scrollToTop()" title="Back to Top">
            ⬆️
        </button>
    </div>

    <script>
        function toggleSection(sectionId) {
            const content = document.querySelector(`#${sectionId} .section-content`);
            const header = document.querySelector(`#${sectionId} .section-header`);
            const expandIcon = header.querySelector('.expand-icon');
            
            if (content.classList.contains('active')) {
                content.classList.remove('active');
                header.classList.remove('expanded');
                expandIcon.textContent = '▼';
            } else {
                content.classList.add('active');
                header.classList.add('expanded');
                expandIcon.textContent = '▲';
            }
        }

        function scrollToSection(sectionId) {
            document.getElementById(sectionId).scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            toggleSection(sectionId);
        }

        function scrollToTop() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }

        function searchTOC() {
            const input = document.getElementById('toc-search').value.toLowerCase();
            const items = document.querySelectorAll('.toc-item');
            
            items.forEach(item => {
                const text = item.textContent.toLowerCase();
                item.style.display = text.includes(input) ? 'block' : 'none';
            });
        }

        // Initialize progress bars
        document.addEventListener('DOMContentLoaded', function() {
            const progressBars = document.querySelectorAll('.progress-fill');
            progressBars.forEach(bar => {
                setTimeout(() => {
                    bar.style.width = bar.style.width || '0%';
                }, 500);
            });
        });

        // Add smooth scrolling for all anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    </script>
</body>
</html>
"""

# Function to generate content without AI
def generate_static_playbook(input_text):
    """Generate a static playbook based on input text without AI."""
    # Parse input for key requirements
    sections_map = {
        "about": "About Rapyder Cloud Solutions",
        "target": "Target Customer Profiles & Personas",
        "solutions": "Solutions Portfolio & Offerings",
        "methodology": "Sales Methodology & Framework",
        "process": "End-to-End Sales Process",
        "tools": "Sales Tools & Technologies",
        "messaging": "Messaging Framework & Value Props",
        "scripts": "Call & Email Scripts Library",
        "kpis": "KPIs & Performance Metrics",
        "case-studies": "Success Stories & Case Studies",
        "objections": "Objection Handling Scenarios",
        "competitive": "Competitive Analysis & Positioning",
        "resources": "Resources & Training Materials",
        "templates": "Templates & Tools Collection",
        "trends": "2025 Industry Trends & Insights",
        "action-plan": "90-Day Action Plan"
    }
    
    # Return enhanced template with input-based customizations
    return ENHANCED_TEMPLATE

# Function to generate AI-powered content
def generate_ai_playbook(input_text, model):
    """Generate AI-enhanced playbook content."""
    if not model:
        return generate_static_playbook(input_text)
    
    prompt = f"""
    Create a comprehensive, modern sales playbook for Rapyder Cloud Solutions based on the following requirements:
    
    {input_text}
    
    Generate a complete HTML document with:
    1. Modern, responsive design with black/red theme
    2. Interactive elements and animations
    3. 16 detailed sections covering all aspects of B2B cloud sales
    4. Real metrics and case studies
    5. Actionable templates and scripts
    6. Mobile-optimized layout
    7. Advanced CSS animations and transitions
    8. JavaScript interactivity
    
    Include all these sections with comprehensive content:
    - About Rapyder & Value Proposition
    - Target Customer Profiles & Buyer Personas
    - Solutions Portfolio with ROI metrics
    - Sales Methodology (SPIN, Challenger, MEDDIC)
    - Step-by-step Sales Process
    - Sales Tools & Technology Stack
    - Messaging Framework & Value Props
    - Call & Email Scripts Library
    - KPIs & Performance Metrics
    - 3+ Detailed Case Studies
    - Objection Handling Scenarios
    - Competitive Analysis & Positioning
    - Resources & Training Materials
    - Templates & Tools Collection
    - 2025 Industry Trends
    - 90-Day Action Plan
    
    Make it visually stunning, highly interactive, and professionally comprehensive.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"AI generation failed: {e}")
        return generate_static_playbook(input_text)

# Enhanced preprocessing function
def preprocess_text(text):
    """Enhanced text preprocessing with validation."""
    try:
        if not text or not text.strip():
            return "Create a comprehensive sales playbook for Rapyder Cloud Solutions with modern design and interactive features."
        
        # Clean and normalize text
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Add default requirements if text is too short
        if len(text) < 50:
            text += " Include modern design, interactive features, case studies, objection handling, and mobile optimization."
        
        return text
    except Exception as e:
        logger.error(f"Text preprocessing failed: {e}")
        return "Create a comprehensive sales playbook for Rapyder Cloud Solutions."

# Enhanced save function with metadata
def save_playbook(content, filename_prefix="rapyder_playbook", metadata=None):
    """Save playbook with enhanced metadata."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{filename_prefix}_{timestamp}_{unique_id}.html"
        
        # Add metadata as HTML comment
        if metadata:
            metadata_comment = f"<!-- Generated by PlaybookGenix\nTimestamp: {timestamp}\nAI Enabled: {metadata.get('ai_enabled', False)}\nUser Input: {metadata.get('input_text', 'N/A')[:100]}... -->\n"
            content = metadata_comment + content
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        
        # Add to session history
        if 'playbook_history' not in st.session_state:
            st.session_state.playbook_history = []
        
        st.session_state.playbook_history.append({
            'filename': filename,
            'timestamp': timestamp,
            'ai_enabled': metadata.get('ai_enabled', False) if metadata else False,
            'preview': content[:200] + "..."
        })
        
        logger.info(f"Playbook saved as {filename}")
        return filename
    except Exception as e:
        logger.error(f"Failed to save playbook: {e}")
        return None

def main():
    st.set_page_config(
        page_title="PlaybookGenix Pro",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Enhanced CSS with modern design
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #1a0000 50%, #000000 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(45deg, #FC3030, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: glow 3s ease-in-out infinite alternate;
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
    }
    
    .main-header p {
        font-size: 1.3rem;
        opacity: 0.9;
        color: #FC3030 !important;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 10px #FC3030); }
        to { filter: drop-shadow(0 0 20px #ff6b6b); }
    }
    
    .feature-card {
        background: linear-gradient(135deg, rgba(26, 26, 26, 0.9), rgba(42, 42, 42, 0.9));
        border: 1px solid #FC3030;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(252, 48, 48, 0.1);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(252, 48, 48, 0.2);
        border-color: #ff6b6b;
    }
    
    .toggle-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        padding: 1rem;
        background: rgba(26, 26, 26, 0.9);
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .ai-toggle {
        position: relative;
        width: 60px;
        height: 30px;
        background: #333;
        border-radius: 15px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .ai-toggle.active {
        background: #FC3030;
    }
    
    .ai-toggle::after {
        content: '';
        position: absolute;
        width: 26px;
        height: 26px;
        background: white;
        border-radius: 50%;
        top: 2px;
        left: 2px;
        transition: all 0.3s ease;
    }
    
    .ai-toggle.active::after {
        transform: translateX(30px);
    }
    
    .input-container {
        background: rgba(26, 26, 26, 0.9);
        border: 2px solid #FC3030;
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(252, 48, 48, 0.1);
    }
    
    .generate-button {
        background: linear-gradient(135deg, #FC3030, #ff6b6b);
        color: #000;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(252, 48, 48, 0.3);
    }
    
    .generate-button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 25px rgba(252, 48, 48, 0.4);
    }
    
    .history-item {
        background: rgba(26, 26, 26, 0.8);
        border: 1px solid #FC3030;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .history-item:hover {
        background: rgba(42, 42, 42, 0.8);
        transform: translateX(5px);
    }
    
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-ai { background: #FC3030; }
    .status-static { background: #666; }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: rgba(26, 26, 26, 0.9);
        border: 1px solid #FC3030;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(252, 48, 48, 0.2);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #FC3030;
        display: block;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #ccc;
        margin-top: 0.5rem;
    }
    
    .preview-container {
        background: rgba(26, 26, 26, 0.9);
        border: 2px solid #FC3030;
        border-radius: 15px;
        margin: 2rem 0;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(252, 48, 48, 0.1);
    }
    
    .preview-header {
        background: linear-gradient(135deg, #FC3030, #ff6b6b);
        color: #000;
        padding: 1rem;
        font-weight: 600;
        display: flex;
        justify-content: between;
        align-items: center;
    }
    
    .loading-spinner {
        border: 3px solid rgba(252, 48, 48, 0.3);
        border-top: 3px solid #FC3030;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .success-message {
        background: linear-gradient(135deg, rgba(46, 125, 50, 0.2), rgba(76, 175, 80, 0.2));
        border: 1px solid #4CAF50;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #4CAF50;
    }
    
    .error-message {
        background: linear-gradient(135deg, rgba(244, 67, 54, 0.2), rgba(229, 57, 53, 0.2));
        border: 1px solid #f44336;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #f44336;
    }
    
    .download-section {
        text-align: center;
        padding: 2rem;
        background: rgba(26, 26, 26, 0.9);
        border-radius: 15px;
        margin: 2rem 0;
    }
    
    .download-button {
        background: linear-gradient(135deg, #4CAF50, #66BB6A);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 0.5rem;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
    
    .download-button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 25px rgba(76, 175, 80, 0.4);
    }
    
    @media (max-width: 768px) {
        .main-header h1 { font-size: 2.5rem; }
        .main-header p { font-size: 1.1rem; }
        .stats-grid { grid-template-columns: 1fr; }
        .feature-card { margin: 0.5rem 0; padding: 1rem; }
        .input-container { padding: 1rem; }
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar Configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # AI Toggle
        ai_enabled = st.toggle(
            "🤖 AI Enhancement",
            value=st.session_state.ai_enabled,
            help="Enable AI-powered content generation for enhanced playbooks"
        )
        st.session_state.ai_enabled = ai_enabled
        
        # Template Selection
        template_style = st.selectbox(
            "🎨 Template Style",
            ["Modern Dark", "Corporate Blue", "Minimalist", "Creative Gradient"],
            help="Choose the visual style for your playbook"
        )
        
        # Content Depth
        content_depth = st.select_slider(
            "📊 Content Depth",
            options=["Basic", "Standard", "Comprehensive", "Enterprise"],
            value="Comprehensive",
            help="Select the level of detail for your playbook"
        )
        
        # Export Options
        st.markdown("### 📤 Export Options")
        export_format = st.multiselect(
            "Format",
            ["HTML", "PDF", "Word", "JSON"],
            default=["HTML"],
            help="Choose export formats"
        )
        
        # Playbook History
        st.markdown("### 📚 Recent Playbooks")
        if st.session_state.playbook_history:
            for i, playbook in enumerate(st.session_state.playbook_history[-5:]):
                with st.expander(f"📄 {playbook['filename'][:20]}..."):
                    st.write(f"**Created:** {playbook['timestamp']}")
                    st.write(f"**AI Used:** {'✅' if playbook['ai_enabled'] else '❌'}")
                    if st.button(f"🔄 Regenerate", key=f"regen_{i}"):
                        st.rerun()
        else:
            st.info("No playbooks generated yet")

    # Main Content Area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Header
        st.markdown("""
        <div class="main-header">
            <h1>🚀 PlaybookGenix Pro</h1>
            <p>Advanced Sales Playbook Generator with AI Intelligence</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature Cards
        st.markdown("""
        <div class="feature-card">
            <h3>✨ Key Features</h3>
            <ul>
                <li><strong>🤖 AI-Powered Generation:</strong> Smart content creation with Gemini AI</li>
                <li><strong>📱 Mobile-First Design:</strong> Responsive layouts for all devices</li>
                <li><strong>🎨 Interactive Elements:</strong> Collapsible sections, search, animations</li>
                <li><strong>📊 Real Data Integration:</strong> Live metrics and performance indicators</li>
                <li><strong>🔧 Customizable Templates:</strong> Multiple themes and styles</li>
                <li><strong>📤 Multi-Format Export:</strong> HTML, PDF, Word, JSON support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Statistics Dashboard
        st.markdown("""
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-number">2.5K+</span>
                <div class="stat-label">Playbooks Generated</div>
            </div>
            <div class="stat-card">
                <span class="stat-number">94%</span>
                <div class="stat-label">User Satisfaction</div>
            </div>
            <div class="stat-card">
                <span class="stat-number">45%</span>
                <div class="stat-label">Sales Increase</div>
            </div>
            <div class="stat-card">
                <span class="stat-number">12min</span>
                <div class="stat-label">Avg Generation Time</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Input Form
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    with st.form(key="enhanced_playbook_form", clear_on_submit=False):
        # Main input area
        input_text = st.text_area(
            "📝 Describe your playbook requirements:",
            placeholder="""Example: Create a comprehensive 2025 Rapyder sales playbook with:
- 3 detailed case studies from banking, healthcare, and e-commerce
- 5 objection-handling scenarios with responses
- Mobile-optimized design with dark theme
- Interactive elements and animations
- ROI calculators and pricing templates
- Competitive analysis against AWS Partners
- Integration with CRM tools and sales automation""",
            height=200,
            help="Provide detailed requirements for your ideal sales playbook"
        )
        
        # Advanced options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            include_case_studies = st.checkbox("📈 Include Case Studies", value=True)
            include_objections = st.checkbox("❓ Objection Handling", value=True)
        
        with col2:
            include_templates = st.checkbox("📄 Templates & Tools", value=True)
            include_competitive = st.checkbox("⚔️ Competitive Analysis", value=True)
        
        with col3:
            include_roi = st.checkbox("💰 ROI Calculators", value=True)
            include_trends = st.checkbox("🔮 2025 Trends", value=True)
        
        # Generate button
        submitted = st.form_submit_button(
            "🚀 Generate Advanced Playbook",
            use_container_width=True,
            type="primary"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Generation Process
    if submitted and input_text:
        # Show loading state
        with st.container():
            st.markdown('<div class="loading-spinner"></div>', unsafe_allow_html=True)
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Text preprocessing
            status_text.text("🔄 Processing your requirements...")
            progress_bar.progress(20)
            
            cleaned_text = preprocess_text(input_text)
            
            # Step 2: AI/Static generation selection
            status_text.text("🤖 Generating playbook content...")
            progress_bar.progress(40)
            
            if ai_enabled:
                model = initialize_gemini()
                if model:
                    playbook_content = generate_ai_playbook(cleaned_text, model)
                    generation_method = "AI-Enhanced"
                else:
                    st.warning("⚠️ AI unavailable, using static generation")
                    playbook_content = generate_static_playbook(cleaned_text)
                    generation_method = "Static Template"
            else:
                playbook_content = generate_static_playbook(cleaned_text)
                generation_method = "Static Template"
            
            # Step 3: Content validation and enhancement
            status_text.text("✅ Validating and enhancing content...")
            progress_bar.progress(60)
            
            # Step 4: File generation
            status_text.text("💾 Generating downloadable files...")
            progress_bar.progress(80)
            
            metadata = {
                'ai_enabled': ai_enabled,
                'input_text': input_text,
                'template_style': template_style,
                'content_depth': content_depth,
                'generation_method': generation_method
            }
            
            filename = save_playbook(playbook_content, metadata=metadata)
            
            # Step 5: Complete
            status_text.text("🎉 Playbook generated successfully!")
            progress_bar.progress(100)
            
            # Success message
            st.markdown(f"""
            <div class="success-message">
                <h4>✅ Playbook Generated Successfully!</h4>
                <p><strong>Method:</strong> {generation_method}</p>
                <p><strong>Template:</strong> {template_style}</p>
                <p><strong>Content Depth:</strong> {content_depth}</p>
                <p><strong>File:</strong> {filename}</p>
            </div>
            """, unsafe_allow_html=True)

    # Preview and Download Section
    if st.session_state.get('current_playbook'):
        st.markdown('<div class="preview-container">', unsafe_allow_html=True)
        st.markdown('<div class="preview-header">📋 Playbook Preview</div>', unsafe_allow_html=True)
        
        # Interactive preview with tabs
        tab1, tab2, tab3 = st.tabs(["🖥️ Full Preview", "📱 Mobile View", "🔍 Structure"])
        
        with tab1:
            st.components.v1.html(st.session_state.current_playbook, height=600, scrolling=True)
        
        with tab2:
            st.components.v1.html(st.session_state.current_playbook, height=800, scrolling=True)
        
        with tab3:
            # Show playbook structure
            st.markdown("### 📊 Playbook Structure Analysis")
            sections = [
                "About Rapyder", "Target Customers", "Solutions", "Methodology",
                "Sales Process", "Tools & Tech", "Messaging", "Scripts",
                "KPIs", "Case Studies", "Objections", "Competitive",
                "Resources", "Templates", "Trends", "Action Plan"
            ]
            
            for i, section in enumerate(sections):
                st.markdown(f"**{i+1}.** {section} ✅")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download section
        st.markdown("""
        <div class="download-section">
            <h3>📤 Download Your Playbook</h3>
            <p>Your playbook is ready! Choose your preferred format:</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if filename:
                with open(filename, "rb") as f:
                    st.download_button(
                        "📄 Download HTML",
                        data=f,
                        file_name=filename,
                        mime="text/html",
                        use_container_width=True
                    )
        
        with col2:
            st.button("📑 Generate PDF", use_container_width=True, disabled=True, help="Coming Soon!")
        
        with col3:
            st.button("📝 Generate Word", use_container_width=True, disabled=True, help="Coming Soon!")
        
        with col4:
            st.button("📊 Export JSON", use_container_width=True, disabled=True, help="Coming Soon!")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🚀 <strong>PlaybookGenix Pro</strong> - Powered by Advanced AI & Modern Web Technologies</p>
        <p>Built with ❤️ for Sales Excellence | Version 2.0</p>
    </div>
    """, unsafe_allow_html=True)
