"""
DoubtBuster Unified Cutting-Edge Design System & Theme Engine
Provides cohesive glassmorphism styling, modern typography, responsive hero headers,
interactive navigation bars, and glowing status badges across all pages.
"""

import streamlit as st
from typing import List, Optional

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Global Font & Smooth Antialiasing */
html, body, [class*="css"], .stMarkdown, .stText, p, span, div {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    letter-spacing: -0.01em;
}

code, pre, .stCodeBlock, .stCode {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Modern Unified Header Card */
.db-hero-card {
    background: linear-gradient(135deg, #0a0f1d 0%, #111827 50%, #1e1b4b 100%);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 18px;
    padding: 1.6rem 2.2rem;
    color: #ffffff;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.4), inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
}

.db-gradient-title {
    font-size: 2.3rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.03em;
    background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block;
}

.db-subtitle {
    color: #94a3b8;
    font-size: 0.98rem;
    margin-top: 0.35rem;
    margin-bottom: 0.8rem;
    line-height: 1.5;
}

.db-badge-container {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.6rem;
    flex-wrap: wrap;
}

.db-badge {
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.14);
    padding: 0.28rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.76rem;
    font-weight: 600;
    color: #e2e8f0;
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    backdrop-filter: blur(8px);
}

.db-badge-accent {
    background: rgba(59, 130, 246, 0.15);
    border: 1px solid rgba(59, 130, 246, 0.35);
    color: #38bdf8;
}

.db-stat-pill {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 14px;
    padding: 0.7rem 1.2rem;
    text-align: center;
    min-width: 135px;
    backdrop-filter: blur(8px);
}

/* Glassmorphism Surface Cards */
.db-glass-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1.2rem;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}

.db-glass-card:hover {
    border-color: rgba(99, 102, 241, 0.3);
    box-shadow: 0 8px 20px -4px rgba(0, 0, 0, 0.2);
}

/* Domain Pill Badge */
.domain-pill {
    background: rgba(59, 130, 246, 0.12);
    border: 1px solid rgba(59, 130, 246, 0.3);
    color: #38bdf8;
    padding: 0.25rem 0.7rem;
    border-radius: 8px;
    font-size: 0.78rem;
    font-weight: 700;
    display: inline-block;
    margin-bottom: 0.6rem;
    letter-spacing: 0.01em;
}

/* Quick Navigation Bar */
.db-navbar {
    display: flex;
    gap: 0.6rem;
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 0.45rem;
    margin-bottom: 1.4rem;
    flex-wrap: wrap;
    backdrop-filter: blur(12px);
}

.db-nav-item {
    padding: 0.45rem 1rem;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #94a3b8;
    text-decoration: none;
    transition: all 0.2s ease;
    border: 1px solid transparent;
}

.db-nav-item:hover {
    color: #ffffff;
    background: rgba(255, 255, 255, 0.05);
}

.db-nav-item.active {
    color: #ffffff;
    background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.35);
    border-color: rgba(129, 140, 248, 0.3);
}

/* Metric KPI Box */
.db-kpi-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.db-kpi-card:hover {
    border-color: rgba(99, 102, 241, 0.35);
    transform: translateY(-2px);
}

.db-kpi-value {
    font-size: 2.2rem;
    font-weight: 800;
    color: #f8fafc;
    line-height: 1.1;
    margin: 0.3rem 0;
}

.db-kpi-label {
    font-size: 0.76rem;
    color: #94a3b8;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Prompt Starter Chips */
.db-starter-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 1rem;
    height: 100%;
    cursor: pointer;
    transition: all 0.2s ease;
}

.db-starter-card:hover {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(99, 102, 241, 0.4);
    transform: translateY(-2px);
}

.db-starter-title {
    font-size: 0.9rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 0.35rem;
}

.db-starter-desc {
    font-size: 0.78rem;
    color: #94a3b8;
    line-height: 1.4;
}

/* Button & Form Enhancements */
div.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.88rem;
    transition: all 0.2s ease;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
    border: 1px solid rgba(129, 140, 248, 0.3);
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.25);
}

div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #4338ca 0%, #4f46e5 100%);
    box-shadow: 0 6px 18px rgba(79, 70, 229, 0.35);
    transform: translateY(-1px);
}

/* Streamlit Tabs Customization */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: rgba(255, 255, 255, 0.02);
    padding: 0.4rem;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    font-size: 0.88rem;
    color: #94a3b8;
}

.stTabs [aria-selected="true"] {
    background: rgba(99, 102, 241, 0.15) !important;
    color: #818cf8 !important;
    border-bottom: 2px solid #818cf8 !important;
}

/* Expander Styling */
.streamlit-expanderHeader {
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    font-weight: 600;
}
</style>
"""

def inject_theme():
    """Injects the global cutting-edge stylesheet into the active Streamlit page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_header(
    title: str = "✨ DoubtBuster",
    subtitle: str = "Gemini-Style Universal AI Academic Tutor — On-the-fly multi-domain reasoning & mathematical verification",
    badges: Optional[List[str]] = None,
    streak: int = 0,
    doubts_count: int = 0,
    show_stats: bool = True
):
    """Renders the signature glassmorphic hero header across pages."""
    if badges is None:
        badges = [
            "⚡ Dynamic Synthesis",
            "🌐 All Disciplines",
            "🧮 SymPy Engine",
            "🧪 Secure Sandbox"
        ]

    badge_html = "".join([f'<span class="db-badge">{b}</span>' for b in badges])

    stats_html = ""
    if show_stats:
        stats_html = f"""
        <div class="db-stat-pill">
            <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em;">Study Streak</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: #38bdf8;">🔥 {streak} <span style="font-size: 0.82rem; font-weight: 600; color: #94a3b8;">days</span></div>
            <div style="font-size: 0.72rem; color: #64748b;">{doubts_count} doubts resolved</div>
        </div>
        """

    header_markup = f"""
    <div class="db-hero-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
            <div style="flex: 1; min-width: 280px;">
                <h1 class="db-gradient-title">{title}</h1>
                <p class="db-subtitle">{subtitle}</p>
                <div class="db-badge-container">
                    {badge_html}
                </div>
            </div>
            {stats_html}
        </div>
    </div>
    """
    st.markdown(header_markup, unsafe_allow_html=True)


def render_quick_nav(active: str = "Home"):
    """
    Renders a unified horizontal navigation pill bar at the top of pages
    allowing 1-click discovery and fast switching.
    """
    nav_items = [
        {"name": "💬 Ask AI Tutor", "key": "Home", "page": "app.py"},
        {"name": "🧠 Practice & Quiz", "key": "Quiz", "page": "pages/2_Practice_Quiz.py"},
        {"name": "📚 Learning History", "key": "History", "page": "pages/1_Learning_History.py"},
        {"name": "📄 Study Hub & Notes", "key": "Study", "page": "pages/3_Study_Materials.py"},
        {"name": "📈 Student Progress", "key": "Progress", "page": "pages/4_Student_Progress.py"},
        {"name": "👨‍🏫 Faculty Dashboard", "key": "Faculty", "page": "pages/5_Faculty_Dashboard.py"}
    ]

    cols = st.columns(len(nav_items))
    for idx, item in enumerate(nav_items):
        with cols[idx]:
            is_active = (item["key"] == active)
            btn_type = "primary" if is_active else "secondary"
            if st.button(item["name"], key=f"nav_btn_{item['key']}", type=btn_type, use_container_width=True):
                if not is_active:
                    st.switch_page(item["page"])
