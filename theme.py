import streamlit as st
 
 
def apply_custom_theme(current_theme="light"):
    """
    Injects clean, clinical styling for the app.
 
    Fixes applied vs. the old version:
      1. Buttons never got styled because the CSS used a *direct child*
         selector (`.stButton > button`). Current Streamlit wraps the real
         <button> one level deeper, so that rule matched nothing. We now
         target the actual element via its stable data-testid
         (`stBaseButton-*`), which works no matter how Streamlit nests
         things internally.
      2. The header banner was hardcoded to a dark gradient regardless of
         theme. It now uses theme-aware colors, so light mode gets a light
         banner and dark mode gets a dark one.
      3. The old blanket `p, span, label {color: ... !important}` rule was
         also overriding the text color *inside* st.success/st.error/
         st.warning/st.info boxes (they render plain <p> tags too), making
         alert text harder to read. We now explicitly hand color back to
         Streamlit's own alert styling.
    """
    is_dark = (current_theme == "dark")
 
    if is_dark:
        # ---- Modern dark palette ----
        bg_app      = "#0B1220"
        bg_card     = "#111A2E"
        bg_sidebar  = "#0E1729"
        text_main   = "#EAF0FA"
        text_sub    = "#93A4BD"
        border_col  = "#22304A"
        input_bg    = "#0E1729"
        banner_grad = "linear-gradient(135deg, #17233D 0%, #0B1220 100%)"
        banner_border = "#26365A"
        shadow      = "0 4px 16px rgba(0, 0, 0, 0.35)"
    else:
        # ---- Clean clinical light palette (default) ----
        bg_app      = "#F5F8FC"
        bg_card     = "#FFFFFF"
        bg_sidebar  = "#FFFFFF"
        text_main   = "#0F172A"
        text_sub    = "#5B6B82"
        border_col  = "#E1E8F1"
        input_bg    = "#FFFFFF"
        banner_grad = "linear-gradient(135deg, #FFFFFF 0%, #EAF2FD 100%)"
        banner_border = "#DCE7F7"
        shadow      = "0 2px 10px rgba(15, 23, 42, 0.06)"
 
    # Shared clinical-blue accent across both themes for brand consistency
    accent_1 = "#2E6BF2"
    accent_2 = "#1849B3"
 
    css = f"""
    <style>
 
    /* ---------- App shell ---------- */
    .stApp, [data-testid="stAppViewContainer"] {{
        background-color: {bg_app} !important;
        color: {text_main};
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    }}
 
    [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}
 
    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {{
        background-color: {bg_sidebar} !important;
        border-right: 1px solid {border_col} !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: {text_main} !important;
    }}
 
    /* Sidebar nav (radio) styled like a clean nav list */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label {{
        padding: 8px 10px;
        border-radius: 8px;
        margin-bottom: 2px;
        transition: background-color 0.15s ease;
    }}
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {{
        background-color: {bg_app};
    }}
 
    /* ---------- General text ---------- */
    p, span, label, h1, h2, h3, h4, h5, h6, .stMarkdown, .stCaption {{
        color: {text_main};
    }}
    .stCaption, [data-testid="stCaptionContainer"] {{
        color: {text_sub} !important;
    }}
 
    /* Give Streamlit's own alert boxes their color back (success/error/
       warning/info) instead of the blanket text color above. */
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span,
    [data-testid="stAlertTitle"] * {{
        color: inherit !important;
    }}
    [data-testid="stAlert"] {{
        border-radius: 10px !important;
    }}
 
    /* ---------- Buttons (the actual fix) ---------- */
    .stButton {{
        width: 100%;
    }}
    [data-testid^="stBaseButton"] {{
        background: linear-gradient(135deg, {accent_1} 0%, {accent_2} 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.2rem !important;
        transition: all 0.2s ease !important;
        width: 100%;
        box-shadow: none !important;
    }}
    [data-testid^="stBaseButton"]:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(46, 107, 242, 0.35) !important;
    }}
    [data-testid^="stBaseButton"] p {{
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }}
 
    /* ---------- Inputs ---------- */
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox input {{
        background-color: {input_bg} !important;
        color: {text_main} !important;
        border-radius: 8px !important;
    }}
    [data-testid="stTextInputRootElement"],
    [data-testid="stNumberInputContainer"] {{
        background-color: {input_bg} !important;
        border: 1px solid {border_col} !important;
        border-radius: 8px !important;
    }}
    /* Selectbox's visible box: style whichever wrapper directly holds the
       input, without depending on an exact class name. */
    .stSelectbox div:has(> input) {{
        background-color: {input_bg} !important;
        border: 1px solid {border_col} !important;
        border-radius: 8px !important;
    }}
 
    /* ---------- Cards / containers ---------- */
    [data-testid="stExpander"] {{
        background-color: {bg_card};
        border: 1px solid {border_col} !important;
        border-radius: 10px !important;
        box-shadow: {shadow};
    }}
    [data-testid="stMetric"] {{
        background-color: {bg_card};
        border: 1px solid {border_col};
        border-radius: 10px;
        padding: 12px 16px;
        box-shadow: {shadow};
    }}
    hr, [data-testid="stDivider"] {{
        border-color: {border_col} !important;
    }}
 
    /* ---------- Header Banner (now theme-aware) ---------- */
    .header-card {{
        background: {banner_grad};
        border: 1px solid {banner_border};
        border-left: 6px solid {accent_1};
        padding: 20px 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: {shadow};
    }}
    .header-card h1 {{
        color: {text_main} !important;
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
    }}
    .header-card p {{
        color: {text_sub} !important;
        margin-top: 5px;
        margin-bottom: 0;
    }}
 
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
 
 
def render_banner(title: str, subtitle: str, icon: str = "🩺"):
    """Displays a styled clinical banner at the top of pages."""
    st.markdown(
        f"""
        <div class="header-card">
            <h1>{icon} {title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )