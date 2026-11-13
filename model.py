"""
Model definition, training, ensemble soft-voting, and evaluation module.
"""

import os
import json
import warnings
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

MODELS_DIR = "models"
MODELS_FILE = os.path.join(MODELS_DIR, "models.joblib")
METRICS_FILE = os.path.join(MODELS_DIR, "metrics.json")
HASH_FILE = os.path.join(MODELS_DIR, "dataset_hash.txt")


Union_DF_Array = Any

def get_base_models(random_state: int = 42) -> Dict[str, Any]:
    """Instantiate the 3 base classifiers."""
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        svc_clf = SVC(
            probability=True,
            kernel="rbf",
            C=1.0,
            gamma="scale",
            random_state=random_state,
        )

    return {
        "Logistic Regression": Pipeline([
            ("scaler", StandardScaler(with_mean=False)),
            ("clf", LogisticRegression(max_iter=200, random_state=random_state)),
        ]),
        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            random_state=random_state,
        ),
        "SVC": Pipeline([
            ("scaler", StandardScaler(with_mean=False)),
            ("clf", svc_clf),
        ]),
    }


class SoftVotingEnsemble:
    """
    Soft voting ensemble that averages predict_proba across models
    and selects the argmax class. Confidence is the winning class probability.
    """

    def __init__(self, models: Dict[str, Any], classes: np.ndarray):
        self.models = models
        self.classes_ = np.array(classes)

    def predict_proba(self, X: Union_DF_Array) -> np.ndarray:  # type: ignore
        """
        Compute averaged predicted probabilities across all sub-models.
        Guarantees that each row sums to 1.
        """
        probas = []
        for name, model in self.models.items():
            p = model.predict_proba(X)
            # Ensure probability columns align with self.classes_
            if hasattr(model, "classes_") and not np.array_equal(model.classes_, self.classes_):
                model_classes = list(model.classes_)
                col_indices = [model_classes.index(c) for c in self.classes_]
                p = p[:, col_indices]
            probas.append(p)

        avg_proba = np.mean(probas, axis=0)
        # Normalize to ensure rows sum strictly to 1.0
        row_sums = avg_proba.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1.0
        return avg_proba / row_sums

    def predict(self, X: Any) -> np.ndarray:
        """Predict the disease class with the highest average probability."""
        avg_proba = self.predict_proba(X)
        win_idx = np.argmax(avg_proba, axis=1)
        return self.classes_[win_idx]

    def predict_sample(self, X_sample: pd.DataFrame) -> Dict[str, Any]:
        """
        Produce a full prediction package for a single sample:
        - final_prediction
        - confidence
        - top3 with probabilities
        - proba_dict (all classes)
        - individual_preds
        - individual_probas
        """
        avg_proba = self.predict_proba(X_sample)[0]
        sorted_indices = np.argsort(avg_proba)[::-1]

        final_class = str(self.classes_[sorted_indices[0]])
        confidence = float(avg_proba[sorted_indices[0]])

        top3 = [
            {"disease": str(self.classes_[idx]), "probability": float(avg_proba[idx])}
            for idx in sorted_indices[:3]
        ]
        all_probas = {
            str(self.classes_[i]): float(avg_proba[i])
            for i in range(len(self.classes_))
        }

        individual_preds = {}
        individual_probas = {}
        for name, model in self.models.items():
            pred = model.predict(X_sample)[0]
            individual_preds[name] = str(pred)
            if hasattr(model, "predict_proba"):
                p = model.predict_proba(X_sample)[0]
                m_classes = getattr(model, "classes_", self.classes_)
                individual_probas[name] = {
                    str(c): float(p[i]) for i, c in enumerate(m_classes)
                }

        return {
            "final_prediction": final_class,
            "confidence": confidence,
            "top3": top3,
            "all_probas": all_probas,
            "individual_preds": individual_preds,
            "individual_probas": individual_probas,
        }


# Type alias for input
Union_DF_Array = Any


def run_cross_validation(
    X: pd.DataFrame,
    y: pd.Series,
    n_splits: int = 5,
    random_state: int = 42,
) -> Dict[str, Dict[str, float]]:
    """
    Run 5-fold Stratified Cross-Validation for each model and the ensemble.
    Returns mean and std of accuracy and macro F1.
    """
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    model_names = ["Logistic Regression", "Random Forest", "SVC", "Ensemble"]
    acc_scores = {m: [] for m in model_names}
    f1_scores = {m: [] for m in model_names}

    classes = np.sort(y.unique())

    for train_idx, val_idx in cv.split(X, y):
        X_tr, y_tr = X.iloc[train_idx], y.iloc[train_idx]
        X_val, y_val = X.iloc[val_idx], y.iloc[val_idx]

        fold_models = get_base_models(random_state=random_state)
        fold_probas = []

        for name, model in fold_models.items():
            model.fit(X_tr, y_tr)
            pred = model.predict(X_val)
            acc_scores[name].append(accuracy_score(y_val, pred))
            f1_scores[name].append(f1_score(y_val, pred, average="macro"))
            fold_probas.append(model.predict_proba(X_val))

        # Soft voting ensemble
        avg_proba = np.mean(fold_probas, axis=0)
        ens_preds = classes[np.argmax(avg_proba, axis=1)]
        acc_scores["Ensemble"].append(accuracy_score(y_val, ens_preds))
        f1_scores["Ensemble"].append(f1_score(y_val, ens_preds, average="macro"))

    cv_results = {}
    for m in model_names:
        cv_results[m] = {
            "cv_accuracy_mean": float(np.mean(acc_scores[m])),
            "cv_accuracy_std": float(np.std(acc_scores[m])),
            "cv_macro_f1_mean": float(np.mean(f1_scores[m])),
            "cv_macro_f1_std": float(np.std(f1_scores[m])),
        }

    return cv_results


