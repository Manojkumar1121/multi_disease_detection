"""
Unit tests for Section 1: Data cleaning, train/test split, soft-voting ensemble,
and model evaluation metrics.
"""

import os
import json
import numpy as np
import pandas as pd
import pytest

from data import (
    DEFAULT_DATASET_PATH,
    coerce_binary,
    get_dataset_hash,
    load_and_clean_data,
    get_train_test_split,
)
from model import (
    get_base_models,
    SoftVotingEnsemble,
    load_artifacts,
    MODELS_FILE,
    METRICS_FILE,
    HASH_FILE,
)


def test_coerce_binary():
    assert coerce_binary(1) == 1
    assert coerce_binary(0) == 0
    assert coerce_binary("1") == 1
    assert coerce_binary("0") == 0
    assert coerce_binary("yes") == 1
    assert coerce_binary("no") == 0
    assert coerce_binary("true") == 1
    assert coerce_binary("false") == 0
    assert coerce_binary(True) == 1
    assert coerce_binary(False) == 0
    assert coerce_binary("invalid") == 0


def test_cleaning_removes_duplicates_and_conflicts():
    df_clean, stats, symptom_cols = load_and_clean_data(DEFAULT_DATASET_PATH)

    # 1. Dataset shapes and counts
    assert stats["raw_rows"] == 2000
    assert stats["exact_duplicates_removed"] == 520
    assert stats["conflicting_patterns_removed"] == 25
    assert stats["conflicting_rows_removed"] == 51
    assert stats["final_rows"] == 1429
    assert len(df_clean) == 1429

    # 2. No exact duplicates remain
    assert df_clean.duplicated().sum() == 0

    # 3. No conflicting feature patterns remain (same symptoms -> different disease)
    grouped = df_clean.groupby(symptom_cols)["Disease"].nunique()
    assert (grouped > 1).sum() == 0

    # 4. All symptom values coerced to 0 or 1
    for col in symptom_cols:
        assert set(df_clean[col].unique()).issubset({0, 1})


def test_no_train_test_leakage():
    df_clean, _, symptom_cols = load_and_clean_data(DEFAULT_DATASET_PATH)
    X_train, X_test, y_train, y_test = get_train_test_split(
        df_clean, symptom_cols=symptom_cols, test_size=0.2, random_state=42
    )

    train_tuples = set(X_train.apply(tuple, axis=1))
    test_tuples = set(X_test.apply(tuple, axis=1))
    overlap = train_tuples.intersection(test_tuples)
    assert len(overlap) == 0, f"Found {len(overlap)} overlapping feature rows between train and test!"


def test_predict_proba_sums_to_one():
    models, ensemble, symptom_cols, classes, _ = load_artifacts()

    # Generate test dummy vectors
    dummy_input = pd.DataFrame([
        [1] * len(symptom_cols),
        [0] * len(symptom_cols),
        [1 if i % 2 == 0 else 0 for i in range(len(symptom_cols))],
    ], columns=symptom_cols)

    probas = ensemble.predict_proba(dummy_input)
    assert probas.shape == (3, len(classes))
    row_sums = np.sum(probas, axis=1)
    np.testing.assert_allclose(row_sums, [1.0, 1.0, 1.0], atol=1e-5)


def test_soft_voting_logic():
    # Test soft-voting argmax logic with dummy predictable probabilities
    class MockModel:
        def __init__(self, proba):
            self._proba = proba
            self.classes_ = np.array(["DiseaseA", "DiseaseB", "DiseaseC"])

        def predict_proba(self, X):
            return np.array([self._proba] * len(X))

    # Model 1 gives [0.7, 0.2, 0.1]
    # Model 2 gives [0.2, 0.7, 0.1]
    # Model 3 gives [0.6, 0.3, 0.1]
    # Average: [0.5, 0.4, 0.1] -> DiseaseA should win with confidence 0.5
    m1 = MockModel([0.7, 0.2, 0.1])
    m2 = MockModel([0.2, 0.7, 0.1])
    m3 = MockModel([0.6, 0.3, 0.1])

    classes = np.array(["DiseaseA", "DiseaseB", "DiseaseC"])
    ensemble = SoftVotingEnsemble({"m1": m1, "m2": m2, "m3": m3}, classes)

    dummy_X = pd.DataFrame([[1, 0]], columns=["s1", "s2"])
    proba = ensemble.predict_proba(dummy_X)[0]
    np.testing.assert_allclose(proba, [0.5, 0.4, 0.1], atol=1e-5)

    pred = ensemble.predict(dummy_X)[0]
    assert pred == "DiseaseA"


def test_metrics_json_integrity():
    assert os.path.exists(METRICS_FILE)
    with open(METRICS_FILE, "r") as f:
        metrics = json.load(f)

    assert "models" in metrics
    assert "classes" in metrics
    expected_models = ["Logistic Regression", "Random Forest", "SVC", "Ensemble"]
    for m in expected_models:
        assert m in metrics["models"]
        m_data = metrics["models"][m]
        assert "holdout_accuracy" in m_data
        assert "holdout_macro_f1" in m_data
        assert "cv_accuracy_mean" in m_data
        assert "cv_accuracy_std" in m_data
        assert "cv_macro_f1_mean" in m_data
        assert "cv_macro_f1_std" in m_data
        assert "per_disease" in m_data
        assert "confusion_matrix" in m_data

        # Sanity check metrics range
        assert 0.8 <= m_data["holdout_accuracy"] <= 1.0
        assert 0.8 <= m_data["cv_accuracy_mean"] <= 1.0
