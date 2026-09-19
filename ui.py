import streamlit as st

def inject_theme():
    """Injects custom CSS styling tailored to clinical diagnostics."""
    is_dark = st.session_state.get("theme", "dark") == "dark"

    if is_dark:
        bg_primary = "#0F172A"       # Dark Slate
        bg_card = "#1E293B"          # Medium Slate Card
        bg_secondary = "#334155"     # Darker Gray/Blue
        text_primary = "#F8FAFC"     # Off-white
        text_muted = "#94A3B8"       # Muted Gray
        border_color = "#334155"
        input_bg = "#0F172A"
    else:
        bg_primary = "#F8FAFC"       # Light Slate
        bg_card = "#FFFFFF"          # Pure White
        bg_secondary = "#F1F5F9"     # Light Gray
        text_primary = "#0F172A"     # Deep Blue/Black
        text_muted = "#64748B"       # Slate Muted
        border_color = "#E2E8F0"
        input_bg = "#FFFFFF"

    accent_teal = "#0D9488"
    accent_sky = "#0284C7"

    css = f"""
    <style>
    /* Global Background */
    .stApp {{
        background-color: {bg_primary} !important;
        color: {text_primary} !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: {bg_card} !important;
        border-right: 1px solid {border_color};
    }}

    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, {accent_sky} 0%, {accent_teal} 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.2s ease-in-out;
    }}
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3);
    }}

    /* Input Controls */
    .stTextInput input, .stNumberInput input, .stSelectbox select {{
        background-color: {input_bg} !important;
        color: {text_primary} !important;
        border: 1px solid {border_color} !important;
        border-radius: 8px !important;
    }}

    /* Metric Cards */
    [data-testid="stMetricValue"] {{
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: {accent_teal} !important;
    }}

    /* Expanders */
    .streamlit-expanderHeader {{
        background-color: {bg_card} !important;
        border-radius: 8px !important;
        color: {text_primary} !important;
    }}

    /* Custom Header Banner */
    .clinical-header {{
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border: 1px solid #334155;
        border-left: 6px solid {accent_teal};
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 24px;
    }}
    .clinical-header h1 {{
        color: #F8FAFC !important;
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }}
    .clinical-header p {{
        color: #94A3B8 !important;
        margin: 5px 0 0 0;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_header(title: str, subtitle: str, icon: str = "🩺"):
    """Renders a styled header card."""
    st.markdown(
        f"""
        <div class="clinical-header">
            <h1>{icon} {title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )