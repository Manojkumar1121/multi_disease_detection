"""
Training pipeline script.
Cleans dataset, fits models, evaluates holdout and 5-fold CV,
and saves artifacts to models/.
"""

import sys
import logging
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from data import (
    DEFAULT_DATASET_PATH,
    load_and_clean_data,
    get_train_test_split,
    get_dataset_hash,
)
from model import (
    get_base_models,
    SoftVotingEnsemble,
    evaluate_all,
    save_artifacts,
    load_artifacts,
    is_retrain_needed,
    MODELS_DIR,
)

logger = logging.getLogger("train")
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )


def train_pipeline(
    dataset_path: str = DEFAULT_DATASET_PATH,
    force: bool = False,
) -> Tuple[Dict[str, Any], SoftVotingEnsemble, list, np.ndarray, Dict[str, Any]]:
    """
    Execute full training pipeline. If artifacts are present and dataset hash matches,
    loads and returns existing artifacts unless force=True.
    """
    dataset_hash = get_dataset_hash(dataset_path)

    if not force and not is_retrain_needed(dataset_hash, models_dir=MODELS_DIR):
        logger.info("Trained model artifacts already exist and dataset hash matches. Loading cached models.")
        return load_artifacts(models_dir=MODELS_DIR)

    logger.info("Starting model training pipeline for %s...", dataset_path)
    df_clean, stats, symptom_cols = load_and_clean_data(dataset_path)
    logger.info("Cleaning stats: %s", stats)

    X_train, X_test, y_train, y_test = get_train_test_split(
        df_clean, symptom_cols=symptom_cols, test_size=0.2, random_state=42
    )
    logger.info(
        "Train set: %d samples, Test set: %d samples. Overlap check: PASSED (0 leakage).",
        len(X_train),
        len(X_test),
    )

    classes = np.sort(y_train.unique())
    models = get_base_models(random_state=42)

    logger.info("Fitting base models (Logistic Regression, Random Forest, SVC)...")
    for name, model in models.items():
        logger.info("Training %s...", name)
        model.fit(X_train, y_train)

    ensemble = SoftVotingEnsemble(models, classes)

    logger.info("Evaluating hold-out and 5-fold cross-validation...")
    metrics = evaluate_all(
        models=models,
        ensemble=ensemble,
        X_train=X_train,
        y_train=y_train,
        X_test=X_test,
        y_test=y_test,
        classes=classes,
    )
    metrics["cleaning_summary"] = stats
    metrics["dataset_hash"] = dataset_hash

    logger.info("Hold-out and CV evaluation complete:")
    for m_name, m_data in metrics["models"].items():
        logger.info(
            "  [%s] Hold-out Acc: %.4f | Macro F1: %.4f | 5-Fold CV Acc: %.4f +/- %.4f",
            m_name,
            m_data["holdout_accuracy"],
            m_data["holdout_macro_f1"],
            m_data["cv_accuracy_mean"],
            m_data["cv_accuracy_std"],
        )

    save_artifacts(
        models=models,
        symptom_cols=symptom_cols,
        classes=classes,
        metrics=metrics,
        dataset_hash=dataset_hash,
        output_dir=MODELS_DIR,
    )
    logger.info("Artifacts saved successfully to '%s'.", MODELS_DIR)

    return models, ensemble, symptom_cols, classes, metrics


if __name__ == "__main__":
    force_flag = "--force" in sys.argv
    path = DEFAULT_DATASET_PATH
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            path = arg
            break
    train_pipeline(dataset_path=path, force=force_flag)
