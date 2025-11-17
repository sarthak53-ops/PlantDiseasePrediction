🌱 Plant Disease Prediction — Deep Learning Web App
This project is a simple and easy-to-use Plant Disease Detection Web App.
You can upload a picture of a plant leaf, and the app will tell you whether the plant is healthy or if it’s affected by a disease — using a trained deep learning model.
🚀 Features
Upload an image of a leaf and get an instant prediction
Uses a trained TensorFlow/Keras deep learning model
Clean and user-friendly Streamlit interface
Fully local — works offline once installed
Jupyter notebook included for experiments and training
🧠 How It Works
The project uses a CNN (Convolutional Neural Network) trained on plant leaf images.
The model learns patterns like color, texture, and shape to identify diseases accurately.
The final trained model is saved as:
plant_model.keras
🛠️ Technology Stack
Python
TensorFlow / Keras
Streamlit (for the web interface)
NumPy, OpenCV, PIL (for image processing)
Jupyter Notebook (for training and testing)
📁 Project Structure
PlantDiseasePrediction/
│── app.py                # Main Streamlit application
│── plant_model.keras     # Trained deep learning model
│── main.ipynb            # Notebook used for training/analysis
│── bgimage.jpg           # Background image used in UI
│── requirements.txt      # Python dependencies
│── Crop Prediction/      # Extra crop-related module
│── README.md
📦 Installation
Make sure you have Python installed.
Install all required libraries:
pip install -r requirements.txt
▶️ Running the App
Start the Streamlit app using:
streamlit run app.py
The app will open automatically in your browser at:
http://localhost:8501
Upload a leaf image and let the model predict!
🔮 Future Ideas
Here are some improvements planned for the future:
Add more plant and disease categories
Improve model accuracy with better datasets
Deploy the app online (Streamlit Cloud, HuggingFace)
Add suggestions for treatments and crop care
🤝 Contributions
If you want to improve the project, feel free to open an issue or submit a pull request.
All contributions are appreciated.
👨‍💻 Author
Sarthak Bhatnagar
GitHub: sarthak53-ops
⭐ Support
If you like this project, please give it a ⭐ on GitHub — it really helps!
