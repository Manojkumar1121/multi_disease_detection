"""
Clinical precautions and care guidance module.
Provides evidence-aligned, general-safety precautions and 'when to seek care'
guidelines for all 10 diseases in the dataset.
Strictly general safety guidance; contains no drug names or medication dosages.
"""

from typing import Dict, List, Any

PRECAUTIONS_DATA: Dict[str, Dict[str, Any]] = {
    "Asthma": {
        "precautions": [
            "Avoid known environmental triggers such as smoke, chemical fumes, cold air, and heavy dust.",
            "Maintain indoor air quality by using HEPA air purifiers and minimizing exposure to pet dander.",
            "Practice controlled breathing techniques (e.g., pursed-lip breathing) to assist airway recovery during mild distress.",
            "Keep warm and cover the nose and mouth with a scarf when transitioning into cold environments.",
        ],
        "when_to_seek_care": (
            "Seek emergency care immediately if experiencing severe breathlessness where speaking in full "
            "sentences is difficult, lips or fingernails appear bluish, or chest retraction occurs."
        ),
    },
    "Dengue": {
        "precautions": [
            "Maintain strict bed rest and drink abundant fluids (oral rehydration salts, coconut water, fresh fruit juices) to prevent dehydration.",
            "Use physical mosquito barriers, fine window netting, insect repellents, and wear long sleeves to prevent re-infection.",
            "Monitor body temperature and fluid intake/output regularly during the febrile and critical phases.",
            "Avoid intense physical exertion until complete clinical clearance and platelet stabilization.",
        ],
        "when_to_seek_care": (
            "Seek urgent emergency medical attention if severe abdominal pain, persistent vomiting, bleeding from "
            "the nose or gums, blood in stools, or profound fatigue/restlessness develops."
        ),
    },
    "Diabetes": {
        "precautions": [
            "Maintain consistent, balanced meal schedules emphasizing high-fiber vegetables, lean proteins, and complex carbohydrates.",
            "Engage in regular moderate physical activity (such as brisk 30-minute walks daily) to support metabolic health.",
            "Perform daily visual inspections of feet, heels, and toes for any small cuts, blisters, redness, or delayed wound healing.",
            "Stay adequately hydrated with water throughout the day and avoid sugar-sweetened beverages.",
        ],
        "when_to_seek_care": (
            "Seek urgent clinical evaluation if you experience sweet or fruity-smelling breath, persistent vomiting, "
            "extreme confusion, visual blurriness with dizziness, or signs of an infected non-healing sore."
        ),
    },
    "Flu": {
        "precautions": [
            "Prioritize complete bed rest and sleep to allow your body's immune defenses to fight the viral infection.",
            "Stay well-hydrated with warm herbal teas, clear broths, and water to replace fluids lost from fever.",
            "Practice proper respiratory etiquette by covering coughs with tissues and washing hands thoroughly with soap.",
            "Use a cool-mist humidifier or warm steam inhalation to relieve upper airway irritation and congestion.",
        ],
        "when_to_seek_care": (
            "Seek prompt medical attention if you experience shortness of breath, persistent chest pain, fever that "
            "returns after initial improvement, or inability to keep liquids down."
        ),
    },
    "Heart Attack": {
        "precautions": [
            "Stop all physical exertion immediately, remain completely calm, and sit or lie in a comfortable, supported position.",
            "Loosen tight clothing around the neck, chest, and waist to facilitate unrestricted airflow.",
            "Ensure someone remains with the patient continuously and keep doors unlocked for emergency responders.",
            "Do not attempt to drive yourself to a hospital under any circumstances.",
        ],
        "when_to_seek_care": (
            "Call local emergency medical services (e.g., 911 / 112) IMMEDIATELY. Acute coronary events require "
            "rapid emergency reperfusion within the golden hour."
        ),
    },
    "Hypertension": {
        "precautions": [
            "Adopt dietary approaches to stop hypertension (DASH diet), minimizing sodium intake and emphasizing fresh vegetables and potassium-rich foods.",
            "Incorporate daily moderate cardiovascular exercise like walking, swimming, or cycling for at least 30 minutes.",
            "Implement active stress-reduction routines including meditation, controlled breathing, and adequate nightly sleep (7-8 hours).",
            "Limit excessive caffeine, avoid tobacco and nicotine products, and maintain healthy body weight.",
        ],
        "when_to_seek_care": (
            "Seek immediate medical attention if elevated blood pressure is accompanied by a severe sudden headache, "
            "chest pain, visual blurriness, shortness of breath, or numbness/weakness in limbs."
        ),
    },
    "Kidney Disease": {
        "precautions": [
            "Follow physician-recommended fluid intake guidelines, balancing adequate hydration without causing fluid retention.",
            "Limit consumption of dietary sodium, processed foods, and high-potassium or high-phosphorus foods as advised by your clinical team.",
            "Avoid unmonitored over-the-counter pain medications that may impair renal filtration capacity.",
            "Monitor daily weight and check ankles, feet, and eyelids for signs of fluid retention and swelling.",
        ],
        "when_to_seek_care": (
            "Seek prompt medical care if you develop sudden swelling in the legs or face, significant decrease in urine output, "
            "blood in urine, shortness of breath on lying flat, or intractable nausea."
        ),
    },
    "Malaria": {
        "precautions": [
            "Rest in a quiet, cool, and well-ventilated room to manage alternating fever and chilling paroxysms.",
            "Drink plenty of fluids, oral rehydration solutions, and water to mitigate dehydration and electrolyte loss.",
            "Sleep under insecticide-treated bed nets and install window and door screens to avoid mosquito exposure.",
            "Wear long-sleeved, light-colored clothing covering extremities, especially between dusk and dawn.",
        ],
        "when_to_seek_care": (
            "Seek emergency medical evaluation promptly if you experience cyclical high fever, shaking chills, dark "
            "or tea-colored urine, jaundice (yellowing of eyes), or altered mental clarity."
        ),
    },
    "Migraine": {
        "precautions": [
            "Retire to a quiet, darkened, and cool room and close your eyes until the sensory sensitivity and pain peak passes.",
            "Apply a cold cloth or wrapped ice pack gently across the forehead or the back of the neck.",
            "Maintain a consistent headache diary noting potential triggers like missed meals, irregular sleep, bright lights, or specific foods.",
            "Maintain steady hydration and avoid skipping meals or sudden caffeine withdrawal.",
        ],
        "when_to_seek_care": (
            "Seek urgent emergency evaluation if experiencing an abrupt 'thunderclap' headache, headache accompanied "
            "by high fever and stiff neck, confusion, seizure, or focal neurological numbness/speech difficulty."
        ),
    },
    "Pneumonia": {
        "precautions": [
            "Ensure strict bed rest and avoid returning to strenuous activity until full clinical recovery and fever resolution.",
            "Drink ample warm fluids, broths, and water to thin respiratory secretions and prevent dehydration.",
            "Inhale gentle warm steam or use a clean cool-mist humidifier to ease persistent chest discomfort and coughing.",
            "Rest in an elevated or semi-reclined posture to facilitate easier chest expansion and lung ventilation.",
        ],
        "when_to_seek_care": (
            "Seek emergency medical care immediately if experiencing severe difficulty breathing, persistent pain in the chest "
            "when breathing or coughing, coughing up blood, or bluish tint to lips or fingertips."
        ),
    },
}

DEFAULT_PRECAUTIONS = {
    "precautions": [
        "Consult a qualified healthcare provider for comprehensive clinical evaluation and tailored diagnosis.",
        "Rest adequately, maintain consistent hydration, and monitor your symptoms closely.",
        "Keep a detailed log of symptom onset, duration, and severity to share with your clinician.",
    ],
    "when_to_seek_care": (
        "Seek urgent medical evaluation if your symptoms worsen suddenly, or if you experience chest pain, "
        "shortness of breath, high fever, or loss of consciousness."
    ),
}


def get_precautions_for_disease(disease: str) -> Dict[str, Any]:
    """
    Retrieve clinical precautions and 'when to seek care' advice for a given disease.
    Returns general fallback advice if disease is unknown or weak input.
    """
    return PRECAUTIONS_DATA.get(disease, DEFAULT_PRECAUTIONS)
