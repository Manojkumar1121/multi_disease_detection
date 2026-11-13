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



# Must be first Streamlit command!
st.set_page_config(page_title="Disease Management Predictor", page_icon="🩺", layout="centered")

# -------- Session state for login, theme, history, users, register page toggle --------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"
if "history" not in st.session_state:
    st.session_state["history"] = []
if "users" not in st.session_state:
    st.session_state["users"] = {"mamaa": "1234"}
if "show_register" not in st.session_state:
    st.session_state["show_register"] = False
theme.apply_custom_theme(st.session_state.get("theme", "dark"))
# 2. Apply theme AFTER "theme" is initialized
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
    st.title("Create Account")
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    if st.button("Register"):
        if new_username in st.session_state["users"]:
            st.error("Username already exists!")
        elif not new_username or not new_password:
            st.error("Username and password cannot be empty!")
        else:
            st.session_state["users"][new_username] = new_password
            st.success("Account created successfully! You can now log in.")
            st.session_state["show_register"] = False
            st.rerun()
    if st.button("Back to Login"):
        st.session_state["show_register"] = False
        st.rerun()

# -------- Login page --------
def login_page():
    st.title("🔒 Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if st.session_state["users"].get(username) == password:
            st.session_state["logged_in"] = True
            st.session_state["show_register"] = False
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password!")
            st.info("Demo credentials: username = mamaa, password = 1234")
    st.info("Don't have an account?")
    if st.button("Create Account"):
        st.session_state["show_register"] = True
        st.rerun()
    # Show register page if toggled
    if st.session_state.get("show_register", False):
        register_page()

# -------- Cached Model Loader --------
@st.cache_resource
def get_app_models(dataset_path: str = DEFAULT_DATASET_PATH):
    return train_pipeline(dataset_path=dataset_path, force=False)

# -------- Dashboard (prediction) page --------
def dashboard_page():
    theme.render_banner(
        "Disease Management Predictor", 
        "Enter patient details, select symptoms, and get an ensemble prediction across 3 ML models.", 
        "🩺"
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
    with st.expander("Model validation & performance metrics"):
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
            color=alt.Color("Count:Q", scale=alt.Scale(scheme="blues"), legend=alt.Legend(title="Count")),
            tooltip=["Actual", "Predicted", "Count"]
        )
        text = base.mark_text(baseline="middle").encode(
            text="Count:Q",
            color=alt.condition(alt.datum.Count > df_cm["Count"].max() / 2, alt.value("white"), alt.value("black"))
        )
        st.altair_chart((heatmap + text).properties(height=380), use_container_width=True)

    # Prediction form
    with st.form("patient_form"):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Patient name", max_chars=50)
        with col2:
            age = st.number_input("Age", min_value=0, max_value=120, value=25, step=1)
        selected = st.multiselect("Select your symptoms", options=symptom_cols, default=[])
        submitted = st.form_submit_button("Predict")

    PRECAUTIONS = {
        "Asthma": [
            "Use your prescribed inhaler as directed.",
            "Avoid known triggers (smoke, dust, cold air).",
            "Warm-up before exercise and keep rescue inhaler handy."
        ],
        # ... (other disease precautions unchanged)
    }
    def get_precautions(label: str):
        return PRECAUTIONS.get(label, [
            "Consult a healthcare professional for personalized advice.",
            "Rest, stay hydrated, and monitor your symptoms.",
            "Seek urgent care if symptoms worsen."
        ])

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
            st.subheader("Recommended Precautions")
            for tip in get_precautions(final_pred):
                st.write(f"- {tip}")

        with st.expander("Model probabilities (if available)"):
            for m_name, proba_dict in sample_res["individual_probas"].items():
                st.write(f"**{m_name}**")
                st.write({k: round(float(v), 3) for k, v in proba_dict.items()})
            st.write("**Ensemble (Soft-Voting)**")
            st.write({k: round(float(v), 3) for k, v in sample_res["all_probas"].items()})

        st.info("*Note:* This tool is for educational purposes and not a medical diagnosis. Please consult a qualified clinician for medical advice.")

        # --- Save to history ---
        st.session_state["history"].append({
            "Patient": username if username else 'Anonymous',
            "Age": int(age),
            "Symptoms": ', '.join(selected),
            "Pred_LogisticRegression": pred_log,
            "Pred_RandomForest": pred_rf,
            "Pred_SVC": pred_svc,
            "FinalPrediction": recorded_prediction,
            "Confidence": confidence,
            "Top3": top3,
        })
    else:
        st.caption("Fill the form and click Predict to see results.")

# -------- Detection History page --------
def history_page():
    st.title("Detection History")
    history = st.session_state["history"]
    if history:
        df = pd.DataFrame(history)
        st.write(df)
        if st.button("Export as CSV"):
            df.to_csv("prediction_history.csv", index=False)
            st.success("Exported as prediction_history.csv")
    else:
        st.info("No predictions yet.")

# -------- Logout --------
def logout_page():
    st.title("Logout")
    st.session_state["logged_in"] = False
    st.success("You are logged out!")
    st.rerun()

# -------- Sidebar Navigation --------
page_tabs = ["Dashboard", "Detection History", "Settings", "Logout"]

# -------- Navigation Routing --------
if not st.session_state.get("logged_in", False):
    login_page()
else:
    # Sidebar Navigation
    st.sidebar.title("🩺 Health Portal")
    st.sidebar.caption("AI Decision Support System")
    st.sidebar.divider()
    
    selected_tab = st.sidebar.radio("Navigate", page_tabs)

    # Dictionary Dispatcher Pattern
    pages = {
        "Dashboard": dashboard_page,
        "Detection History": history_page,
        "Settings": settings_page,
        "Logout": logout_page,
    }

    # Execute selected page function safely
    if selected_tab in pages:
        pages[selected_tab]()

        