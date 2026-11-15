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


def apply_auth_theme():
    """
    Injects custom CSS specifically for the split-screen authentication
    (Login and Registration) pages, matching the reference design:
    - Left 50% dark emerald hero panel with DNA double helix & glowing branding.
    - Right 50% clinical light (#F4F7F6) auth panel with centered login/register card.
    - Hides Streamlit sidebar and collapses container padding to full-bleed.
    - Custom styled input fields with username and lock left icons.
    - Full-width coral-orange action button (#FF6F59 -> #FA573E).
    - Outlined secondary switcher button (Create Account / Back to Login).
    - Corner sparkle accent in bottom right.
    """
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', system-ui, -apple-system, sans-serif !important;
    }

    /* 1. Reset App Background & Hide Sidebar */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #F4F7F6 !important;
        overflow-x: hidden !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
        z-index: 99 !important;
    }

    section[data-testid="stSidebar"],
    [data-testid="collapsedControl"] {
        display: none !important;
        width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 2. Full-bleed Block Container */
    .block-container {
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* 3. Two-Column 50/50 Split Viewport */
    [data-testid="stHorizontalBlock"] {
        min-height: 100vh !important;
        margin: 0 !important;
        padding: 0 !important;
        gap: 0 !important;
        display: flex !important;
        flex-direction: row !important;
        align-items: stretch !important;
    }

    /* Left Column: Dark Emerald Hero Panel */
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child {
        min-height: 100vh !important;
        width: 50% !important;
        flex: 1 1 50% !important;
        background: linear-gradient(155deg, #06231C 0%, #0A3D30 45%, #07221B 100%) !important;
        position: relative !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: stretch !important;
        padding: 0 !important;
        overflow: hidden !important;
    }

    [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child > div {
        height: 100% !important;
        width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Right Column: Light Clinical Auth Form */
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child {
        min-height: 100vh !important;
        width: 50% !important;
        flex: 1 1 50% !important;
        background-color: #F4F7F6 !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        padding: 40px 60px !important;
        position: relative !important;
        box-sizing: border-box !important;
    }

    /* Constrain the form width in right column */
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child > div,
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child [data-testid="stVerticalBlock"] {
        max-width: 430px !important;
        width: 100% !important;
        margin: auto !important;
    }

    /* 4. Remove default Streamlit Form borders & padding */
    [data-testid="stHorizontalBlock"] [data-testid="stForm"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        box-shadow: none !important;
        margin-bottom: 0 !important;
    }

    /* 5. Auth Header */
    .auth-title-container {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 24px;
    }

    .auth-title-text {
        color: #11252D !important;
        font-size: 1.7rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }

    /* 6. Form Field Labels */
    .auth-field-label {
        font-size: 0.92rem;
        font-weight: 600;
        color: #152E27;
        margin-bottom: 6px;
        margin-top: 14px;
    }

    /* 7. Input Fields with Inner Icons */
    [data-testid="stHorizontalBlock"] [data-testid="stTextInput"] {
        margin-bottom: 8px !important;
    }

    [data-testid="stHorizontalBlock"] [data-testid="stTextInputRootElement"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CCDCD5 !important;
        border-radius: 10px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
        height: 48px !important;
        position: relative !important;
        transition: all 0.15s ease !important;
    }

    [data-testid="stHorizontalBlock"] [data-testid="stTextInputRootElement"]:focus-within {
        border-color: #0E5C46 !important;
        box-shadow: 0 0 0 3px rgba(14, 92, 70, 0.12) !important;
    }

    /* User Avatar icon inside Username field */
    [data-testid="stHorizontalBlock"] [data-testid="stTextInput"]:has(input[type="text"]) [data-testid="stTextInputRootElement"]::before {
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
    }

    [data-testid="stHorizontalBlock"] [data-testid="stTextInput"]:has(input[type="text"]) input {
        padding-left: 42px !important;
        font-size: 0.95rem !important;
        color: #122C24 !important;
        height: 46px !important;
    }

    /* Padlock icon inside Password field */
    [data-testid="stHorizontalBlock"] [data-testid="stTextInput"]:has(input[type="password"]) [data-testid="stTextInputRootElement"]::before {
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
    }

    [data-testid="stHorizontalBlock"] [data-testid="stTextInput"]:has(input[type="password"]) input {
        padding-left: 42px !important;
        font-size: 0.95rem !important;
        color: #122C24 !important;
        height: 46px !important;
    }

    /* 8. Full-width Coral Submit Button */
    [data-testid="stHorizontalBlock"] [data-testid="stFormSubmitButton"] {
        width: 100% !important;
        margin-top: 14px !important;
    }

    [data-testid="stHorizontalBlock"] [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #FF6F59 0%, #FA573E 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        height: 48px !important;
        width: 100% !important;
        box-shadow: 0 4px 14px rgba(255, 111, 89, 0.4) !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stHorizontalBlock"] [data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 18px rgba(255, 111, 89, 0.5) !important;
    }

    /* 9. Forgot Password Link */
    .auth-forgot-row {
        text-align: right;
        margin-top: 8px;
        margin-bottom: 24px;
    }

    .auth-forgot-link {
        color: #648278 !important;
        font-size: 0.86rem !important;
        font-weight: 500 !important;
        text-decoration: none !important;
        transition: color 0.15s ease;
    }

    .auth-forgot-link:hover {
        color: #0E5C46 !important;
        text-decoration: underline !important;
    }

    /* 10. Secondary Switcher (Don't have an account? [ Create Account ]) */
    .auth-switch-label-wrap {
        text-align: right;
        color: #1E3832;
        font-size: 0.92rem;
        font-weight: 500;
        line-height: 34px;
    }

    [data-testid="stHorizontalBlock"] .stButton {
        display: flex !important;
        align-items: center !important;
    }

    [data-testid="stHorizontalBlock"] .stButton > button {
        background: transparent !important;
        border: 1.5px solid #486E63 !important;
        color: #1E3832 !important;
        border-radius: 8px !important;
        padding: 4px 14px !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        box-shadow: none !important;
        height: 34px !important;
        min-height: 34px !important;
        line-height: 1.2 !important;
        transition: all 0.15s ease !important;
    }

    [data-testid="stHorizontalBlock"] .stButton > button:hover {
        background: #E5ECE8 !important;
        border-color: #385B51 !important;
        color: #112520 !important;
        transform: none !important;
        box-shadow: none !important;
    }

    /* 11. Subtle Corner Sparkle */
    .auth-corner-sparkle {
        position: fixed !important;
        bottom: 28px !important;
        right: 36px !important;
        pointer-events: none !important;
        z-index: 10 !important;
    }

    /* Mobile Responsive */
    @media (max-width: 820px) {
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child {
            width: 100% !important;
            min-height: 360px !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child {
            width: 100% !important;
            min-height: auto !important;
            padding: 30px 20px !important;
        }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_auth_left_panel():
    """Renders the emerald hero left panel using st.components.v1.html
    to bypass Streamlit HTML sanitisation which strips SVG elements.
    """
    import streamlit.components.v1 as components
    _html = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body { width:100%; height:100%; overflow:hidden;
    background:linear-gradient(155deg,#06231C 0%,#0A3D30 45%,#07221B 100%); }
  .panel { width:100%; height:100vh; position:relative; overflow:hidden; }
  svg.hs { position:absolute; top:0; left:0; width:100%; height:100%; }
</style>
</head>
<body>
<div class="panel">
<svg class="hs" viewBox="0 0 540 800" preserveAspectRatio="xMidYMid slice"
     xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"   stop-color="#06231C"/>
      <stop offset="45%"  stop-color="#0A3E31"/>
      <stop offset="100%" stop-color="#07221B"/>
    </linearGradient>
    <radialGradient id="hg" cx="50%" cy="38%" r="58%">
      <stop offset="0%"   stop-color="#5ECFB0" stop-opacity="0.65"/>
      <stop offset="100%" stop-color="#1A6E5A" stop-opacity="0.25"/>
    </radialGradient>
    <radialGradient id="vig" cx="50%" cy="50%" r="70%">
      <stop offset="0%"   stop-color="transparent"/>
      <stop offset="100%" stop-color="#030F0B" stop-opacity="0.5"/>
    </radialGradient>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="sg" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect width="540" height="800" fill="url(#bg)"/>
  <rect width="540" height="800" fill="url(#vig)"/>

  <!-- Bokeh -->
  <circle cx="85"  cy="130" r="3"   fill="#2EE5B8" opacity="0.4"/>
  <circle cx="470" cy="260" r="2"   fill="#2EE5B8" opacity="0.3"/>
  <circle cx="75"  cy="500" r="2.5" fill="#2EE5B8" opacity="0.35"/>
  <circle cx="430" cy="700" r="3"   fill="#2EE5B8" opacity="0.3"/>
  <circle cx="190" cy="750" r="2"   fill="#2EE5B8" opacity="0.25"/>
  <circle cx="340" cy="80"  r="2.5" fill="#2EE5B8" opacity="0.28"/>
  <circle cx="510" cy="460" r="2"   fill="#2EE5B8" opacity="0.22"/>

  <!-- DNA helix -->
  <g opacity="0.9">
    <line x1="50.0" y1="840.0" x2="50.0" y2="840.0" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.34"/>
        <circle cx="50.0" cy="840.0" r="3.5" fill="#2EE5B8" fill-opacity="0.44"/>
        <circle cx="50.0" cy="840.0" r="3.5" fill="#2EE5B8" fill-opacity="0.44"/>
        <line x1="88.3" y1="809.1" x2="50.8" y2="790.9" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.31"/>
        <circle cx="88.3" cy="809.1" r="3.5" fill="#2EE5B8" fill-opacity="0.41"/>
        <circle cx="50.8" cy="790.9" r="3.5" fill="#2EE5B8" fill-opacity="0.41"/>
        <line x1="120.4" y1="775.3" x2="57.8" y2="744.7" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.23"/>
        <circle cx="120.4" cy="775.3" r="3.5" fill="#2EE5B8" fill-opacity="0.33"/>
        <circle cx="57.8" cy="744.7" r="3.5" fill="#2EE5B8" fill-opacity="0.33"/>
        <line x1="142.3" y1="736.4" x2="75.0" y2="703.6" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.19"/>
        <circle cx="142.3" cy="736.4" r="3.5" fill="#2EE5B8" fill-opacity="0.29"/>
        <circle cx="75.0" cy="703.6" r="3.5" fill="#2EE5B8" fill-opacity="0.29"/>
        <line x1="153.2" y1="692.2" x2="103.2" y2="667.8" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.28"/>
        <circle cx="153.2" cy="692.2" r="3.5" fill="#2EE5B8" fill-opacity="0.38"/>
        <circle cx="103.2" cy="667.8" r="3.5" fill="#2EE5B8" fill-opacity="0.38"/>
        <line x1="155.9" y1="644.0" x2="139.6" y2="636.0" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.33"/>
        <circle cx="155.9" cy="644.0" r="3.5" fill="#2EE5B8" fill-opacity="0.43"/>
        <circle cx="139.6" cy="636.0" r="3.5" fill="#2EE5B8" fill-opacity="0.43"/>
        <line x1="155.9" y1="594.5" x2="178.6" y2="605.5" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.33"/>
        <circle cx="155.9" cy="594.5" r="3.5" fill="#2EE5B8" fill-opacity="0.43"/>
        <circle cx="178.6" cy="605.5" r="3.5" fill="#2EE5B8" fill-opacity="0.43"/>
        <line x1="159.7" y1="546.7" x2="213.9" y2="573.3" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.27"/>
        <circle cx="159.7" cy="546.7" r="3.5" fill="#2EE5B8" fill-opacity="0.37"/>
        <circle cx="213.9" cy="573.3" r="3.5" fill="#2EE5B8" fill-opacity="0.37"/>
        <line x1="172.3" y1="503.4" x2="240.4" y2="536.6" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.17"/>
        <circle cx="172.3" cy="503.4" r="3.5" fill="#2EE5B8" fill-opacity="0.27"/>
        <circle cx="240.4" cy="536.6" r="3.5" fill="#2EE5B8" fill-opacity="0.27"/>
        <line x1="196.1" y1="465.4" x2="255.7" y2="494.6" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.25"/>
        <circle cx="196.1" cy="465.4" r="3.5" fill="#2EE5B8" fill-opacity="0.35"/>
        <circle cx="255.7" cy="494.6" r="3.5" fill="#2EE5B8" fill-opacity="0.35"/>
        <line x1="229.6" y1="432.2" x2="261.3" y2="447.8" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.32"/>
        <circle cx="229.6" cy="432.2" r="3.5" fill="#2EE5B8" fill-opacity="0.42"/>
        <circle cx="261.3" cy="447.8" r="3.5" fill="#2EE5B8" fill-opacity="0.42"/>
        <line x1="268.3" y1="401.6" x2="261.7" y2="398.4" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.34"/>
        <circle cx="268.3" cy="401.6" r="3.5" fill="#2EE5B8" fill-opacity="0.44"/>
        <circle cx="261.7" cy="398.4" r="3.5" fill="#2EE5B8" fill-opacity="0.44"/>
        <line x1="305.9" y1="370.4" x2="263.2" y2="349.6" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.30"/>
        <circle cx="305.9" cy="370.4" r="3.5" fill="#2EE5B8" fill-opacity="0.40"/>
        <circle cx="263.2" cy="349.6" r="3.5" fill="#2EE5B8" fill-opacity="0.40"/>
        <line x1="336.6" y1="335.9" x2="271.6" y2="304.1" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.22"/>
        <circle cx="336.6" cy="335.9" r="3.5" fill="#2EE5B8" fill-opacity="0.32"/>
        <circle cx="271.6" cy="304.1" r="3.5" fill="#2EE5B8" fill-opacity="0.32"/>
        <line x1="356.6" y1="296.1" x2="290.7" y2="263.9" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.21"/>
        <circle cx="356.6" cy="296.1" r="3.5" fill="#2EE5B8" fill-opacity="0.31"/>
        <circle cx="290.7" cy="263.9" r="3.5" fill="#2EE5B8" fill-opacity="0.31"/>
        <line x1="365.8" y1="251.1" x2="320.5" y2="228.9" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.29"/>
        <circle cx="365.8" cy="251.1" r="3.5" fill="#2EE5B8" fill-opacity="0.39"/>
        <circle cx="320.5" cy="228.9" r="3.5" fill="#2EE5B8" fill-opacity="0.39"/>
        <line x1="367.7" y1="202.4" x2="357.8" y2="197.6" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.34"/>
        <circle cx="367.7" cy="202.4" r="3.5" fill="#2EE5B8" fill-opacity="0.44"/>
        <circle cx="357.8" cy="197.6" r="3.5" fill="#2EE5B8" fill-opacity="0.44"/>
        <line x1="367.9" y1="153.0" x2="396.7" y2="167.0" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.32"/>
        <circle cx="367.9" cy="153.0" r="3.5" fill="#2EE5B8" fill-opacity="0.42"/>
        <circle cx="396.7" cy="167.0" r="3.5" fill="#2EE5B8" fill-opacity="0.42"/>
        <line x1="372.8" y1="105.8" x2="430.8" y2="134.2" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.25"/>
        <circle cx="372.8" cy="105.8" r="3.5" fill="#2EE5B8" fill-opacity="0.35"/>
        <circle cx="430.8" cy="134.2" r="3.5" fill="#2EE5B8" fill-opacity="0.35"/>
        <line x1="387.2" y1="63.3" x2="455.5" y2="96.7" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.16"/>
        <circle cx="387.2" cy="63.3" r="3.5" fill="#2EE5B8" fill-opacity="0.26"/>
        <circle cx="455.5" cy="96.7" r="3.5" fill="#2EE5B8" fill-opacity="0.26"/>
        <line x1="412.8" y1="26.3" x2="469.0" y2="53.7" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.26"/>
        <circle cx="412.8" cy="26.3" r="3.5" fill="#2EE5B8" fill-opacity="0.36"/>
        <circle cx="469.0" cy="53.7" r="3.5" fill="#2EE5B8" fill-opacity="0.36"/>
        <line x1="447.6" y1="-6.3" x2="473.3" y2="6.3" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.33"/>
        <circle cx="447.6" cy="-6.3" r="3.5" fill="#2EE5B8" fill-opacity="0.43"/>
        <circle cx="473.3" cy="6.3" r="3.5" fill="#2EE5B8" fill-opacity="0.43"/>
        <line x1="486.6" y1="-36.8" x2="473.4" y2="-43.2" stroke="#2CD5A3" stroke-width="2" stroke-opacity="0.34"/>
        <circle cx="486.6" cy="-36.8" r="3.5" fill="#2EE5B8" fill-opacity="0.44"/>
        <circle cx="473.4" cy="-43.2" r="3.5" fill="#2EE5B8" fill-opacity="0.44"/>
    <path d="M 50.0,840.0 L 88.3,809.1 L 120.4,775.3 L 142.3,736.4 L 153.2,692.2 L 155.9,644.0 L 155.9,594.5 L 159.7,546.7 L 172.3,503.4 L 196.1,465.4 L 229.6,432.2 L 268.3,401.6 L 305.9,370.4 L 336.6,335.9 L 356.6,296.1 L 365.8,251.1 L 367.7,202.4 L 367.9,153.0 L 372.8,105.8 L 387.2,63.3 L 412.8,26.3 L 447.6,-6.3 L 486.6,-36.8" fill="none" stroke="#2EE5B8" stroke-width="2.5" stroke-opacity="0.35"/>
    <path d="M 50.0,840.0 L 50.8,790.9 L 57.8,744.7 L 75.0,703.6 L 103.2,667.8 L 139.6,636.0 L 178.6,605.5 L 213.9,573.3 L 240.4,536.6 L 255.7,494.6 L 261.3,447.8 L 261.7,398.4 L 263.2,349.6 L 271.6,304.1 L 290.7,263.9 L 320.5,228.9 L 357.8,197.6 L 396.7,167.0 L 430.8,134.2 L 455.5,96.7 L 469.0,53.7 L 473.3,6.3 L 473.4,-43.2" fill="none" stroke="#2EE5B8" stroke-width="2.5" stroke-opacity="0.35"/>
  </g>

  <!-- Cross badge top-right -->
  <g transform="translate(368,115)">
    <rect width="68" height="68" rx="18" fill="#0A3028" fill-opacity="0.75" stroke="#1E7A5E" stroke-width="1.5"/>
    <path d="M34 20 V48 M20 34 H48" stroke="#2DE3B4" stroke-width="5" stroke-linecap="round" filter="url(#sg)"/>
  </g>

  <!-- Cross badge bottom-left -->
  <g transform="translate(66,636)">
    <rect width="56" height="56" rx="15" fill="#0A3028" fill-opacity="0.75" stroke="#1E7A5E" stroke-width="1.5"/>
    <path d="M28 16 V40 M16 28 H40" stroke="#2DE3B4" stroke-width="4.5" stroke-linecap="round" filter="url(#sg)"/>
  </g>

  <!-- Heart badge upper-left -->
  <g transform="translate(96,224)">
    <rect width="68" height="58" rx="15" fill="#fff" fill-opacity="0.05"
          stroke="#fff" stroke-opacity="0.14" stroke-width="1"/>
    <path d="M34 42 C34 42 12 29 12 18 C12 11 17 7 24 7 C28 7 32 10 34 13
             C36 10 40 7 44 7 C51 7 56 11 56 18 C56 29 34 42 34 42 Z"
          fill="url(#hg)" stroke="#78D5B8" stroke-width="1.4"
          stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M6 28 H17 L21 21 L26 33 L30 28 H46" fill="none"
          stroke="#2DE3B4" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <!-- Heart badge lower-right -->
  <g transform="translate(306,574)">
    <rect width="100" height="82" rx="20" fill="#fff" fill-opacity="0.05"
          stroke="#fff" stroke-opacity="0.14" stroke-width="1"/>
    <path d="M50 60 C50 60 20 42 20 26 C20 16 27 10 36 10 C43 10 48 14 50 18
             C52 14 57 10 64 10 C73 10 80 16 80 26 C80 42 50 60 50 60 Z"
          fill="url(#hg)" stroke="#78D5B8" stroke-width="1.6"
          stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M4 36 H24 L30 25 L38 46 L44 36 H76 L81 29 L86 36 H98" fill="none"
          stroke="#2DE3B4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <!-- Center branding -->
  <g transform="translate(270,410)">
    <g transform="translate(-34,-92)" filter="url(#glow)">
      <path d="M34 64 C34 64 62 46 62 24 C62 12 52 4 42 4 C36 4 34 8 34 8
               C34 8 32 4 26 4 C16 4 6 12 6 24 C6 46 34 64 34 64 Z"
            fill="#0C4035" stroke="#2DE3B4" stroke-width="2.5"/>
      <path d="M34 44 C34 44 18 34 18 25 C18 19 23 15 28 15 C31 15 33 17 34 19
               C35 17 37 15 40 15 C45 15 50 19 50 25 C50 34 34 44 34 44 Z"
            fill="none" stroke="#2DE3B4" stroke-width="2.2"
            stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M18 30 H24 L28 22 L34 38 L38 30 H50" fill="none"
            stroke="#2DE3B4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    <text x="0" y="22" fill="#FFFFFF"
          font-family="'Plus Jakarta Sans',system-ui,-apple-system,sans-serif"
          font-size="36" font-weight="800" text-anchor="middle"
          letter-spacing="-0.5">Health Portal</text>
    <text x="0" y="52" fill="#8CD6BC"
          font-family="'Plus Jakarta Sans',system-ui,-apple-system,sans-serif"
          font-size="15.5" font-weight="400" text-anchor="middle"
          letter-spacing="0.3">Multi-Disease Detection System</text>
  </g>
</svg>
</div>
</body>
</html>"""
    components.html(_html, height=700, scrolling=False)

