# Dataset Audit & Cleaning Documentation

## 1. Provenance and Synthetic Data Characteristics

The bundled dataset (`pro_disease_dataset.csv`) consists of **2,000 observations**, **24 binary symptom indicators**, and **10 disease target classes**.

Upon forensic clinical and statistical audit, **this dataset appears heavily synthetic or artificially generated**:

1. **Near-Identical Class Distribution:** Each of the 10 diseases originally contained almost exactly 200 samples (Dengue: 207, Hypertension: 206, Flu: 204, Malaria: 200, Asthma: 200, Diabetes: 199, Kidney Disease: 197, Pneumonia: 197, Migraine: 196, Heart Attack: 194). Natural epidemiological datasets reflect skewed disease prevalence and demographic divergence.
2. **Clinically Unnatural Co-occurrences:** Numerous symptom combinations in the dataset contradict physiological symptom presentation (e.g., combinations of acute viral symptoms identically matching chronic cardiovascular conditions).
3. **Identical Duplicate Symptom Signatures:** Out of 2,000 rows, **520 rows (26.0%)** were exact duplicate records.
4. **Conflicting Symptom Patterns:** **25 distinct symptom signatures (spanning 51 observations)** were mapped to conflicting disease labels (identical symptom vectors mapped simultaneously to entirely different diseases).

---

## 2. Data Hygiene & Cleaning Pipeline

To ensure rigorous machine learning evaluation without synthetic inflation or label noise, the pipeline (`data.py`) enforces:

1. **Binary Coercion:** Standardizes all 24 symptom columns into strict integer binary values ($0$ or $1$), safely parsing strings, floats, booleans, and nulls.
2. **Exact Duplicate Removal:** Drops all exact identical rows, eliminating 520 redundant entries.
3. **Conflict Resolution:** Identifies all feature vectors associated with more than one disease label ($N_{diseases} > 1$) and purges them completely (25 conflicting patterns, 51 rows).
4. **Leakage-Free Partitioning:** The remaining **1,429 clean, unique samples** are split into an 80% training set (1,143 samples) and a 20% hold-out test set (286 samples) stratified by disease.
5. **Leakage Assertion:** An explicit set intersection check asserts that zero test feature patterns exist in the training partition.

### Cleaning Summary
| Metric | Count |
| :--- | :--- |
| **Initial Raw Observations** | 2,000 |
| **Exact Duplicate Rows Dropped** | 520 |
| **Conflicting Symptom Patterns Dropped** | 25 patterns (51 rows) |
| **Final Cleaned Unique Observations** | 1,429 |
| **Train Set Size (80% Stratified)** | 1,143 |
| **Hold-out Test Size (20% Stratified)** | 286 |
| **Train/Test Feature Overlap** | **0 (Zero Leakage)** |

---

## 3. Prototype Disclaimer & Clinical Limitations

- **Prototype Status:** This system is an educational and technological demonstrator developed for hackathon evaluation. It is **not** an FDA-approved medical diagnostic tool.
- **No Replacement for Clinical Care:** Machine learning models trained on synthetic symptom matrices cannot replace clinical judgment, physical examination, laboratory blood work, imaging (ECG, X-rays), or physician-patient interaction.
- **Emergency Safeguard:** Emergency red-flag rules are hardcoded in `explain.py` to prompt immediate emergency services contact regardless of model confidence.

---

## 4. Evaluating On External Datasets

An external evaluation utility is provided: `evaluate_external.py`.

```bash
python evaluate_external.py path/to/external_dataset.csv
```

This utility validates column compatibility, applies binary coercion and cleaning, and evaluates hold-out accuracy, macro F1, per-disease metrics, and confusion matrices against the ensemble model.
