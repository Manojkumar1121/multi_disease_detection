"""
Theme and custom clinical UI styling module.
Renders the bespoke clinical aesthetic:
- Dark slate-teal sidebar with glowing brand mark, active emerald navigation pill, and user status badge.
- Mint-tinted clinical background (#F1F5F3).
- Top medical header with botanical leaves and stethoscope graphic.
- Disease category pills (Lung, Heart, Brain, Kidney).
- Deep emerald gradient hero banner with glowing stethoscope and AI chip circuit.
- Coral-orange action buttons (#FF6F59), dashed file upload container, and sage-tinted inputs.
"""

import base64
import os
import streamlit as st


def apply_custom_theme(current_theme="light"):
    """
    Injects custom clinical CSS styling matching the exact design specifications.
    """
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    /* =========================================================================
       1. GLOBAL APP SHELL & BACKGROUND
       ========================================================================= */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', system-ui, -apple-system, sans-serif !important;
    }

    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #F1F5F3 !important;
        color: #11252D !important;
    }

    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Main block container padding */
    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1080px !important;
    }

    /* =========================================================================
       2. SIDEBAR STYLING
       ========================================================================= */
    section[data-testid="stSidebar"] {
        background-color: #14232C !important;
        border-right: 1px solid #1D3441 !important;
        width: 290px !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }

    /* Brand Header */
    .sidebar-brand-container {
        margin-bottom: 20px;
    }

    .sidebar-brand-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
    }

    .brand-logo-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        background: linear-gradient(135deg, #105946 0%, #177C62 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(16, 89, 70, 0.45);
        border: 1px solid #23A080;
    }

    .brand-title {
        color: #FFFFFF !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        line-height: 1.2 !important;
        letter-spacing: -0.02em;
    }

    .brand-sub {
        color: #7995A2 !important;
        font-size: 0.76rem !important;
        margin: 0 !important;
        font-weight: 500 !important;
    }

    /* User Profile Pill Badge */
    .user-profile-badge {
        background: #1C303B;
        border: 1px solid #264353;
        border-radius: 20px;
        padding: 7px 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 22px;
    }

    .user-profile-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .user-avatar-circle {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background: #2E5062;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.85rem;
        color: #FFFFFF;
        border: 1.5px solid #487289;
    }

    .user-details {
        display: flex;
        flex-direction: column;
    }

    .user-details-label {
        font-size: 0.72rem;
        color: #8CA4B1;
        line-height: 1.1;
    }

    .user-details-name {
        font-size: 0.88rem;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.2;
    }

    .user-status-dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 10px #10B981, 0 0 4px #10B981;
    }

    /* Sidebar Navigation Heading */
    .sidebar-nav-heading {
        color: #8C9FA8 !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        text-transform: capitalize !important;
        margin-bottom: 8px !important;
        letter-spacing: 0.01em;
    }

    /* =========================================================================
       3. SIDEBAR RADIO MENU (PILL BUTTONS - NO BLUE BLOBS!)
       ========================================================================= */
    section[data-testid="stSidebar"] [data-testid="stRadio"] > div {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    /* Hide native radio circle */
    section[data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"] {
        display: none !important;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label {
        display: flex !important;
        align-items: center !important;
        padding: 10px 16px !important;
        border-radius: 10px !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        color: #D3DFE6 !important;
        background: transparent !important;
        border: 1px solid transparent !important;
        cursor: pointer !important;
        transition: all 0.18s ease-in-out !important;
        margin-bottom: 0 !important;
    }

    /* Inactive item hover */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: #1B2F3B !important;
        color: #FFFFFF !important;
        border-color: #274556 !important;
    }

    /* Hide the radio inner circle dot icon */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child {
        display: none !important;
    }

    /* ACTIVE ITEM: Rich Dark Emerald Gradient Pill (Matches Image 2) */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"],
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(135deg, #094535 0%, #115D48 100%) !important;
        border: 1px solid #1A7B5F !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(9, 69, 53, 0.5) !important;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] p,
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* =========================================================================
       4. TOP TITLE & MEDICAL BANNER
       ========================================================================= */
    .top-header-wrapper {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 22px;
        position: relative;
    }

    .top-header-left {
        display: flex;
        align-items: stretch;
        gap: 14px;
    }

    .top-header-accent-bar {
        width: 4px;
        background: #0E5C46;
        border-radius: 4px;
        flex-shrink: 0;
    }

    .top-header-text h1 {
        font-size: 1.68rem !important;
        font-weight: 800 !important;
        color: #0E242C !important;
        margin: 0 0 4px 0 !important;
        line-height: 1.2 !important;
        letter-spacing: -0.02em;
    }

    .top-header-text p {
        font-size: 0.92rem !important;
        color: #517169 !important;
        margin: 0 !important;
        font-weight: 500 !important;
    }

    .top-header-right-art {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        position: relative;
    }

    /* =========================================================================
       5. FOUR CATEGORY PILL BADGES
       ========================================================================= */
    .category-pills-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-bottom: 22px;
    }

    .category-pill {
        border-radius: 12px;
        padding: 12px 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        font-weight: 600;
        font-size: 0.93rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
        border: 1px solid transparent;
        transition: transform 0.15s ease;
    }

    .category-pill:hover {
        transform: translateY(-2px);
    }

    .pill-lung {
        background-color: #D8E7DE;
        border-color: #C3D9CB;
        color: #19462D;
    }

    .pill-heart {
        background-color: #F8E4D5;
        border-color: #EBD0BD;
        color: #793417;
    }

    .pill-brain {
        background-color: #FAEBD8;
        border-color: #ECD8BF;
        color: #7A491A;
    }

    .pill-kidney {
        background-color: #DCE8F0;
        border-color: #C4D7E2;
        color: #21485E;
    }

    /* =========================================================================
       6. HERO BANNER: DEEP EMERALD WITH STETHOSCOPE & AI CHIP
       ========================================================================= */
    .hero-banner-card {
        background: linear-gradient(135deg, #07382B 0%, #0F5844 55%, #084333 100%);
        border-radius: 14px;
        padding: 24px 28px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
        box-shadow: 0 6px 20px rgba(7, 56, 43, 0.22);
        position: relative;
        overflow: hidden;
        border: 1px solid #146D54;
    }

    /* Subtle DNA/circuit background watermark */
    .hero-banner-card::before {
        content: "";
        position: absolute;
        right: 80px;
        top: -20px;
        bottom: -20px;
        width: 300px;
        background-image: radial-gradient(#158063 1px, transparent 1px);
        background-size: 16px 16px;
        opacity: 0.25;
        pointer-events: none;
    }

    .hero-banner-left {
        display: flex;
        align-items: center;
        gap: 20px;
        z-index: 1;
    }

    .hero-steth-icon {
        width: 52px;
        height: 52px;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .hero-banner-text h2 {
        color: #FFFFFF !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        margin: 0 0 6px 0 !important;
        letter-spacing: -0.01em;
    }

    .hero-banner-text p {
        color: #D6EDE4 !important;
        font-size: 0.94rem !important;
        margin: 0 !important;
        font-weight: 400 !important;
        line-height: 1.4 !important;
    }

    .hero-ai-chip {
        z-index: 1;
        flex-shrink: 0;
    }

    /* =========================================================================
       7. UPLOAD SECTION (DASHED BOX WITH CORAL BUTTON)
       ========================================================================= */
    .upload-box-wrapper {
        background: #F8FAF9;
        border: 1.5px dashed #A4C2B6;
        border-radius: 12px;
        padding: 14px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
    }

    .upload-left-group {
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .upload-btn-styled {
        background: linear-gradient(135deg, #FF6F59 0%, #FA573E 100%);
        color: #FFFFFF;
        font-weight: 700;
        font-size: 0.92rem;
        padding: 8px 18px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 3px 10px rgba(255, 111, 89, 0.35);
        cursor: pointer;
    }

    .upload-specs {
        color: #55726B;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .upload-drag-hint {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #6C8A81;
        font-size: 0.9rem;
        font-weight: 500;
    }

    /* Style Streamlit's native file uploader */
    [data-testid="stFileUploader"] {
        margin-bottom: 18px !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background-color: #F8FAF9 !important;
        border: 1.5px dashed #A4C2B6 !important;
        border-radius: 12px !important;
        padding: 12px 18px !important;
    }

    [data-testid="stFileUploaderDropzone"] button {
        background: linear-gradient(135deg, #FF6F59 0%, #FA573E 100%) !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 700 !important;
        box-shadow: 0 3px 10px rgba(255, 111, 89, 0.35) !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] * {
        color: #55726B !important;
    }

    /* =========================================================================
       8. MODEL VALIDATION EXPANDER (MINT-SAGE BAR)
       ========================================================================= */
    [data-testid="stExpander"] {
        background-color: #CFE2D7 !important;
        border: 1px solid #B8D3C4 !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        margin-bottom: 22px !important;
    }

    [data-testid="stExpander"] summary {
        background-color: #CFE2D7 !important;
        color: #133D2D !important;
        font-weight: 700 !important;
        font-size: 0.96rem !important;
        padding: 12px 18px !important;
        border-radius: 10px !important;
    }

    [data-testid="stExpander"] summary:hover {
        background-color: #C3DDD0 !important;
    }

    [data-testid="stExpander"] summary svg {
        fill: #133D2D !important;
    }

    [data-testid="stExpanderDetails"] {
        background-color: #FFFFFF !important;
        border-top: 1px solid #B8D3C4 !important;
        border-radius: 0 0 10px 10px !important;
        padding: 18px !important;
    }

    /* =========================================================================
       9. PATIENT FORM & INPUT FIELDS
       ========================================================================= */
    [data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #D6E4DC !important;
        border-radius: 14px !important;
        padding: 24px 26px !important;
        box-shadow: 0 4px 16px rgba(16, 40, 30, 0.04) !important;
    }

    /* Form field labels with custom icons */
    .form-field-label {
        font-size: 0.92rem;
        font-weight: 700;
        color: #132E27;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Text & Number Inputs */
    .stTextInput input,
    .stNumberInput input {
        background-color: #FAFCFB !important;
        border-radius: 10px !important;
        color: #122C24 !important;
        font-size: 0.95rem !important;
        padding: 10px 14px !important;
    }

    [data-testid="stTextInputRootElement"],
    [data-testid="stNumberInputContainer"] {
        background-color: #FAFCFB !important;
        border: 1.5px solid #CCDCD3 !important;
        border-radius: 10px !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }

    [data-testid="stTextInputRootElement"]:focus-within,
    [data-testid="stNumberInputContainer"]:focus-within {
        border-color: #0E5C46 !important;
        box-shadow: 0 0 0 3px rgba(14, 92, 70, 0.12) !important;
    }

    /* Multiselect box (Light Sage Green in Image 2) */
    [data-baseweb="select"] > div {
        background-color: #C4DEC9 !important;
        border: 1.5px solid #ADCDB3 !important;
        border-radius: 10px !important;
        color: #16402E !important;
        min-height: 44px !important;
    }

    [data-baseweb="select"] * {
        color: #16402E !important;
        font-weight: 500 !important;
    }

    [data-baseweb="select"] svg {
        fill: #16402E !important;
    }

    /* Selected symptom chips inside multiselect */
    [data-baseweb="select"] [data-baseweb="tag"] {
        background: #0E5C46 !important;
        border-radius: 6px !important;
        border: none !important;
    }

    [data-baseweb="select"] [data-baseweb="tag"] * {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    [data-baseweb="select"] [data-baseweb="tag"] svg {
        fill: #FFFFFF !important;
    }

    /* Dropdown menu popover */
    [data-baseweb="popover"] [data-baseweb="menu"],
    [data-baseweb="popover"] ul {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CCDCD3 !important;
        border-radius: 10px !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08) !important;
    }

    [data-baseweb="popover"] li {
        color: #152E27 !important;
        padding: 9px 14px !important;
        font-weight: 500 !important;
    }

    [data-baseweb="popover"] li:hover,
    [data-baseweb="popover"] li[aria-selected="true"] {
        background-color: #EBF3EE !important;
        color: #0E5C46 !important;
    }

    /* =========================================================================
       10. PREDICT ACTION BUTTON (CORAL-ORANGE PILL)
       ========================================================================= */
    /* Form submit button */
    [data-testid="stFormSubmitButton"] {
        display: inline-block !important;
        width: auto !important;
    }

    [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #FF6F59 0%, #FA573E 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        padding: 0.65rem 2.2rem !important;
        box-shadow: 0 4px 14px rgba(255, 111, 89, 0.4) !important;
        transition: all 0.2s ease !important;
        width: auto !important;
    }

    [data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 18px rgba(255, 111, 89, 0.5) !important;
    }

    /* General primary buttons */
    .stDownloadButton > button,
    .stButton > button {
        background: linear-gradient(135deg, #FF6F59 0%, #FA573E 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        padding: 0.6rem 1.8rem !important;
        box-shadow: 0 4px 12px rgba(255, 111, 89, 0.35) !important;
        transition: all 0.2s ease !important;
    }

    .stDownloadButton > button:hover,
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(255, 111, 89, 0.45) !important;
    }

    /* Button and Helper Text inline container */
    .predict-row-container {
        display: flex;
        align-items: center;
        gap: 18px;
        margin-top: 10px;
    }

    .predict-helper-text {
        color: #55726B;
        font-size: 0.88rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* =========================================================================
       11. CLINICAL CARDS, METRICS & RESULTS
       ========================================================================= */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #D6E4DC;
        border-left: 4px solid #0E5C46;
        border-radius: 10px;
        padding: 12px 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        color: #0E5C46 !important;
    }

    /* Alert Styling */
    [data-testid="stAlert"] {
        border-radius: 10px !important;
        border-width: 1px !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_sidebar_header(username: str = "manoj"):
    """Renders the top branding and logged-in user profile badge in the sidebar."""
    display_user = username if username else "clinician"
    st.sidebar.markdown(
        f"""
        <div class="sidebar-brand-container">
            <div class="sidebar-brand-header">
                <div class="brand-logo-icon">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>
                        <path d="M3.22 12H9.5l1.5-3 2 6 1.5-3h6.28"/>
                    </svg>
                </div>
                <div class="brand-text">
                    <div class="brand-title">Health Portal</div>
                    <div class="brand-sub">Multi-Disease Detection System</div>
                </div>
            </div>
            <div class="user-profile-badge">
                <div class="user-profile-left">
                    <div class="user-avatar-circle">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>
                            <circle cx="12" cy="7" r="4"/>
                        </svg>
                    </div>
                    <div class="user-details">
                        <span class="user-details-label">Signed in as:</span>
                        <span class="user-details-name">{display_user}</span>
                    </div>
                </div>
                <div class="user-status-dot" title="Online"></div>
            </div>
            <div class="sidebar-nav-heading">Navigate</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_header(
    title: str = "Multi-Disease Detection System",
    subtitle: str = "AI-powered diagnosis for multiple diseases from patient data and symptoms",
):
    """
    Renders top title bar and clinical stethoscope graphic.
    """
    st.markdown(
        f"""
        <div class="top-header-wrapper">
            <div class="top-header-left">
                <div class="top-header-accent-bar"></div>
                <div class="top-header-text">
                    <h1>{title}</h1>
                    <p>{subtitle}</p>
                </div>
            </div>
            <div class="top-header-right-art">
                <!-- Stethoscope & Botanical Leaves SVG Art -->
                <svg width="210" height="90" viewBox="0 0 210 90" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <!-- Leaves -->
                    <g opacity="0.88">
                        <path d="M195 12 C185 2 170 8 175 22 C180 34 198 32 195 12 Z" fill="#2E7D32"/>
                        <path d="M205 32 C192 24 185 38 190 48 C198 55 208 45 205 32 Z" fill="#388E3C"/>
                        <path d="M180 4 C170 0 160 10 168 18 C176 24 184 15 180 4 Z" fill="#43A047"/>
                    </g>
                    <!-- Stethoscope loop -->
                    <path d="M12 40 C35 85, 95 85, 120 40 C135 15, 155 18, 168 32" stroke="#263238" stroke-width="4.5" stroke-linecap="round"/>
                    <path d="M12 40 C-2 15, 20 -2, 45 10 C62 20, 68 40, 75 52" stroke="#37474F" stroke-width="4" stroke-linecap="round"/>
                    <!-- Chrome binaural ear tubes -->
                    <path d="M35 14 L20 6" stroke="#90A4AE" stroke-width="3" stroke-linecap="round"/>
                    <path d="M48 20 L60 8" stroke="#90A4AE" stroke-width="3" stroke-linecap="round"/>
                    <!-- Eartips -->
                    <circle cx="18" cy="5" r="3" fill="#263238"/>
                    <circle cx="62" cy="7" r="3" fill="#263238"/>
                    <!-- Chest piece (Diaphragm) -->
                    <circle cx="168" cy="34" r="13" fill="#B0BEC5" stroke="#78909C" stroke-width="2.5"/>
                    <circle cx="168" cy="34" r="9" fill="#ECEFF1"/>
                    <circle cx="168" cy="34" r="4.5" fill="#546E7A"/>
                </svg>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_category_pills():
    """Renders the 4 clinical disease category pills across the top."""
    st.markdown(
        """
        <div class="category-pills-grid">
            <div class="category-pill pill-lung">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#19462D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17 19.5c1.5-1.5 2-4 2-7.5 0-3.5-1.5-6-4-6-1.5 0-2.5 1-3 2.5"/>
                    <path d="M7 19.5c-1.5-1.5-2-4-2-7.5 0-3.5 1.5-6 4-6 1.5 0 2.5 1 3 2.5"/>
                    <path d="M12 6v14"/>
                    <path d="M12 10c1.5-1 3-1.5 4.5-1.5"/>
                    <path d="M12 10c-1.5-1-3-1.5-4.5-1.5"/>
                </svg>
                <span>Lung Disease</span>
            </div>
            <div class="category-pill pill-heart">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#793417" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>
                    <path d="M3.22 12H9.5l1.5-3 2 6 1.5-3h6.28"/>
                </svg>
                <span>Heart Disease</span>
            </div>
            <div class="category-pill pill-brain">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#7A491A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 4.44-2.04"/>
                    <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-4.44-2.04"/>
                </svg>
                <span>Brain Disease</span>
            </div>
            <div class="category-pill pill-kidney">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#21485E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M7 6c-2.5 0-4 2-4 5.5s2 6.5 4 7.5 4 0 4-2.5-1-4-2-5c1.5-1 2-3 1-4.5S8.5 6 7 6Z"/>
                    <path d="M17 6c2.5 0 4 2 4 5.5s-2 6.5-4 7.5-4 0-4-2.5 1-4 2-5c-1.5-1-2-3-1-4.5S15.5 6 17 6Z"/>
                </svg>
                <span>Kidney Disease</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero_banner(
    title: str = "Disease Management Predictor",
    subtitle: str = "Enter patient details, select symptoms, and get an ensemble prediction across multiple ML models.",
):
    """
    Renders the rich emerald hero banner with glowing stethoscope and AI circuit chip.
    """
    st.markdown(
        f"""
        <div class="hero-banner-card">
            <div class="hero-banner-left">
                <div class="hero-steth-icon">
                    <svg width="46" height="46" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"/>
                        <path d="M8 15v1a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6v-4"/>
                        <circle cx="20" cy="10" r="2"/>
                    </svg>
                </div>
                <div class="hero-banner-text">
                    <h2>{title}</h2>
                    <p>{subtitle}</p>
                </div>
            </div>
            <div class="hero-ai-chip">
                <!-- AI Processor Chip Icon -->
                <svg width="68" height="68" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="14" y="14" width="36" height="36" rx="8" stroke="#FFFFFF" stroke-width="2.5" fill="#0C4837"/>
                    <line x1="22" y1="8" x2="22" y2="14" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
                    <line x1="32" y1="8" x2="32" y2="14" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
                    <line x1="42" y1="8" x2="42" y2="14" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
                    <line x1="22" y1="50" x2="22" y2="56" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
                    <line x1="32" y1="50" x2="32" y2="56" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
                    <line x1="42" y1="50" x2="42" y2="56" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
                    <line x1="8" y1="22" x2="14" y2="22" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
                    <line x1="8" y1="32" x2="14" y2="32" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
                    <line x1="8" y1="42" x2="14" y2="42" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
                    <line x1="50" y1="22" x2="56" y2="22" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
                    <line x1="50" y1="32" x2="56" y2="32" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
                    <line x1="50" y1="42" x2="56" y2="42" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
                    <text x="32" y="38" fill="#FFFFFF" font-family="'Plus Jakarta Sans', sans-serif" font-size="14" font-weight="800" text-anchor="middle">AI</text>
                </svg>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_banner(title: str, subtitle: str, icon: str = "🩺"):
    """Compatibility wrapper for other pages (Detection History, Settings)."""
    st.markdown(
        f"""
        <div class="hero-banner-card" style="margin-bottom: 22px;">
            <div class="hero-banner-left">
                <div style="font-size: 2.2rem; margin-right: 6px;">{icon}</div>
                <div class="hero-banner-text">
                    <h2>{title}</h2>
                    <p>{subtitle}</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

_AUTH_HERO_DATA_URI_CACHE = None


def get_auth_hero_data_uri() -> str:
    """Loads and caches the base64 data URI of the cropped auth hero image."""
    global _AUTH_HERO_DATA_URI_CACHE
    if _AUTH_HERO_DATA_URI_CACHE is not None:
        return _AUTH_HERO_DATA_URI_CACHE

    png_path = os.path.join(os.path.dirname(__file__), "assets", "health_portal_auth_hero.png")
    svg_path = os.path.join(os.path.dirname(__file__), "assets", "health_portal_auth_hero.svg")

    if os.path.exists(png_path):
        with open(png_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            _AUTH_HERO_DATA_URI_CACHE = f"data:image/png;base64,{b64}"
    elif os.path.exists(svg_path):
        with open(svg_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            _AUTH_HERO_DATA_URI_CACHE = f"data:image/svg+xml;base64,{b64}"
    else:
        _AUTH_HERO_DATA_URI_CACHE = ""

    return _AUTH_HERO_DATA_URI_CACHE


def get_auth_hero_b64() -> str:
    """Loads base64 payload for backwards-compatibility."""
    uri = get_auth_hero_data_uri()
    if "," in uri:
        return uri.split(",", 1)[1]
    return uri


def apply_auth_theme():
    """
    Injects custom CSS specifically for the split-screen authentication
    (Login and Registration) pages, matching the reference design in Image 2:
    - Left 46% dark emerald hero panel with cropped DNA double helix & glowing branding.
    - Right 54% clinical light (#F4F7F6) auth panel with centered 350px login/register card.
    - Completely hides Streamlit sidebar and removes all container padding.
    - Custom styled input fields with username and lock left icons.
    - Prominent orange gradient Login button (#FF791F to #FF5722) with rounded corners.
    - Outlined secondary switcher button (Create Account / Back to Login).
    - Corner sparkle accent in bottom right.
    """
    data_uri = get_auth_hero_data_uri()
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', 'Inter', system-ui, -apple-system, sans-serif !important;
    }}

    /* =========================================================================
       1. GLOBAL RESET & FULL-BLEED VIEWPORT (NO GAPS, NO MARGINS)
       ========================================================================= */
    html, body {{
        margin: 0 !important;
        padding: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        overflow-x: hidden !important;
        background-color: #F4F7F6 !important;
    }}

    .stApp,
    [data-testid="stAppViewContainer"],
    section.main,
    .main,
    .block-container,
    [data-testid="stAppViewContainer"] section.main .block-container,
    .main .block-container {{
        background-color: #F4F7F6 !important;
        padding: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
        min-height: 100vh !important;
        overflow-x: hidden !important;
    }}

    /* Transparent top header */
    [data-testid="stHeader"],
    header[data-testid="stHeader"] {{
        background: transparent !important;
        color: #11252D !important;
        z-index: 99 !important;
    }}

    /* Completely hide sidebar on auth pages */
    section[data-testid="stSidebar"],
    [data-testid="collapsedControl"] {{
        display: none !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* Remove gaps from vertical layout block */
    .block-container > [data-testid="stVerticalBlock"],
    .block-container > div > [data-testid="stVerticalBlock"] {{
        gap: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
        min-height: 100vh !important;
    }}

    /* =========================================================================
       2. TOP-LEVEL 46/54 SPLIT-SCREEN LAYOUT (SEAMLESS 0 GAP)
       ========================================================================= */
    /* Target ONLY the root stHorizontalBlock split */
    .block-container > [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"] > [data-testid="stHorizontalBlock"],
    .block-container > [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"],
    .block-container > div > [data-testid="stElementContainer"] > [data-testid="stHorizontalBlock"],
    .block-container > div > [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: stretch !important;
        gap: 0px !important;
        column-gap: 0px !important;
        row-gap: 0px !important;
        --column-gap: 0px !important;
        --gap: 0px !important;
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
        min-height: 100vh !important;
        height: 100vh !important;
        overflow: hidden !important;
    }}

    /* Reset columns under top-level stHorizontalBlock */
    .block-container > [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"] > [data-testid="stHorizontalBlock"] > [data-testid="column"],
    .block-container > [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] > [data-testid="column"],
    .block-container > div > [data-testid="stElementContainer"] > [data-testid="stHorizontalBlock"] > [data-testid="column"],
    .block-container > div > [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
        min-height: 100vh !important;
        height: 100vh !important;
    }}

    /* LEFT HERO PANEL (46% width, exact cropped visual, zero border) */
    .block-container > [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"] > [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child,
    .block-container > [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child,
    .block-container > div > [data-testid="stElementContainer"] > [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child,
    .block-container > div > [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child {{
        flex: 0 0 46% !important;
        width: 46% !important;
        max-width: 46% !important;
        min-width: 46% !important;
        background: #06231C url("{data_uri}") no-repeat center center / cover !important;
        position: relative !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: stretch !important;
        justify-content: stretch !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
    }}

    /* Stretch all child wrappers inside left column */
    .block-container > [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"] > [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child > div,
    .block-container > [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child > div,
    .block-container > div > [data-testid="stElementContainer"] > [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child > div,
    .block-container > div > [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child > div,
    .block-container [data-testid="column"]:first-child [data-testid="stVerticalBlock"],
    .block-container [data-testid="column"]:first-child [data-testid="stElementContainer"],
    .block-container [data-testid="column"]:first-child .stMarkdown,
    .block-container [data-testid="column"]:first-child [data-testid="stMarkdownContainer"] {{
        height: 100% !important;
        min-height: 100vh !important;
        width: 100% !important;
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
        display: flex !important;
        flex-direction: column !important;
        flex: 1 1 100% !important;
    }}

    .auth-hero-container {{
        width: 100% !important;
        height: 100% !important;
        min-height: 100vh !important;
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        overflow: hidden !important;
        position: relative !important;
    }}

    .auth-hero-img {{
        width: 100% !important;
        height: 100% !important;
        min-height: 100vh !important;
        object-fit: cover !important;
        object-position: center center !important;
        display: block !important;
        pointer-events: none !important;
        user-select: none !important;
        border: none !important;
    }}

    /* RIGHT CLINICAL AUTH PANEL (54% width, light clinical, vertically centered) */
    .block-container > [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"] > [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child,
    .block-container > [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child,
    .block-container > div > [data-testid="stElementContainer"] > [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child,
    .block-container > div > [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child {{
        flex: 0 0 54% !important;
        width: 54% !important;
        max-width: 54% !important;
        min-width: 54% !important;
        background-color: #F4F7F6 !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        padding: 20px 40px !important;
        position: relative !important;
        box-sizing: border-box !important;
        overflow-y: auto !important;
        margin: 0 !important;
        border: none !important;
    }}

    /* Centered 350px card container inside right column */
    .block-container [data-testid="column"]:last-child > [data-testid="stVerticalBlock"],
    .block-container [data-testid="column"]:last-child > div > [data-testid="stVerticalBlock"],
    .block-container [data-testid="column"]:last-child > div {{
        width: 350px !important;
        max-width: 350px !important;
        min-width: 300px !important;
        margin: auto !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: stretch !important;
        gap: 0 !important;
    }}

    .block-container [data-testid="column"]:last-child [data-testid="stElementContainer"],
    .block-container [data-testid="column"]:last-child [data-testid="stForm"] {{
        width: 350px !important;
        max-width: 350px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }}

    /* =========================================================================
       3. NESTED SWITCHER ROW RESET
       ========================================================================= */
    [data-testid="column"]:last-child [data-testid="stHorizontalBlock"] {{
        min-height: auto !important;
        height: auto !important;
        width: 350px !important;
        max-width: 350px !important;
        margin: 8px auto 0 auto !important;
        padding: 0 !important;
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
        column-gap: 8px !important;
    }}

    [data-testid="column"]:last-child [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
        min-height: auto !important;
        height: auto !important;
        width: auto !important;
        flex: 1 1 auto !important;
        max-width: none !important;
        min-width: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        background: transparent !important;
    }}

    /* =========================================================================
       4. FORM ELEMENTS STYLING
       ========================================================================= */
    [data-testid="stHorizontalBlock"] [data-testid="stForm"] {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        box-shadow: none !important;
        margin-bottom: 0 !important;
        width: 350px !important;
        max-width: 350px !important;
    }}

    /* Auth Header (Lock Icon + Heading text) */
    .auth-title-container {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 22px;
        width: 350px;
        max-width: 350px;
    }}

    .auth-title-text {{
        color: #11252D !important;
        font-size: 1.55rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }}

    /* Form Field Labels */
    .auth-field-label {{
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        color: #152E27 !important;
        margin-bottom: 6px !important;
        margin-top: 14px !important;
    }}

    /* Input Fields with Inner Icons */
    [data-testid="column"]:last-child [data-testid="stTextInput"] {{
        margin-bottom: 6px !important;
        width: 350px !important;
        max-width: 350px !important;
    }}

    [data-testid="column"]:last-child [data-testid="stTextInputRootElement"] {{
        background-color: #FFFFFF !important;
        border: 1.5px solid #CCDCD5 !important;
        border-radius: 10px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
        height: 46px !important;
        position: relative !important;
        transition: all 0.15s ease !important;
        width: 350px !important;
        max-width: 350px !important;
    }}

    [data-testid="column"]:last-child [data-testid="stTextInputRootElement"]:focus-within {{
        border-color: #0E5C46 !important;
        box-shadow: 0 0 0 3px rgba(14, 92, 70, 0.12) !important;
    }}

    /* User Avatar icon inside Username field */
    [data-testid="column"]:last-child [data-testid="stTextInput"]:has(input[type="text"]) [data-testid="stTextInputRootElement"]::before {{
        content: "";
        position: absolute;
        left: 14px;
        top: 50%;
        transform: translateY(-50%);
        width: 18px;
        height: 18px;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2368857C' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2'/%3E%3Ccircle cx='12' cy='7' r='4'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-size: contain;
        z-index: 3;
        pointer-events: none;
    }}

    [data-testid="column"]:last-child [data-testid="stTextInput"]:has(input[type="text"]) input {{
        padding-left: 42px !important;
        font-size: 0.92rem !important;
        color: #122C24 !important;
        height: 44px !important;
    }}

    /* Padlock icon inside Password field */
    [data-testid="column"]:last-child [data-testid="stTextInput"]:has(input[type="password"]) [data-testid="stTextInputRootElement"]::before {{
        content: "";
        position: absolute;
        left: 14px;
        top: 50%;
        transform: translateY(-50%);
        width: 18px;
        height: 18px;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2368857C' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect width='18' height='11' x='3' y='11' rx='2' ry='2'/%3E%3Cpath d='M7 11V7a5 5 0 0 1 10 0v4'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-size: contain;
        z-index: 3;
        pointer-events: none;
    }}

    [data-testid="column"]:last-child [data-testid="stTextInput"]:has(input[type="password"]) input {{
        padding-left: 42px !important;
        font-size: 0.92rem !important;
        color: #122C24 !important;
        height: 44px !important;
    }}

    /* Full-width Warm Orange Gradient Submit Button */
    [data-testid="column"]:last-child [data-testid="stFormSubmitButton"] {{
        width: 350px !important;
        max-width: 350px !important;
        margin-top: 18px !important;
    }}

    [data-testid="column"]:last-child [data-testid="stFormSubmitButton"] > button {{
        background: linear-gradient(180deg, #FF791F 0%, #FF5722 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        height: 46px !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(255, 121, 31, 0.4) !important;
        transition: all 0.2s ease !important;
    }}

    [data-testid="column"]:last-child [data-testid="stFormSubmitButton"] > button:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 18px rgba(255, 121, 31, 0.5) !important;
    }}

    /* Forgot Password Link (aligned right beneath the button) */
    .auth-forgot-row {{
        text-align: right !important;
        margin-top: 8px !important;
        margin-bottom: 22px !important;
        width: 350px !important;
        max-width: 350px !important;
    }}

    .auth-forgot-link {{
        color: #6B827A !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        text-decoration: none !important;
        transition: color 0.15s ease !important;
    }}

    .auth-forgot-link:hover {{
        color: #0E5C46 !important;
        text-decoration: underline !important;
    }}

    /* Secondary Switcher (Don't have an account? [ Create Account ]) */
    .auth-switch-label-wrap {{
        text-align: right !important;
        color: #1E3832 !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        line-height: 34px !important;
        white-space: nowrap !important;
    }}

    [data-testid="column"]:last-child .stButton {{
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
    }}

    [data-testid="column"]:last-child .stButton > button {{
        background: transparent !important;
        border: 1.5px solid #3B5B51 !important;
        color: #1E3832 !important;
        border-radius: 8px !important;
        padding: 4px 14px !important;
        font-size: 0.84rem !important;
        font-weight: 600 !important;
        box-shadow: none !important;
        height: 34px !important;
        min-height: 34px !important;
        line-height: 1.2 !important;
        transition: all 0.15s ease !important;
        white-space: nowrap !important;
    }}

    [data-testid="column"]:last-child .stButton > button:hover {{
        background: #E5ECE8 !important;
        border-color: #2D4840 !important;
        color: #112520 !important;
        transform: none !important;
        box-shadow: none !important;
    }}

    /* Subtle Corner Sparkle */
    .auth-corner-sparkle {{
        position: fixed !important;
        bottom: 28px !important;
        right: 36px !important;
        pointer-events: none !important;
        z-index: 10 !important;
    }}

    /* Mobile Responsive */
    @media (max-width: 820px) {{
        .block-container > [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"],
        .block-container > div > [data-testid="stHorizontalBlock"] {{
            flex-direction: column !important;
        }}
        .block-container [data-testid="column"]:first-child {{
            width: 100% !important;
            flex: 1 1 auto !important;
            min-height: 320px !important;
            max-width: 100% !important;
        }}
        .block-container [data-testid="column"]:last-child {{
            width: 100% !important;
            flex: 1 1 auto !important;
            min-height: auto !important;
            padding: 30px 20px !important;
            max-width: 100% !important;
        }}
        .block-container [data-testid="column"]:last-child > [data-testid="stVerticalBlock"],
        .block-container [data-testid="column"]:last-child > div > [data-testid="stVerticalBlock"],
        .block-container [data-testid="column"]:last-child > div,
        .block-container [data-testid="column"]:last-child [data-testid="stElementContainer"],
        .block-container [data-testid="column"]:last-child [data-testid="stForm"],
        .auth-title-container,
        .auth-forgot-row,
        [data-testid="column"]:last-child [data-testid="stTextInput"],
        [data-testid="column"]:last-child [data-testid="stTextInputRootElement"],
        [data-testid="column"]:last-child [data-testid="stFormSubmitButton"],
        [data-testid="column"]:last-child [data-testid="stHorizontalBlock"] {{
            width: 100% !important;
            max-width: 100% !important;
        }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_auth_left_panel():
    """
    Renders the emerald hero left panel using an HTML img tag with base64 data URI
    and background-image to ensure 100% reliable full-bleed rendering without markdown bugs.
    """
    data_uri = get_auth_hero_data_uri()
    st.markdown(
        f'<div class="auth-hero-container"><img src="{data_uri}" class="auth-hero-img" alt="Health Portal Multi-Disease Detection System" /></div>',
        unsafe_allow_html=True,
    )


