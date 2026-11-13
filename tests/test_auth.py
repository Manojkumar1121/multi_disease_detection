"""
Unit tests for Section 3: SQLite authentication, bcrypt password hashing,
username normalization, password policy, and per-user assessment storage.
"""

import os
import json
import pytest
from auth import (
    init_db,
    normalize_username,
    hash_password,
    check_password,
    register_user,
    authenticate_user,
    save_assessment,
    get_user_assessments,
)


@pytest.fixture
def temp_db(tmp_path):
    """Provide an isolated temporary SQLite database for tests."""
    db_file = str(tmp_path / "test_app.db")
    init_db(db_file)
    return db_file


def test_username_normalization():
    assert normalize_username("  DoctorBob  ") == "doctorbob"
    assert normalize_username("Alice_MD") == "alice_md"
    assert normalize_username("   ") == ""


def test_password_hashing():
    pwd = "SecurePassword123!"
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert check_password(pwd, hashed) is True
    assert check_password("WrongPassword!", hashed) is False


def test_password_length_enforcement(temp_db):
    # Passwords shorter than 8 chars must be rejected
    success, msg = register_user("clinician1", "short", db_path=temp_db)
    assert success is False
    assert "at least 8 characters" in msg

    # Passwords of length >= 8 must be accepted
    success_valid, msg_valid = register_user("clinician1", "validpass123", db_path=temp_db)
    assert success_valid is True
    assert "Account created" in msg_valid


def test_user_registration_and_duplicate_prevention(temp_db):
    success, _ = register_user("DrHouse", "Diagnostician99", db_path=temp_db)
    assert success is True

    # Case-insensitive duplicate check
    dup_success, dup_msg = register_user("  drhouse  ", "AnotherPassword99", db_path=temp_db)
    assert dup_success is False
    assert "already exists" in dup_msg


def test_authentication_round_trip(temp_db):
    register_user("NurseJackie", "HospitalPass1", db_path=temp_db)

    # Valid login
    user = authenticate_user("  nursejackie ", "HospitalPass1", db_path=temp_db)
    assert user is not None
    assert user["username"] == "nursejackie"
    assert isinstance(user["id"], int)

    # Invalid password
    assert authenticate_user("nursejackie", "WrongHospitalPass", db_path=temp_db) is None

    # Nonexistent user
    assert authenticate_user("nonexistent", "HospitalPass1", db_path=temp_db) is None


def test_per_user_assessment_isolation(temp_db):
    register_user("user_a", "PasswordUserA1", db_path=temp_db)
    register_user("user_b", "PasswordUserB1", db_path=temp_db)

    user_a = authenticate_user("user_a", "PasswordUserA1", db_path=temp_db)
    user_b = authenticate_user("user_b", "PasswordUserB1", db_path=temp_db)

    # Save assessment for User A
    save_assessment(
        user_id=user_a["id"],
        patient_name="Patient 01",
        age=45,
        symptoms="cough, fever",
        top_prediction="Flu",
        confidence=0.88,
        top3_json=json.dumps([{"disease": "Flu", "probability": 0.88}]),
        db_path=temp_db,
    )

    # Save assessment for User B
    save_assessment(
        user_id=user_b["id"],
        patient_name="Patient 02",
        age=60,
        symptoms="chest_pain, shortness_of_breath",
        top_prediction="Heart Attack",
        confidence=0.92,
        top3_json=json.dumps([{"disease": "Heart Attack", "probability": 0.92}]),
        db_path=temp_db,
    )

    records_a = get_user_assessments(user_a["id"], db_path=temp_db)
    records_b = get_user_assessments(user_b["id"], db_path=temp_db)

    assert len(records_a) == 1
    assert records_a[0]["patient_name"] == "Patient 01"
    assert records_a[0]["top_prediction"] == "Flu"

    assert len(records_b) == 1
    assert records_b[0]["patient_name"] == "Patient 02"
    assert records_b[0]["top_prediction"] == "Heart Attack"
