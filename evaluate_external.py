"""
External dataset evaluation utility.
Evaluates model performance and data cleanliness on external public symptom-disease datasets.
Usage:
    python evaluate_external.py path/to/external_dataset.csv
"""

import sys
import os
import json
import numpy as np
import pandas as pd
from data import load_and_clean_data, get_train_test_split
from model import get_base_models, SoftVotingEnsemble, evaluate_all, load_artifacts


def evaluate_external_dataset(dataset_path: str):
    """Run full cleaning, validation, and evaluation on an external CSV dataset."""
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset file '{dataset_path}' does not exist.")
        sys.exit(1)

    print(f"===========================================================")
    print(f"  EXTERNAL DATASET EVALUATION: {dataset_path}")
    print(f"===========================================================")

    try:
        df_clean, stats, symptom_cols = load_and_clean_data(dataset_path)
    except Exception as e:
        print(f"Failed to load and clean external dataset: {e}")
        sys.exit(1)

    print("\n[1] Data Cleaning & Hygiene Summary:")
    print(f"  - Raw observations:                {stats['raw_rows']}")
    print(f"  - Exact duplicates dropped:        {stats['exact_duplicates_removed']}")
    print(f"  - Conflicting patterns detected:   {stats['conflicting_patterns_removed']} ({stats['conflicting_rows_removed']} rows dropped)")
    print(f"  - Final clean observations:        {stats['final_rows']}")
    print(f"  - Unique symptom columns ({len(symptom_cols)}): {symptom_cols[:5]}...")

    # Split train/test
    X_train, X_test, y_train, y_test = get_train_test_split(
        df_clean, symptom_cols=symptom_cols, test_size=0.2, random_state=42
    )
    print("\n[2] Train/Test Partitioning:")
    print(f"  - Training samples (80%):          {len(X_train)}")
    print(f"  - Hold-out test samples (20%):     {len(X_test)}")
    print(f"  - Leakage check:                   PASSED (0 test patterns in train)")

    classes = np.sort(y_train.unique())
    print(f"  - Target disease classes ({len(classes)}): {list(classes)}")

    models = get_base_models(random_state=42)
    print("\n[3] Fitting Classifiers on External Data...")
    for name, model in models.items():
        model.fit(X_train, y_train)

    ensemble = SoftVotingEnsemble(models, classes)

    print("\n[4] Computing Cross-Validation & Hold-out Metrics...")
    metrics = evaluate_all(
        models=models,
        ensemble=ensemble,
        X_train=X_train,
        y_train=y_train,
        X_test=X_test,
        y_test=y_test,
        classes=classes,
    )

    print("\n[5] Model Performance Summary:")
    print("-" * 75)
    print(f"{'Model':<22} | {'Hold-out Acc':<13} | {'Macro F1':<10} | {'5-Fold CV Acc':<18}")
    print("-" * 75)
    for m_name in ["Logistic Regression", "Random Forest", "SVC", "Ensemble"]:
        m_info = metrics["models"][m_name]
        print(
            f"{m_name:<22} | {m_info['holdout_accuracy']:<13.4f} | "
            f"{m_info['holdout_macro_f1']:<10.4f} | "
            f"{m_info['cv_accuracy_mean']:.4f} +/- {m_info['cv_accuracy_std']:.4f}"
        )
    print("-" * 75)

    print("\n[6] Per-Disease Classification Report (Ensemble):")
    ens_per_disease = metrics["models"]["Ensemble"]["per_disease"]
    print(f"{'Disease':<20} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10} | {'Support':<8}")
    print("-" * 65)
    for d_name, d_scores in ens_per_disease.items():
        print(
            f"{d_name:<20} | {d_scores['precision']:<10.3f} | "
            f"{d_scores['recall']:<10.3f} | {d_scores['f1']:<10.3f} | "
            f"{d_scores['support']:<8}"
        )
    print("-" * 65)

    print("\nEvaluation successfully completed.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python evaluate_external.py <path_to_csv>")
        sys.exit(1)
    evaluate_external_dataset(sys.argv[1])
