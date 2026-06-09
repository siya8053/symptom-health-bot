from flask import Flask, render_template, request, jsonify
import os
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

conditions = {
    "Anxiety and Panic Disorder": {
        "symptoms": ["chest tightness", "anxiety", "weakness", "irritability", "restlessness", "low mood"],
        "description": "A mental health condition where intense fear or worry triggers physical symptoms.",
        "causes": ["Stress", "Hormonal imbalance", "Lifestyle factors"],
        "precautions": ["Regular sleep", "Meditation", "Limit caffeine"],
        "remedy": ["Deep breathing", "Yoga", "Exercise"]
    },

    "Dehydration": {
        "symptoms": ["headache", "weakness", "nausea", "fatigue", "dizziness", "dry skin"],
        "description": "Loss of body fluids affecting normal body functions.",
        "causes": ["Low water intake", "Heat exposure", "Excess sweating"],
        "precautions": ["Drink water regularly", "Eat fruits", "Avoid heat"],
        "remedy": ["ORS", "Coconut water", "Rest"]
    },

    "Flu / Viral Infection": {
        "symptoms": ["fever", "fatigue", "body ache", "chills", "cough"],
        "description": "A viral infection affecting respiratory system.",
        "causes": ["Virus exposure", "Weak immunity"],
        "precautions": ["Hygiene", "Avoid cold", "Rest"],
        "remedy": ["Warm fluids", "Steam inhalation"]
    },

    "Migraine": {
        "symptoms": ["headache", "light sensitivity", "nausea", "dizziness"],
        "description": "Severe headache often with sensitivity to light and nausea.",
        "causes": ["Stress", "Lack of sleep", "Hormonal changes"],
        "precautions": ["Reduce screen time", "Sleep well"],
        "remedy": ["Cold compress", "Dark room rest"]
    },

    "Food Poisoning": {
        "symptoms": ["nausea", "vomiting", "diarrhea", "stomach pain"],
        "description": "Illness caused by contaminated food.",
        "causes": ["Bacteria", "Spoiled food"],
        "precautions": ["Eat fresh food", "Maintain hygiene"],
        "remedy": ["ORS", "Light diet"]
    },

    "Common Cold": {
        "symptoms": ["cough", "runny nose", "sore throat", "sneezing"],
        "description": "Mild viral infection affecting nose and throat.",
        "causes": ["Cold weather", "Virus"],
        "precautions": ["Stay warm", "Avoid cold drinks"],
        "remedy": ["Steam inhalation", "Warm fluids"]
    },

    "Anemia": {
        "symptoms": ["fatigue", "weakness", "dizziness", "pale skin"],
        "description": "Condition due to low red blood cells.",
        "causes": ["Iron deficiency", "Poor diet"],
        "precautions": ["Iron-rich diet"],
        "remedy": ["Spinach", "Dates", "Supplements"]
    },

    "Diabetes": {
    "symptoms": ["frequent urination", "excessive thirst", "fatigue",
                 "blurred vision", "weight loss", "increased hunger"],
    "description": "High blood sugar condition affecting body metabolism.",
    "causes": ["Poor insulin function", "Genetics", "Obesity"],
    "precautions": ["Reduce sugar intake", "Exercise regularly", "Monitor glucose"],
    "remedy": ["Drink water", "Healthy diet", "Regular checkup"]
},

"Asthma": {
    "symptoms": ["shortness of breath", "wheezing", "chest tightness",
                 "cough", "difficulty breathing"],
    "description": "Respiratory condition causing breathing difficulty.",
    "causes": ["Allergy", "Dust", "Pollution", "Cold air"],
    "precautions": ["Avoid smoke", "Avoid allergens", "Use inhaler"],
    "remedy": ["Steam inhalation", "Rest", "Warm fluids"]
},

"COVID-19": {
    "symptoms": ["fever", "dry cough", "fatigue",
                 "loss of taste", "loss of smell", "breathing difficulty"],
    "description": "Viral infection caused by coronavirus.",
    "causes": ["Virus exposure", "Crowded places"],
    "precautions": ["Wear mask", "Wash hands", "Social distancing"],
    "remedy": ["Isolation", "Hydration", "Rest"]
},

"Typhoid": {
    "symptoms": ["high fever", "weakness", "stomach pain",
                 "headache", "loss of appetite"],
    "description": "Bacterial infection caused by contaminated food and water.",
    "causes": ["Poor hygiene", "Contaminated water"],
    "precautions": ["Drink clean water", "Eat hygienic food"],
    "remedy": ["ORS", "Rest", "Doctor consultation"]
},

"Allergy": {
    "symptoms": ["sneezing", "itching", "skin rash",
                 "runny nose", "watery eyes"],
    "description": "Immune system reaction to allergens.",
    "causes": ["Dust", "Pollen", "Food allergy"],
    "precautions": ["Avoid allergens", "Maintain cleanliness"],
    "remedy": ["Antihistamines", "Drink water"]
},

"Stress": {
    "symptoms": ["anxiety", "headache", "fatigue",
                 "sleep problems", "irritability"],
    "description": "Mental pressure affecting physical and emotional health.",
    "causes": ["Work pressure", "Lack of sleep", "Overthinking"],
    "precautions": ["Meditation", "Exercise", "Take breaks"],
    "remedy": ["Relaxation", "Music", "Deep breathing"]
},

"Indigestion": {
    "symptoms": ["stomach pain", "bloating", "nausea",
                 "heartburn", "gas"],
    "description": "Digestive discomfort after eating.",
    "causes": ["Spicy food", "Overeating", "Fast eating"],
    "precautions": ["Eat slowly", "Avoid oily food"],
    "remedy": ["Warm water", "Light diet"]
},

"Dengue": {
    "symptoms": ["high fever", "joint pain", "muscle pain",
                 "skin rash", "headache"],
    "description": "Mosquito-borne viral infection.",
    "causes": ["Mosquito bites"],
    "precautions": ["Use mosquito nets", "Avoid stagnant water"],
    "remedy": ["Hydration", "Rest", "Doctor consultation"]
},

"Malaria": {
    "symptoms": ["fever", "chills", "sweating",
                 "headache", "vomiting"],
    "description": "Mosquito-borne parasitic disease.",
    "causes": ["Mosquito bites"],
    "precautions": ["Use mosquito repellent", "Sleep under nets"],
    "remedy": ["Rest", "Fluids", "Medical treatment"]
}
}
@app.route('/analyze', methods=['POST'])
def analyze():
    selected = [s.strip().lower() for s in request.json.get("symptoms", [])]

    results = []

    for name, data in conditions.items():
        condition_symptoms = [s.lower() for s in data["symptoms"]]

        match = len(set(selected) & set(condition_symptoms))
        percent = int((match / max(len(selected), 1)) * 100)

        if match > 0:
            results.append({
                "name": name,
                "percent": max(percent, 20),
                "desc": data["description"],
                "causes": data["causes"],
                "precautions": data["precautions"],
                "remedy": data["remedy"]
            })

    if not results:
        results.append({
            "name": "General Health Issue",
            "percent": 30,
            "desc": "Symptoms are not strongly matching any condition.",
            "causes": ["Stress", "Lifestyle", "Diet"],
            "precautions": ["Healthy routine", "Hydration"],
            "remedy": ["Rest", "Balanced diet"]
        })

    results = sorted(results, key=lambda x: x["percent"], reverse=True)

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
    