def evaluate_all(
    models: Dict[str, Any],
    ensemble: SoftVotingEnsemble,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    classes: np.ndarray,
) -> Dict[str, Any]:
    """
    Compute hold-out accuracy, macro F1, per-disease precision/recall/F1,
    confusion matrix, and 5-fold CV metrics.
    """
    classes_list = [str(c) for c in classes]
    cv_metrics = run_cross_validation(X_train, y_train, n_splits=5, random_state=42)

    eval_results = {
        "classes": classes_list,
        "models": {},
    }

    eval_targets = list(models.items()) + [("Ensemble", ensemble)]

    for name, model in eval_targets:
        y_pred = model.predict(X_test)
        acc = float(accuracy_score(y_test, y_pred))
        macro_f1 = float(f1_score(y_test, y_pred, average="macro"))

        report = classification_report(
            y_test, y_pred, labels=classes_list, output_dict=True, zero_division=0
        )
        cm = confusion_matrix(y_test, y_pred, labels=classes_list).tolist()

        per_disease = {}
        for c in classes_list:
            if c in report:
                per_disease[c] = {
                    "precision": float(report[c]["precision"]),
                    "recall": float(report[c]["recall"]),
                    "f1": float(report[c]["f1-score"]),
                    "support": int(report[c]["support"]),
                }

        eval_results["models"][name] = {
            "holdout_accuracy": acc,
            "holdout_macro_f1": macro_f1,
            "cv_accuracy_mean": cv_metrics[name]["cv_accuracy_mean"],
            "cv_accuracy_std": cv_metrics[name]["cv_accuracy_std"],
            "cv_macro_f1_mean": cv_metrics[name]["cv_macro_f1_mean"],
            "cv_macro_f1_std": cv_metrics[name]["cv_macro_f1_std"],
            "per_disease": per_disease,
            "confusion_matrix": cm,
        }

    return eval_results


def save_artifacts(
    models: Dict[str, Any],
    symptom_cols: List[str],
    classes: np.ndarray,
    metrics: Dict[str, Any],
    dataset_hash: str,
    output_dir: str = MODELS_DIR,
) -> None:
    """Save trained models, metadata, metrics, and dataset hash."""
    os.makedirs(output_dir, exist_ok=True)
    models_path = os.path.join(output_dir, "models.joblib")
    metrics_path = os.path.join(output_dir, "metrics.json")
    hash_path = os.path.join(output_dir, "dataset_hash.txt")

    artifact = {
        "models": models,
        "symptom_cols": symptom_cols,
        "classes": classes,
    }
    joblib.dump(artifact, models_path)

    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    with open(hash_path, "w", encoding="utf-8") as f:
        f.write(dataset_hash.strip())


def load_artifacts(
    models_dir: str = MODELS_DIR,
) -> Tuple[Dict[str, Any], SoftVotingEnsemble, List[str], np.ndarray, Dict[str, Any]]:
    """Load models, construct ensemble, and load metrics."""
    models_path = os.path.join(models_dir, "models.joblib")
    metrics_path = os.path.join(models_dir, "metrics.json")

    if not os.path.exists(models_path) or not os.path.exists(metrics_path):
        raise FileNotFoundError(f"Model artifacts not found in {models_dir}.")

    artifact = joblib.load(models_path)
    models = artifact["models"]
    symptom_cols = artifact["symptom_cols"]
    classes = artifact["classes"]

    ensemble = SoftVotingEnsemble(models, classes)

    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    return models, ensemble, symptom_cols, classes, metrics


def is_retrain_needed(
    dataset_hash: str,
    models_dir: str = MODELS_DIR,
) -> bool:
    """Check if retraining is required based on artifact existence and dataset hash."""
    models_path = os.path.join(models_dir, "models.joblib")
    metrics_path = os.path.join(models_dir, "metrics.json")
    hash_path = os.path.join(models_dir, "dataset_hash.txt")

    if not (os.path.exists(models_path) and os.path.exists(metrics_path) and os.path.exists(hash_path)):
        return True

    try:
        with open(hash_path, "r", encoding="utf-8") as f:
            saved_hash = f.read().strip()
        return saved_hash != dataset_hash.strip()
    except Exception:
        return True
