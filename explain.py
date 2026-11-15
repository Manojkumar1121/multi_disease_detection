"""
Explainability, safety guards, and red-flag rules module.
Implements leave-one-symptom-out feature attribution, weak-input guards,
emergency red-flag rules, and Altair visualizations.
"""

from typing import List, Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd
import altair as alt

# Configurable safety guard thresholds
MIN_SYMPTOMS_THRESHOLD: int = 2
MIN_CONFIDENCE_THRESHOLD: float = 0.40

# Clinical emergency red-flag symptom combinations
RED_FLAG_RULES: Dict[str, Tuple[str, ...]] = {
    "Suspected Acute Coronary Syndrome (Chest Pain + Shortness of Breath)": (
        "chest_pain",
        "shortness_of_breath",
    ),
    "Suspected Acute Myocardial Infarction (Chest Pain + Diaphoresis)": (
        "chest_pain",
        "sweating",
    ),
    "Cardiac Distress (Chest Tightness + Diaphoresis)": (
        "chest_tightness",
        "sweating",
    ),
    "Cardiorespiratory Distress (Chest Tightness + Shortness of Breath)": (
        "chest_tightness",
        "shortness_of_breath",
    ),
    "Severe Cardiopulmonary Emergency (Difficulty Breathing + Chest Pain)": (
        "difficulty_breathing",
        "chest_pain",
    ),
    "Severe Respiratory Distress (Difficulty Breathing + Wheezing + Chest Tightness)": (
        "difficulty_breathing",
        "wheezing",
        "chest_tightness",
    ),
    "Hemodynamic Instability (Chest Pain + Dizziness)": (
        "chest_pain",
        "dizziness",
    ),
    "Acute Pulmonary or Systemic Fluid Overload (Difficulty Breathing + Swelling)": (
        "difficulty_breathing",
        "swelling",
    ),
}


def check_red_flags(selected_symptoms: List[str]) -> Tuple[bool, List[str]]:
    """
    Check if selected symptoms trigger any emergency red-flag rule.

    Returns:
        (is_emergency, list_of_matching_rule_names)
    """
    selected_set = set(selected_symptoms)
    triggered = []

    for rule_name, required_symptoms in RED_FLAG_RULES.items():
        if set(required_symptoms).issubset(selected_set):
            triggered.append(rule_name)

    return (len(triggered) > 0, triggered)


def check_weak_input(
    selected_symptoms: List[str],
    confidence: float,
    min_symptoms: int = MIN_SYMPTOMS_THRESHOLD,
    min_confidence: float = MIN_CONFIDENCE_THRESHOLD,
) -> Tuple[bool, str]:
    """
    Evaluate weak-input safety guard:
    - If fewer than min_symptoms are selected.
    - If ensemble confidence is below min_confidence.

    Returns:
        (is_weak, user_message)
    """
    if len(selected_symptoms) < min_symptoms:
        return True, (
            f"Not enough information: Only {len(selected_symptoms)} symptom(s) selected. "
            f"Please select at least {min_symptoms} symptoms for an initial assessment, "
            "or consult a healthcare professional."
        )

    if confidence < min_confidence:
        return True, (
            f"Not enough information: Model confidence ({confidence:.1%}) is below the "
            f"safety threshold ({min_confidence:.1%}). The selected symptoms do not match "
            "a distinctive diagnostic profile. Please consult a qualified clinician."
        )

    return False, ""


