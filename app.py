import streamlit as st
import pandas as pd
import numpy as np
import theme
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from statistics import mode



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

# -------- Dashboard (prediction) page --------
def dashboard_page():
    theme.render_banner(
    "Disease Management Predictor", 
    "Enter patient details, select symptoms, and get an ensemble prediction across 3 ML models.", 
    "🩺")
    DEFAULT_PATH = "pro_disease_dataset.csv"
    @st.cache_data
    def load_data(path: str = DEFAULT_PATH):
        try:
            df = pd.read_csv(path)
            return df
        except Exception as e:
            st.error(f"Failed to load dataset from {path}: {e}")
            return None
    uploaded = st.file_uploader("Upload disease dataset (CSV) or use default bundled file", type=["csv"])
    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
        except Exception as e:
            st.error(f"Could not read uploaded CSV: {e}")
            st.stop()
    else:
        df = load_data(DEFAULT_PATH)
    if df is None:
        st.stop()
    if "Disease" not in df.columns:
        st.error("The dataset must have a 'Disease' column as the target.")
        st.stop()
    symptom_cols = [c for c in df.columns if c != "Disease"]
    # Model training
    X = df[symptom_cols]
    y = df["Disease"]
    def coerce_binary(x):
        if x in [1, 0]:
            return x
        if isinstance(x, str):
            s = x.strip().lower()
            if s in ["1", "yes", "true", "y"]:
                return 1
            if s in ["0", "no", "false", "n"]:
                return 0
        try:
            return int(float(x))
        except Exception:
            return 0
    X = X.map(coerce_binary)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    logreg = Pipeline([
        ("scaler", StandardScaler(with_mean=False)),
        ("clf", LogisticRegression(max_iter=200))
    ])
    rf = RandomForestClassifier(n_estimators=300, random_state=42)
    svc = Pipeline([
        ("scaler", StandardScaler(with_mean=False)),
        ("clf", SVC(probability=True, kernel="rbf", C=1.0, gamma="scale", random_state=42))
    ])
    logreg.fit(X_train, y_train)
    rf.fit(X_train, y_train)
    svc.fit(X_train, y_train)
    # Metrics
    with st.expander("Model validation (on hold-out set)"):
        for name, model in [("Logistic Regression", logreg), ("Random Forest", rf), ("SVC", svc)]:
            pred = model.predict(X_test)
            st.write(f"{name}** accuracy: {accuracy_score(y_test, pred):.3f}")
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
        x_input = pd.DataFrame([[1 if c in selected else 0 for c in symptom_cols]], columns=symptom_cols)
        pred_log = logreg.predict(x_input)[0]
        pred_rf = rf.predict(x_input)[0]
        pred_svc = svc.predict(x_input)[0]
        votes = [pred_log, pred_rf, pred_svc]
        try:
            final_pred = mode(votes)
        except Exception:
            final_pred = pred_rf
        st.subheader("Results")
        st.write(f"*Patient:* {username if username else 'Anonymous'} *Age:* {int(age)}")
        st.write(f"*Selected symptoms:* {', '.join(selected) if selected else 'None'}")
        cols = st.columns(3)
        cols[0].metric("Logistic Regression", str(pred_log))
        cols[1].metric("Random Forest", str(pred_rf))
        cols[2].metric("SVC", str(pred_svc))
        st.success(f"🎯 *Final prediction (majority vote):* {final_pred}")
        with st.expander("Model probabilities (if available)"):
            def safe_proba(model, x):
                if hasattr(model, "predict_proba"):
                    p = model.predict_proba(x)
                    classes = model.classes_
                    return dict(zip(classes, p[0]))
                return None
            for name, model in [("Logistic Regression", logreg), ("Random Forest", rf), ("SVC", svc)]:
                proba = safe_proba(model, x_input)
                if proba is not None:
                    st.write(f"{name}")
                    st.write({k: round(float(v), 3) for k, v in proba.items()})
                else:
                    st.write(f"{name}: probabilities not available")
        st.divider()
        st.subheader("Recommended Precautions")
        for tip in get_precautions(final_pred):
            st.write(f"- {tip}")
        st.info("*Note:* This tool is for educational purposes and not a medical diagnosis. Please consult a qualified clinician for medical advice.")
        # --- Save to history ---
        st.session_state["history"].append({
            "Patient": username if username else 'Anonymous',
            "Age": int(age),
            "Symptoms": ', '.join(selected),
            "Pred_LogisticRegression": pred_log,
            "Pred_RandomForest": pred_rf,
            "Pred_SVC": pred_svc,
            "FinalPrediction": final_pred,
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

        