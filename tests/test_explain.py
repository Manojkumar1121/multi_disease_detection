"""
Unit tests for Section 2: Explainability, leave-one-symptom-out attribution,
weak-input guards, and red-flag emergency detection.
"""

import pytest
import pandas as pd
from model import load_artifacts
from explain import (
    MIN_SYMPTOMS_THRESHOLD,
    MIN_CONFIDENCE_THRESHOLD,
    check_weak_input,
    check_red_flags,
    compute_leave_one_out_importance,
    build_top3_chart,
    build_importance_chart,
)


def test_weak_input_guard_zero_and_one_symptoms():
    # 0 symptoms
    is_weak_0, msg_0 = check_weak_input([], confidence=0.85)
    assert is_weak_0 is True
    assert "Not enough information" in msg_0
    assert "0 symptom(s) selected" in msg_0

    # 1 symptom
    is_weak_1, msg_1 = check_weak_input(["cough"], confidence=0.90)
    assert is_weak_1 is True
    assert "Not enough information" in msg_1
    assert "1 symptom(s) selected" in msg_1

    # 2 symptoms with high confidence -> passes
    is_weak_2, _ = check_weak_input(["cough", "fever"], confidence=0.75)
    assert is_weak_2 is False


def test_weak_input_guard_low_confidence():
    # 3 symptoms but confidence is 0.35 (below 0.40 threshold)
    is_weak, msg = check_weak_input(["cough", "fever", "fatigue"], confidence=0.35)
    assert is_weak is True
    assert "Not enough information" in msg
    assert "below the safety threshold" in msg

    # Confidence exactly at or above 0.40 passes
    is_weak_pass, _ = check_weak_input(["cough", "fever", "fatigue"], confidence=0.40)
    assert is_weak_pass is False


def test_red_flag_rules_trigger():
    # Emergency combinations
    is_em_1, triggers_1 = check_red_flags(["chest_pain", "shortness_of_breath"])
    assert is_em_1 is True
    assert len(triggers_1) >= 1

    is_em_2, triggers_2 = check_red_flags(["chest_tightness", "sweating", "fatigue"])
    assert is_em_2 is True
    assert len(triggers_2) >= 1

    is_em_3, triggers_3 = check_red_flags(["difficulty_breathing", "chest_pain"])
    assert is_em_3 is True

    # Non-emergency combinations
    is_em_safe, triggers_safe = check_red_flags(["cough", "fever", "fatigue"])
    assert is_em_safe is False
    assert len(triggers_safe) == 0


def test_leave_one_out_symptom_attribution():
    models, ensemble, symptom_cols, classes, _ = load_artifacts()

    selected = ["chest_pain", "shortness_of_breath", "sweating"]
    x_input = pd.DataFrame([[1 if c in selected else 0 for c in symptom_cols]], columns=symptom_cols)
    res = ensemble.predict_sample(x_input)
    top_class = res["final_prediction"]
    base_confidence = res["confidence"]

    importance = compute_leave_one_out_importance(
        ensemble=ensemble,
        selected_symptoms=selected,
        symptom_cols=symptom_cols,
        top_class=top_class,
        baseline_confidence=base_confidence,
    )

    assert len(importance) == len(selected)
    # Check that entries are sorted descending by probability drop
    drops = [item["drop"] for item in importance]
    assert drops == sorted(drops, reverse=True)

    # Check structure
    for item in importance:
        assert "symptom" in item
        assert "drop" in item
        assert "prob_without" in item


def test_altair_charts_construction():
    top3_dummy = [
        {"disease": "Asthma", "probability": 0.70},
        {"disease": "Flu", "probability": 0.20},
        {"disease": "Pneumonia", "probability": 0.10},
    ]
    chart_top3 = build_top3_chart(top3_dummy)
    assert chart_top3 is not None

    importance_dummy = [
        {"symptom": "wheezing", "drop": 0.35, "prob_without": 0.35},
        {"symptom": "cough", "drop": 0.15, "prob_without": 0.55},
    ]
    chart_imp = build_importance_chart(importance_dummy)
    assert chart_imp is not None