def compute_leave_one_out_importance(
    ensemble: Any,
    selected_symptoms: List[str],
    symptom_cols: List[str],
    top_class: str,
    baseline_confidence: float,
) -> List[Dict[str, Any]]:
    """
    Compute symptom attribution using Leave-One-Symptom-Out (LOSO):
    Removes each selected symptom one at a time, recomputes the ensemble probability
    for top_class, and reports the drop: drop = baseline_confidence - p_reduced.
    Symptoms are ranked in descending order of their positive probability drop.
    """
    if not selected_symptoms:
        return []

    # If only 1 symptom is selected, the drop without it is baseline - p(empty)
    results = []
    base_row = [1 if c in selected_symptoms else 0 for c in symptom_cols]

    for symptom in selected_symptoms:
        if symptom not in symptom_cols:
            continue
        col_idx = symptom_cols.index(symptom)
        reduced_row = list(base_row)
        reduced_row[col_idx] = 0

        x_reduced = pd.DataFrame([reduced_row], columns=symptom_cols)
        p_reduced_dict = ensemble.predict_sample(x_reduced)["all_probas"]
        p_without = p_reduced_dict.get(top_class, 0.0)

        drop = baseline_confidence - p_without
        results.append({
            "symptom": symptom,
            "drop": float(drop),
            "prob_without": float(p_without),
            "impact_pct": float(drop * 100),
        })

    # Rank by drop descending (symptoms causing largest drop drove prediction most)
    results.sort(key=lambda item: item["drop"], reverse=True)
    return results


def build_top3_chart(top3: List[Dict[str, Any]]) -> alt.Chart:
    """
    Construct Altair horizontal bar chart for top 3 diseases with probabilities.
    """
    df = pd.DataFrame(top3)
    df["display_prob"] = df["probability"].apply(lambda p: f"{p:.1%}")
    df["label"] = df["disease"]

    base = alt.Chart(df).encode(
        y=alt.Y("disease:N", title="Disease", sort="-x", axis=alt.Axis(labelFontSize=12)),
        x=alt.X(
            "probability:Q",
            title="Ensemble Probability",
            scale=alt.Scale(domain=[0, 1.0]),
            axis=alt.Axis(format="%", tickCount=5),
        ),
    )

    bars = base.mark_bar(cornerRadiusEnd=6, height=26).encode(
        color=alt.Color(
            "probability:Q",
            scale=alt.Scale(scheme="greens", domain=[0.0, 1.0]),
            legend=None,
        ),
        tooltip=[
            alt.Tooltip("disease:N", title="Disease"),
            alt.Tooltip("probability:Q", title="Probability", format=".1%"),
        ],
    )

    labels = base.mark_text(
        align="left",
        baseline="middle",
        dx=6,
        fontSize=12,
        fontWeight=600,
        color="#1E293B",
    ).encode(
        text="display_prob:N"
    )

    return (bars + labels).properties(
        title=alt.TitleParams("Top 3 Candidate Diseases by Ensemble Probability", fontSize=14),
        height=160,
    )


def build_importance_chart(importance_data: List[Dict[str, Any]]) -> alt.Chart:
    """
    Construct Altair horizontal bar chart for leave-one-symptom-out attribution.
    """
    df = pd.DataFrame(importance_data)
    df["display_drop"] = df["drop"].apply(lambda d: f"{d:+.1%}")
    # Human-friendly symptom labels (replace underscores with spaces)
    df["symptom_label"] = df["symptom"].str.replace("_", " ").str.title()

    base = alt.Chart(df).encode(
        y=alt.Y(
            "symptom_label:N",
            title="Selected Symptom",
            sort="-x",
            axis=alt.Axis(labelFontSize=11),
        ),
        x=alt.X(
            "drop:Q",
            title="Probability Drop (Leave-One-Out Impact)",
            axis=alt.Axis(format="%", tickCount=5),
        ),
    )

    bars = base.mark_bar(cornerRadiusEnd=5, height=22).encode(
        color=alt.condition(
            alt.datum.drop > 0,
            alt.value("#0E5C46"),  # Deep clinical emerald for positive drivers
            alt.value("#94A3B8"),  # Slate gray for neutral/suppressive
        ),
        tooltip=[
            alt.Tooltip("symptom_label:N", title="Symptom"),
            alt.Tooltip("drop:Q", title="Impact on Top Disease", format="+.1%"),
            alt.Tooltip("prob_without:Q", title="Probability Without Symptom", format=".1%"),
        ],
    )

    labels = base.mark_text(
        align="left",
        baseline="middle",
        dx=5,
        fontSize=11,
    ).encode(
        text="display_drop:N"
    )

    chart_height = max(120, len(df) * 32)
    return (bars + labels).properties(
        title=alt.TitleParams("Key Symptoms Driving Top Prediction (Leave-One-Out)", fontSize=13),
        height=chart_height,
    )
