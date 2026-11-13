"""
Unit tests for precautions and PDF report generation.
Verifies that precautions exist for every disease label in the dataset,
general safety advice only (no drug names or dosages), and PDF generation.
"""

import pytest
import pandas as pd
from data import DEFAULT_DATASET_PATH, load_and_clean_data
from precautions import PRECAUTIONS_DATA, get_precautions_for_disease
from report import generate_pdf_report


def test_precautions_exist_for_all_dataset_diseases():
    df_clean, _, _ = load_and_clean_data(DEFAULT_DATASET_PATH)
    unique_diseases = df_clean["Disease"].unique()

    assert len(unique_diseases) == 10
    for disease in unique_diseases:
        assert disease in PRECAUTIONS_DATA, f"Missing precautions for {disease}!"
        data = PRECAUTIONS_DATA[disease]
        assert "precautions" in data
        assert "when_to_seek_care" in data
        assert 3 <= len(data["precautions"]) <= 4
        assert len(data["when_to_seek_care"]) > 20


def test_no_drug_names_or_dosages_in_precautions():
    prohibited_terms = [
        "mg", "mcg", "tablet", "capsule", "dosage",
        "aspirin", "paracetamol", "acetaminophen", "ibuprofen",
        "metformin", "insulin", "albuterol", "antibiotic", "amoxicillin",
    ]

    for disease, data in PRECAUTIONS_DATA.items():
        text_corpus = " ".join(data["precautions"]) + " " + data["when_to_seek_care"]
        words = text_corpus.lower().split()
        for term in prohibited_terms:
            assert term not in words, f"Prohibited clinical drug term '{term}' found in precautions for {disease}!"


def test_pdf_report_generation():
    pdf_bytes = generate_pdf_report(
        patient_name="John Doe",
        age=50,
        symptoms=["chest_pain", "sweating"],
        top_prediction="Heart Attack",
        confidence=0.91,
        top3=[{"disease": "Heart Attack", "probability": 0.91}, {"disease": "Hypertension", "probability": 0.05}],
        contributing_symptoms=[{"symptom": "chest_pain", "drop": 0.40, "prob_without": 0.51}],
        precautions_info=get_precautions_for_disease("Heart Attack"),
        red_flag_info=(True, ["Chest pain with diaphoresis (sweating)"]),
    )

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 1500
    # PDF header check
    assert pdf_bytes.startswith(b"%PDF")
