"""
Data processing module for disease prediction.
Handles dataset loading, binary symptom coercion, deduplication, conflict resolution,
and train/test splitting with data leakage assertions.
"""

import hashlib
import logging
from typing import Tuple, List, Dict, Any, Union
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

DEFAULT_DATASET_PATH = "pro_disease_dataset.csv"


def coerce_binary(x: Any) -> int:
    """Coerce various representations of boolean/binary data to 0 or 1."""
    if x in (1, 0, 1.0, 0.0):
        return int(x)
    if isinstance(x, bool):
        return 1 if x else 0
    if isinstance(x, str):
        s = x.strip().lower()
        if s in ("1", "yes", "true", "y", "t"):
            return 1
        if s in ("0", "no", "false", "n", "f"):
            return 0
    try:
        val = float(x)
        return 1 if val >= 0.5 else 0
    except (ValueError, TypeError):
        return 0


def get_dataset_hash(filepath_or_bytes: Union[str, bytes]) -> str:
    """Compute SHA-256 hash of dataset file or byte content."""
    sha256 = hashlib.sha256()
    if isinstance(filepath_or_bytes, bytes):
        sha256.update(filepath_or_bytes)
    else:
        with open(filepath_or_bytes, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha256.update(chunk)
    return sha256.hexdigest()


def load_and_clean_data(
    source: Union[str, pd.DataFrame] = DEFAULT_DATASET_PATH
) -> Tuple[pd.DataFrame, Dict[str, Any], List[str]]:
    """
    Load CSV or use existing DataFrame, coerce symptom columns to 0/1,
    drop exact duplicates, and drop conflicting symptom patterns that
    have more than one Disease label.

    Returns:
        df_clean: Cleaned DataFrame.
        stats: Dictionary of cleaning metrics.
        symptom_cols: List of symptom column names.
    """
    if isinstance(source, pd.DataFrame):
        df = source.copy()
    else:
        df = pd.read_csv(source)

    if "Disease" not in df.columns:
        raise ValueError("Dataset missing required 'Disease' target column.")

    raw_rows = len(df)
    symptom_cols = [c for c in df.columns if c != "Disease"]

    # Coerce symptom columns to binary 0/1
    for col in symptom_cols:
        df[col] = df[col].map(coerce_binary).astype(int)

    # 1. Drop exact duplicate rows
    df_no_dupes = df.drop_duplicates().copy()
    exact_duplicates_removed = raw_rows - len(df_no_dupes)

    # 2. Detect feature patterns that appear with more than one Disease label
    grouped = df_no_dupes.groupby(symptom_cols)["Disease"].nunique()
    conflicting_patterns = grouped[grouped > 1]
    num_conflicting_patterns = len(conflicting_patterns)

    # Filter out conflicting patterns
    if num_conflicting_patterns > 0:
        conflicting_tuples = set(conflicting_patterns.index)
        is_conflicting = df_no_dupes[symptom_cols].apply(tuple, axis=1).isin(conflicting_tuples)
        conflicting_rows_removed = int(is_conflicting.sum())
        df_clean = df_no_dupes[~is_conflicting].copy()
    else:
        conflicting_rows_removed = 0
        df_clean = df_no_dupes

    final_rows = len(df_clean)

    stats = {
        "raw_rows": int(raw_rows),
        "exact_duplicates_removed": int(exact_duplicates_removed),
        "conflicting_patterns_removed": int(num_conflicting_patterns),
        "conflicting_rows_removed": int(conflicting_rows_removed),
        "final_rows": int(final_rows),
    }

    logger.info(
        "Data cleaning complete: raw=%d, exact_dupes_dropped=%d, "
        "conflicting_patterns=%d (rows_dropped=%d), final_clean_rows=%d",
        raw_rows,
        exact_duplicates_removed,
        num_conflicting_patterns,
        conflicting_rows_removed,
        final_rows,
    )

    return df_clean, stats, symptom_cols


def get_train_test_split(
    df_clean: pd.DataFrame,
    symptom_cols: List[str] = None,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Split cleaned data into train and test sets with stratification on Disease.
    Asserts that no feature row in test appears in train.
    """
    if symptom_cols is None:
        symptom_cols = [c for c in df_clean.columns if c != "Disease"]

    X = df_clean[symptom_cols]
    y = df_clean["Disease"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # Assert no test feature row appears in train
    train_patterns = set(X_train.apply(tuple, axis=1))
    test_patterns = set(X_test.apply(tuple, axis=1))
    leakage = train_patterns.intersection(test_patterns)
    assert len(leakage) == 0, f"Data leakage assertion failed! Found {len(leakage)} overlapping feature rows between train and test."

    return X_train, X_test, y_train, y_test
