import json
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import theme
from data import DEFAULT_DATASET_PATH
from train import train_pipeline
from explain import (
    check_red_flags,
    check_weak_input,
    compute_leave_one_out_importance,
    build_top3_chart,
    build_importance_chart,
)
from auth import (
    register_user,
    authenticate_user,
    save_assessment,
    get_user_assessments,
)
from precautions import get_precautions_for_disease
from report import generate_pdf_report



# Must be first Streamlit command!
st.set_page_config(page_title="Disease Management Predictor", page_icon="🩺", layout="wide")

# -------- Session state for login, theme, register page toggle --------
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"
if "show_register" not in st.session_state:
    st.session_state["show_register"] = False

# Dispatch appropriate theme based on authentication state
if not st.session_state.get("user_id"):
    theme.apply_auth_theme()
else:
    theme.apply_custom_theme(st.session_state["theme"])

# -------- Settings page (theme selection) --------
def settings_page():
    theme.render_banner("Settings", "Configure theme preferences for your workspace.", "⚙️")
    theme_choice = st.selectbox("Choose theme", ["dark", "light"], index=(0 if st.session_state["theme"] == "dark" else 1))
    if theme_choice != st.session_state["theme"]:
        st.session_state["theme"] = theme_choice
        st.rerun()
    st.write(f"Current theme: **{st.session_state['theme']}**")

