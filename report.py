"""
Clinical assessment report generation module using fpdf2.
Generates a downloadable clinical summary report containing:
- Patient demographics (name, age)
- Reported symptoms
- Top 3 candidate diseases with ensemble probabilities
- Key contributing symptoms (leave-one-symptom-out attribution)
- Recommended precautions and 'when to seek care' guidance
- Emergency red-flag notices
- Medical disclaimer and generation timestamp
"""

from datetime import datetime, timezone
from typing import List, Dict, Any, Tuple, Optional
from fpdf import FPDF, XPos, YPos


class ClinicalReportPDF(FPDF):
    """Clean, medical-styled PDF generator for assessment results."""

    def header(self):
        # Header banner bar
        self.set_fill_color(30, 58, 138)  # Deep clinical blue
        self.rect(0, 0, 210, 16, "F")
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 11)
        self.set_xy(10, 4)
        self.cell(190, 8, "MULTI-DISEASE DECISION SUPPORT SYSTEM  |  ASSESSMENT REPORT", align="L")
        self.ln(14)

    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 8, f"Page {self.page_no()}/{{nb}}  |  Confidential Medical Assessment Document", align="C")


def generate_pdf_report(
    patient_name: str,
    age: int,
    symptoms: List[str],
    top_prediction: str,
    confidence: float,
    top3: List[Dict[str, Any]],
    contributing_symptoms: List[Dict[str, Any]],
    precautions_info: Dict[str, Any],
    red_flag_info: Tuple[bool, List[str]],
    timestamp_str: Optional[str] = None,
) -> bytes:
    """
    Generate PDF assessment report as raw bytes for download.
    """
    if timestamp_str is None:
        timestamp_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    pdf = ClinicalReportPDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Document Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, "Clinical Risk Assessment Summary", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, f"Report Generated: {timestamp_str}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    # 1. Emergency Red-Flag Banner (if triggered)
    has_red_flags, red_flag_rules = red_flag_info
    if has_red_flags:
        pdf.set_fill_color(254, 242, 242)
        pdf.set_draw_color(239, 68, 68)
        pdf.set_line_width(0.5)
        pdf.rect(10, pdf.get_y(), 190, 20, "DF")
        pdf.set_xy(14, pdf.get_y() + 2)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(185, 28, 28)
        pdf.cell(180, 6, "CRITICAL NOTICE: POTENTIAL EMERGENCY DETECTED", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_xy(14, pdf.get_y())
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(127, 29, 29)
        rules_text = " | ".join(red_flag_rules)
        pdf.multi_cell(180, 4.5, f"Triggered rules: {rules_text}. Seek urgent clinical evaluation or call emergency services.")
        pdf.ln(6)
    else:
        pdf.set_fill_color(240, 253, 244)
        pdf.set_draw_color(74, 222, 128)
        pdf.set_line_width(0.3)
        pdf.rect(10, pdf.get_y(), 190, 8, "DF")
        pdf.set_xy(14, pdf.get_y() + 1.5)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(22, 101, 52)
        pdf.cell(180, 5, "No critical emergency symptom combinations triggered.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(4)

    # 2. Patient Demographics Box
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(10, pdf.get_y(), 190, 18, "DF")
    pdf.set_xy(14, pdf.get_y() + 3)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(40, 6, f"Patient Name: {patient_name}")
    pdf.cell(30, 6, f"Age: {int(age)}")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(71, 85, 105)
    symptom_str = ", ".join(symptoms) if symptoms else "None selected"
    if len(symptom_str) > 70:
        symptom_str = symptom_str[:67] + "..."
    pdf.cell(0, 6, f"Reported Symptoms: {symptom_str}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(12)

    # 3. Model Diagnostic Evaluation
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 7, "Diagnostic Prediction & Differential", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(50, 6, f"Primary Prediction: {top_prediction}")
    pdf.cell(0, 6, f"Ensemble Confidence: {confidence:.1%}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    # Top 3 table
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(237, 242, 247)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(10, 6, "#", border=1, fill=True, align="C")
    pdf.cell(120, 6, "Candidate Disease", border=1, fill=True)
    pdf.cell(60, 6, "Probability", border=1, fill=True, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(15, 23, 42)
    for idx, cand in enumerate(top3[:3], 1):
        pdf.cell(10, 5.5, str(idx), border=1, align="C")
        pdf.cell(120, 5.5, cand.get("disease", "N/A"), border=1)
        pdf.cell(60, 5.5, f"{cand.get('probability', 0.0):.1%}", border=1, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    # 4. Key Contributing Symptoms (LOSO)
    if contributing_symptoms:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(30, 58, 138)
        pdf.cell(0, 6, "Key Contributing Symptoms (Leave-One-Symptom-Out Attribution)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font("Helvetica", "B", 8)
        pdf.set_fill_color(237, 242, 247)
        pdf.set_text_color(51, 65, 85)
        pdf.cell(80, 5.5, "Selected Symptom", border=1, fill=True)
        pdf.cell(55, 5.5, "Probability Drop (Marginal Impact)", border=1, fill=True, align="R")
        pdf.cell(55, 5.5, "Confidence Without Symptom", border=1, fill=True, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(15, 23, 42)
        for item in contributing_symptoms[:5]:
            s_name = item["symptom"].replace("_", " ").title()
            pdf.cell(80, 5, s_name, border=1)
            pdf.cell(55, 5, f"{item['drop']:+.1%}", border=1, align="R")
            pdf.cell(55, 5, f"{item['prob_without']:.1%}", border=1, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(4)

    # 5. Clinical Safety Precautions
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 6, f"Recommended Safety Guidance ({top_prediction})", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(30, 41, 59)
    precautions_list = precautions_info.get("precautions", [])
    for tip in precautions_list:
        pdf.multi_cell(190, 5, f"- {tip}")

    when_care = precautions_info.get("when_to_seek_care")
    if when_care:
        pdf.ln(1)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(185, 28, 28)
        pdf.multi_cell(190, 5, f"When to Seek Immediate Care: {when_care}")

    pdf.ln(3)

    # 6. Disclaimer
    pdf.set_fill_color(241, 245, 249)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(10, pdf.get_y(), 190, 22, "DF")
    pdf.set_xy(12, pdf.get_y() + 2)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(186, 4, "LEGAL & CLINICAL DISCLAIMER", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_xy(12, pdf.get_y())
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(100, 116, 139)
    pdf.multi_cell(
        186,
        3.5,
        "This automated report is generated by a multi-model machine learning research prototype for decision support "
        "and educational purposes only. It DOES NOT provide a definitive diagnosis, clinical prescription, or therapy plan. "
        "Diagnostic outcomes must be independently reviewed and verified by a licensed, certified medical doctor or clinician."
    )

    return bytes(pdf.output())
