import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import base64
import io

def add_bg(local_image_path):
    with open(local_image_path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .block-container {{
            background: rgba(0,0,0,0.60);
            padding: 20px;
            border-radius: 12px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg("/Users/sarthakbhatnagar/Downloads/STHK/bgimage.jpg")

# 🔥 FIXED MODEL LOAD
model = tf.keras.models.load_model("plant_model.keras", safe_mode=False, compile=False)

img_size = 64

class_names = [
    'Pepper__bell___Bacterial_spot',
    'Pepper__bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Tomato_Bacterial_spot',
    'Tomato_Early_blight',
    'Tomato_Late_blight',
    'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite',
    'Tomato__Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus',
    'Tomato__Tomato_mosaic_virus',
    'Tomato_healthy'
]

def split_prediction(label):
    clean = label.replace("__", "_").replace("___", "_")
    parts = clean.split("_")
    if parts[-1].lower() == "healthy":
        plant = " ".join(parts[:-1])
        disease = "Healthy"
    else:
        plant = parts[0]
        disease = " ".join(parts[1:]).replace("_", " ")
    return plant.capitalize(), disease.capitalize()

treatments = {
    "Bacterial spot": [
        "Spray Copper Oxychloride 50% WP",
        "Use Streptocycline (100 ppm)",
        "Avoid overhead irrigation",
        "Remove infected leaves"
    ],
    "Early blight": [
        "Spray Mancozeb 75% WP",
        "Use Chlorothalonil",
        "Improve air circulation"
    ],
    "Late blight": [
        "Use Metalaxyl + Mancozeb (Ridomil Gold)",
        "Spray Dimethomorph",
        "Destroy infected plants"
    ],
    "Leaf mold": [
        "Spray Copper Fungicide",
        "Improve airflow"
    ],
    "Septoria leaf spot": [
        "Apply Mancozeb or Chlorothalonil",
        "Remove infected leaves"
    ],
    "Spider mites two spotted spider mite": [
        "Spray Abamectin 1.9% EC",
        "Use Neem Oil 0.5%"
    ],
    "Target spot": [
        "Spray Difenoconazole",
        "Remove infected leaves"
    ],
    "Tomato yellowleaf curl virus": [
        "Use Imidacloprid (whitefly control)",
        "Remove infected plants"
    ],
    "Tomato mosaic virus": [
        "Remove infected plants",
        "Disinfect tools"
    ],
    "Healthy": [
        "No treatment needed ✔️ Plant is healthy."
    ]
}

descriptions = {
    "Bacterial spot": "A bacterial infection causing spots & leaf damage.",
    "Early blight": "Fungal disease causing brown concentric target-like spots.",
    "Late blight": "Severe fungal disease favored by cool, humid weather.",
    "Leaf mold": "Thrives in humid areas, causing yellow patches under leaves.",
    "Healthy": "No symptoms detected."
}

def water_stress_score(image):
    gray = np.mean(np.array(image.resize((100, 100))), axis=2)
    dryness = np.mean(gray)
    score = max(0, min(100, (dryness / 255) * 100))
    return round(score, 2)

def disease_severity(image):
    gray = np.mean(np.array(image.resize((100, 100))), axis=2)
    damage = np.sum(gray < 100) / gray.size
    return round(damage * 100, 2)

fertilizer = {
    "Tomato": "Apply 15-15-15 NPK or organic compost every 2 weeks.",
    "Pepper": "Use 5-10-10 fertilizer every 15 days.",
    "Potato": "Apply 10-20-20 NPK at planting stage."
}

def generate_pdf(plant, disease, conf, treat_list):
    from reportlab.pdfgen import canvas
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 800, "Plant Disease Report")
    c.drawString(100, 770, f"Plant: {plant}")
    c.drawString(100, 750, f"Disease: {disease}")
    c.drawString(100, 730, f"Confidence: {conf:.2f}%")
    c.drawString(100, 700, "Treatment:")
    y = 680
    for t in treat_list:
        c.drawString(120, y, f"- {t}")
        y -= 20
    c.save()
    buffer.seek(0)
    return buffer

st.title("🌿 Smart Plant Disease Detection System")

uploaded = st.file_uploader("📤 Upload leaf image", type=["jpg", "jpeg", "png"])

if uploaded:
    image = Image.open(uploaded)
    st.image(image, width=300)

    if st.button("🔍 Predict Disease"):
        image_resized = image.resize((img_size, img_size))
        img_array = np.expand_dims(np.array(image_resized), 0)

        preds = model.predict(img_array)
        result = np.argmax(preds)
        confidence = np.max(preds) * 100

        predicted_label = class_names[result]
        plant_name, disease_name = split_prediction(predicted_label)

        st.subheader("🔍 Prediction Result")
        st.write("🌱 **Plant:**", plant_name)
        st.write("🦠 **Disease:**", disease_name)

        st.write("📊 **Confidence:**")
        st.progress(int(confidence))

        sev = disease_severity(image)
        st.write(f"🔥 **Disease Severity:** {sev}%")

        ws = water_stress_score(image)
        st.write(f"💧 **Water Stress Score:** {ws}%")

        st.subheader("💊 Recommended Treatment")
        found = False
        for t_key in treatments:
            if t_key.lower() in disease_name.lower():
                for item in treatments[t_key]:
                    st.write("✔️", item)
                found = True
                break

        fert = fertilizer.get(plant_name, "Use balanced NPK fertilizer.")
        st.subheader("🌱 Fertilizer Recommendation")
        st.write(fert)

        treat_list = treatments.get(disease_name.lower(), ["No treatment info available"])

        try:
            pdf = generate_pdf(plant_name, disease_name, confidence, treat_list)
            st.download_button("📥 Download Report as PDF", data=pdf, file_name="report.pdf")
        except:
            st.error("PDF generation failed. Install reportlab: pip install reportlab")
