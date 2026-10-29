"""
Reusable UI component helpers for DoubtBuster frontend.
Separates presentation cards, badges, and layout widgets from application state.
"""
from typing import Dict, Any


def render_metric_card(title: str, value: str, subtitle: str = "") -> str:
    """Generates styled HTML metric card."""
    return f"""
    <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 1rem; text-align: center;">
        <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">{title}</div>
        <div style="font-size: 1.8rem; font-weight: 800; color: #38bdf8; margin: 0.2rem 0;">{value}</div>
        <div style="font-size: 0.75rem; color: #64748b;">{subtitle}</div>
    </div>
    """


def render_domain_badge(domain: str) -> str:
    """Generates styled domain pill badge."""
    return f'<span style="background: rgba(56, 189, 248, 0.12); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 9999px; padding: 0.2rem 0.75rem; font-size: 0.75rem; font-weight: 600;">🏷️ {domain}</span>'