# -------- Register (create account) page --------
def register_page():
    col_left, col_right = st.columns([46, 54], gap=None)

    with col_left:
        theme.render_auth_left_panel()

    with col_right:
        # Title with Lock Icon matching reference design
        st.markdown(
            """
            <div class="auth-title-container">
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#11252D" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
                <span class="auth-title-text">Create Account</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("register_form", border=False):
            st.markdown('<div class="auth-field-label">Username</div>', unsafe_allow_html=True)
            new_username = st.text_input("Username", placeholder="Enter your username", label_visibility="collapsed")

            st.markdown('<div class="auth-field-label">Password (minimum 8 characters)</div>', unsafe_allow_html=True)
            new_password = st.text_input("Password", type="password", placeholder="At least 8 characters", label_visibility="collapsed")

            submit = st.form_submit_button("Create Account", use_container_width=True)
            if submit:
                success, msg = register_user(new_username, new_password)
                if success:
                    st.success(msg)
                    st.session_state["show_register"] = False
                    st.rerun()
                else:
                    st.error(msg)

        st.markdown('<div style="height: 18px;"></div>', unsafe_allow_html=True)

        # Switcher: Already have an account? [ Back to Login ]
        col_lbl, col_btn = st.columns([1.1, 1], gap="small")
        with col_lbl:
            st.markdown('<div class="auth-switch-label-wrap">Already have an account?</div>', unsafe_allow_html=True)
        with col_btn:
            if st.button("Back to Login", key="btn_to_login"):
                st.session_state["show_register"] = False
                st.rerun()

        # Corner sparkle
        st.markdown(
            """
            <div class="auth-corner-sparkle">
                <svg width="44" height="44" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 0C12 6.627 6.627 12 0 12C6.627 12 12 17.373 12 24C12 17.373 17.373 12 24 12C17.373 12 12 6.627 12 0Z" fill="#C5DCD1" opacity="0.45"/>
                </svg>
            </div>
            """,
            unsafe_allow_html=True,
        )

# -------- Login page --------
def login_page():
    col_left, col_right = st.columns([46, 54], gap=None)

    with col_left:
        theme.render_auth_left_panel()

    with col_right:
        # Title with Solid Lock Icon matching reference design
        st.markdown(
            """
            <div class="auth-title-container">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="4" y="10" width="16" height="12" rx="3" fill="#11252D"/>
                    <path d="M7 10V6.5C7 3.73858 9.23858 1.5 12 1.5C14.7614 1.5 17 3.73858 17 6.5V10" stroke="#11252D" stroke-width="3" stroke-linecap="round"/>
                    <circle cx="12" cy="15" r="1.5" fill="#FFFFFF"/>
                    <path d="M12 16.5V18.5" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
                <span class="auth-title-text">Login to Health Portal</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("login_form", border=False):
            st.markdown('<div class="auth-field-label">Username</div>', unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Enter your username", label_visibility="collapsed")

            st.markdown('<div class="auth-field-label">Password</div>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", placeholder="••••••••", label_visibility="collapsed")

            submit = st.form_submit_button("Login", use_container_width=True)
            if submit:
                user = authenticate_user(username, password)
                if user is not None:
                    st.session_state["user_id"] = user["id"]
                    st.session_state["username"] = user["username"]
                    st.session_state["show_register"] = False
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        st.markdown(
            """
            <div class="auth-forgot-row">
                <a href="#" class="auth-forgot-link">Forgot password?</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Switcher: Don't have an account? [ Create Account ]
        col_lbl, col_btn = st.columns([1.1, 1], gap="small")
        with col_lbl:
            st.markdown('<div class="auth-switch-label-wrap">Don\'t have an account?</div>', unsafe_allow_html=True)
        with col_btn:
            if st.button("Create Account", key="btn_to_reg"):
                st.session_state["show_register"] = True
                st.rerun()

        # Corner sparkle
        st.markdown(
            """
            <div class="auth-corner-sparkle">
                <svg width="44" height="44" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 0C12 6.627 6.627 12 0 12C6.627 12 12 17.373 12 24C12 17.373 17.373 12 24 12C17.373 12 12 6.627 12 0Z" fill="#C5DCD1" opacity="0.45"/>
                </svg>
            </div>
            """,
            unsafe_allow_html=True,
        )

# -------- Cached Model Loader --------
@st.cache_resource
def get_app_models(dataset_path: str = DEFAULT_DATASET_PATH):
    return train_pipeline(dataset_path=dataset_path, force=False)

# -------- Dashboard (prediction) page --------
def dashboard_page():
    # 1. Main Header with Stethoscope and Botanical Leaves Artwork
    theme.render_header(
        "Multi-Disease Detection System",
        "AI-powered diagnosis for multiple diseases from patient data and symptoms",
    )

    # 2. Four Disease Category Pills (Lung, Heart, Brain, Kidney)
    theme.render_category_pills()

    # 3. Rich Emerald Hero Banner with AI Chip
    theme.render_hero_banner(
        "Disease Management Predictor",
        "Enter patient details, select symptoms, and get an ensemble prediction across multiple ML models.",
    )

    DEFAULT_PATH = "pro_disease_dataset.csv"
    uploaded = st.file_uploader("Upload disease dataset (CSV) or use default bundled file", type=["csv"])
    if uploaded is not None:
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
                tmp.write(uploaded.getvalue())
                dataset_path = tmp.name
        except Exception as e:
            st.error(f"Could not read uploaded CSV: {e}")
            st.stop()
    else:
        dataset_path = DEFAULT_PATH

    models, ensemble, symptom_cols, classes, metrics = get_app_models(dataset_path)

    # Metrics expander
    with st.expander("Model Validation & performance metrics"):
        st.markdown("#### Model Performance Summary")
        st.write("Validation scores on hold-out test set (stratified 20%) and 5-fold cross-validation:")
        summary_rows = []
        for m_name in ["Logistic Regression", "Random Forest", "SVC", "Ensemble"]:
            m_info = metrics["models"][m_name]
            st.write(f"- **{m_name}** accuracy: {m_info['holdout_accuracy']:.3f} (CV: {m_info['cv_accuracy_mean']:.3f} ± {m_info['cv_accuracy_std']:.3f})")
            summary_rows.append({
                "Model": m_name,
                "Hold-out Accuracy": f"{m_info['holdout_accuracy']:.3f}",
                "Hold-out Macro F1": f"{m_info['holdout_macro_f1']:.3f}",
                "5-Fold CV Accuracy": f"{m_info['cv_accuracy_mean']:.3f} ± {m_info['cv_accuracy_std']:.3f}",
                "5-Fold CV Macro F1": f"{m_info['cv_macro_f1_mean']:.3f} ± {m_info['cv_macro_f1_std']:.3f}",
            })
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

        st.markdown("#### Per-Disease Classification Metrics (Ensemble)")
        ens_per_disease = metrics["models"]["Ensemble"]["per_disease"]
        disease_rows = []
        for d_name, d_scores in ens_per_disease.items():
            disease_rows.append({
                "Disease": d_name,
                "Precision": f"{d_scores['precision']:.3f}",
                "Recall": f"{d_scores['recall']:.3f}",
                "F1-Score": f"{d_scores['f1']:.3f}",
                "Support": d_scores["support"],
            })
        st.dataframe(pd.DataFrame(disease_rows), use_container_width=True, hide_index=True)

        st.markdown("#### Confusion Matrix Heatmap (Ensemble)")
        cm = metrics["models"]["Ensemble"]["confusion_matrix"]
        cm_data = []
        for i, actual in enumerate(classes):
            for j, predicted in enumerate(classes):
                cm_data.append({
                    "Actual": actual,
                    "Predicted": predicted,
                    "Count": cm[i][j],
                })
        df_cm = pd.DataFrame(cm_data)
        base = alt.Chart(df_cm).encode(
            x=alt.X("Predicted:N", title="Predicted Disease", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("Actual:N", title="Actual Disease", sort=list(classes)),
        )
        heatmap = base.mark_rect().encode(
            color=alt.Color("Count:Q", scale=alt.Scale(scheme="greens"), legend=alt.Legend(title="Count")),
            tooltip=["Actual", "Predicted", "Count"]
        )
        text = base.mark_text(baseline="middle").encode(
            text="Count:Q",
            color=alt.condition(alt.datum.Count > df_cm["Count"].max() / 2, alt.value("white"), alt.value("black"))
        )
        st.altair_chart((heatmap + text).properties(height=380), use_container_width=True)

    # Prediction form matching Target UI
    with st.form("patient_form"):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Patient name", placeholder="Enter patient name", max_chars=50)
        with col2:
            age = st.number_input("Age", min_value=0, max_value=120, value=25, step=1)
        selected = st.multiselect("Select your symptoms", options=symptom_cols, default=[], placeholder="Choose options")
        
        btn_col, hint_col = st.columns([1, 4])
        with btn_col:
            submitted = st.form_submit_button("✦ Predict")
        with hint_col:
            st.markdown(
                '<div style="padding-top: 10px; color: #55726B; font-size: 0.88rem; font-weight: 500;">'
                '| &nbsp; ⓘ Fill the form and click Predict to see results.'
                '</div>',
                unsafe_allow_html=True
            )

    if submitted:
        # 1. Red-flag emergency detection (evaluated regardless of model confidence)
        has_red_flags, red_flag_triggers = check_red_flags(selected)
        if has_red_flags:
            st.error("🚨 **These symptoms can indicate an emergency. Seek urgent medical care.**")
            with st.expander("⚠️ Identified Emergency Risk Pattern(s)", expanded=True):
                for rule_desc in red_flag_triggers:
                    st.write(f"- {rule_desc}")
                st.caption(
                    "If you or the patient are experiencing acute chest pain, severe shortness of breath, "
                    "or sudden collapse, call emergency medical services immediately."
                )

        # 2. Model inference
        x_input = pd.DataFrame([[1 if c in selected else 0 for c in symptom_cols]], columns=symptom_cols)
        sample_res = ensemble.predict_sample(x_input)
        final_pred = sample_res["final_prediction"]
        confidence = sample_res["confidence"]
        top3 = sample_res["top3"]
        pred_log = sample_res["individual_preds"]["Logistic Regression"]
        pred_rf = sample_res["individual_preds"]["Random Forest"]
        pred_svc = sample_res["individual_preds"]["SVC"]

        st.subheader("Results")
        st.write(f"*Patient:* {username if username else 'Anonymous'} | *Age:* {int(age)}")
        st.write(f"*Selected symptoms:* {', '.join(selected) if selected else 'None'}")

        # 3. Weak-input safety guard
        is_weak, weak_msg = check_weak_input(selected, confidence)
        importance_data = []

        if is_weak:
            st.warning("⚠️ **Not enough information**")
            st.info(
                f"{weak_msg}\n\n"
                "*Suggestion:* Please add more symptoms for a more reliable differential, "
                "or consult a qualified healthcare professional."
            )
            recorded_prediction = "Not enough information"
        else:
            recorded_prediction = final_pred
            cols = st.columns(3)
            cols[0].metric("Logistic Regression", str(pred_log))
            cols[1].metric("Random Forest", str(pred_rf))
            cols[2].metric("SVC", str(pred_svc))
            st.success(f"🎯 **Final prediction (soft-voting ensemble):** {final_pred} (Confidence: {confidence:.1%})")

            # Top 3 diseases horizontal bar chart (Altair)
            st.markdown("#### Top 3 Disease Candidates")
            st.altair_chart(build_top3_chart(top3), use_container_width=True)

            # Leave-one-symptom-out feature attribution
            st.markdown("#### Symptom Attribution (Leave-One-Symptom-Out)")
            st.caption("Marginal probability drop when each selected symptom is excluded:")
            importance_data = compute_leave_one_out_importance(
                ensemble=ensemble,
                selected_symptoms=selected,
                symptom_cols=symptom_cols,
                top_class=final_pred,
                baseline_confidence=confidence,
            )
            if importance_data:
                st.altair_chart(build_importance_chart(importance_data), use_container_width=True)

            st.divider()
            st.subheader(f"Recommended Precautions ({final_pred})")
            precautions_info = get_precautions_for_disease(final_pred)
            for tip in precautions_info.get("precautions", []):
                st.write(f"- {tip}")
            when_care = precautions_info.get("when_to_seek_care")
            if when_care:
                st.warning(f"**When to seek immediate care:** {when_care}")

        with st.expander("Model probabilities (if available)"):
            for m_name, proba_dict in sample_res["individual_probas"].items():
                st.write(f"**{m_name}**")
                st.write({k: round(float(v), 3) for k, v in proba_dict.items()})
            st.write("**Ensemble (Soft-Voting)**")
            st.write({k: round(float(v), 3) for k, v in sample_res["all_probas"].items()})

        # --- Downloadable PDF Clinical Report ---
        st.divider()
        report_precautions = get_precautions_for_disease(recorded_prediction)
        pdf_bytes = generate_pdf_report(
            patient_name=username if username else "Anonymous",
            age=int(age),
            symptoms=selected,
            top_prediction=recorded_prediction,
            confidence=confidence,
            top3=top3,
            contributing_symptoms=importance_data if not is_weak else [],
            precautions_info=report_precautions,
            red_flag_info=(has_red_flags, red_flag_triggers),
        )
        st.download_button(
            label="📄 Download Assessment Report (PDF)",
            data=pdf_bytes,
            file_name=f"Clinical_Report_{username if username else 'Patient'}.pdf",
            mime="application/pdf",
        )

        st.info("*Note:* This tool is for educational purposes and not a medical diagnosis. Please consult a qualified clinician for medical advice.")

        # --- Save to database for authenticated user ---
        if st.session_state.get("user_id"):
            save_assessment(
                user_id=st.session_state["user_id"],
                patient_name=username if username else "Anonymous",
                age=int(age),
                symptoms=", ".join(selected) if selected else "None",
                top_prediction=recorded_prediction,
                confidence=float(confidence),
                top3_json=json.dumps(top3),
            )

# -------- Detection History page --------
def history_page():
    theme.render_banner("Detection History", "View past clinical assessment records and analytics.", "📋")
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please log in to view detection history.")
        return

    records = get_user_assessments(user_id)
    if records:
        df = pd.DataFrame(records)
        display_df = df[["id", "patient_name", "age", "symptoms", "top_prediction", "confidence", "created_at"]].copy()
        display_df.rename(columns={
            "id": "ID",
            "patient_name": "Patient",
            "age": "Age",
            "symptoms": "Symptoms",
            "top_prediction": "Predicted Disease",
            "confidence": "Confidence",
            "created_at": "Timestamp",
        }, inplace=True)
        display_df["Confidence"] = display_df["Confidence"].apply(lambda c: f"{float(c):.1%}")
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # Download button (replaces server-side CSV file write)
        csv_bytes = display_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export History as CSV",
            data=csv_bytes,
            file_name=f"assessment_history_{st.session_state.get('username', 'user')}.csv",
            mime="text/csv",
        )

        # History Analytics Section
        st.divider()
        st.markdown("### 📊 History Analytics")
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("##### Most Frequent Predictions")
            pred_counts = df["top_prediction"].value_counts().reset_index()
            pred_counts.columns = ["Disease", "Count"]
            chart_preds = alt.Chart(pred_counts).mark_bar(cornerRadiusEnd=4).encode(
                y=alt.Y("Disease:N", sort="-x", title="Prediction"),
                x=alt.X("Count:Q", title="Assessments", axis=alt.Axis(tickMinStep=1)),
                color=alt.Color("Count:Q", scale=alt.Scale(scheme="greens"), legend=None),
                tooltip=["Disease", "Count"]
            ).properties(height=max(140, len(pred_counts) * 28))
            st.altair_chart(chart_preds, use_container_width=True)

        with col_b:
            st.markdown("##### Most Frequently Reported Symptoms")
            all_symptoms = []
            for sym_str in df["symptoms"].dropna():
                if sym_str and sym_str != "None":
                    for s in str(sym_str).split(","):
                        clean_s = s.strip()
                        if clean_s:
                            all_symptoms.append(clean_s.replace("_", " ").title())
            if all_symptoms:
                sym_counts = pd.Series(all_symptoms).value_counts().head(8).reset_index()
                sym_counts.columns = ["Symptom", "Count"]
                chart_syms = alt.Chart(sym_counts).mark_bar(cornerRadiusEnd=4).encode(
                    y=alt.Y("Symptom:N", sort="-x", title="Symptom"),
                    x=alt.X("Count:Q", title="Frequency", axis=alt.Axis(tickMinStep=1)),
                    color=alt.Color("Count:Q", scale=alt.Scale(scheme="tealblues"), legend=None),
                    tooltip=["Symptom", "Count"]
                ).properties(height=max(140, len(sym_counts) * 28))
                st.altair_chart(chart_syms, use_container_width=True)
            else:
                st.caption("No symptom records found.")
    else:
        st.info("No assessments recorded yet. Use the Dashboard to run disease predictions.")

# -------- Logout Action --------
def logout_action():
    st.session_state["user_id"] = None
    st.session_state["username"] = None
    st.session_state["show_register"] = False
    st.rerun()

# -------- Sidebar Navigation & Routing --------
if not st.session_state.get("user_id"):
    if st.session_state.get("show_register", False):
        register_page()
    else:
        login_page()
else:
    # Custom Brand Header & Profile Pill
    theme.render_sidebar_header(username=st.session_state.get("username", "manoj"))
    
    # Custom Styled Sidebar Navigation Menu
    nav_map = {
        "🏠  Dashboard": "Dashboard",
        "🩺  Detection History": "Detection History",
        "⚙️  Settings": "Settings",
        "🚪  Logout": "Logout",
    }
    nav_choice = st.sidebar.radio("Navigate", list(nav_map.keys()), label_visibility="collapsed")
    selected_tab = nav_map[nav_choice]

    # Dictionary Dispatcher Pattern
    if selected_tab == "Logout":
        logout_action()
    else:
        pages = {
            "Dashboard": dashboard_page,
            "Detection History": history_page,
            "Settings": settings_page,
        }
        if selected_tab in pages:
            pages[selected_tab]()

        
