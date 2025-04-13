from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from PIL import Image
import io
import tensorflow as tf
from tensorflow.keras.models import load_model

# Initialize FastAPI app
app = FastAPI()

# Enable CORS to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained TensorFlow model
MODEL_PATH = "C:/Users/Om/Desktop/OM/proj/baseline_cnn.keras"

try:
    model = load_model(MODEL_PATH)
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Define image preprocessing
def preprocess_image(image_bytes):
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("L")  # Convert to grayscale (1 channel)
        img = img.resize((128, 128))  # Resize to model's input size
        img_array = np.array(img, dtype=np.float32) / 255.0  # Normalize pixel values
        img_array = np.expand_dims(img_array, axis=-1)  # Add channel dimension (H, W, 1)
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension (1, H, W, 1)
        
        print(f"Processed image shape: {img_array.shape}")  # Debugging line
        return img_array
    except Exception as e:
        print(f"Error in preprocessing: {e}")
        return None

# Define detailed dementia categories
class_info = {
    0: {
        "category": "Non Demented",
        "description": "Individuals with normal cognitive function, experiencing only typical age-related memory changes. No significant cognitive decline.",
        "characteristics": [
            "Occasional forgetfulness (e.g., misplacing items, forgetting names temporarily).",
            "No significant impact on daily life activities.",
            "Can learn new skills and retain memory with minimal difficulty.",
            "No language, orientation, or behavioral issues."
        ],
        "advice": [
            "Maintain a healthy diet rich in omega-3, fruits, and vegetables.",
            "Engage in mental exercises like puzzles, reading, and learning new skills.",
            "Stay socially active to improve cognitive resilience.",
            "Regular physical activity to enhance blood flow to the brain.",
            "Regular medical check-ups to monitor cognitive health."
        ]
    },
    1: {
        "category": "Very Mild Demented",
        "description": "Early stage of cognitive decline where minor memory lapses occur, but daily functions remain largely unaffected.",
        "characteristics": [
            "Minor short-term memory loss (e.g., forgetting appointments, difficulty recalling names).",
            "Mild difficulty in concentration and problem-solving.",
            "No severe behavioral or emotional changes.",
            "Can still handle daily activities without much assistance."
        ],
        "advice": [
            "Routine cognitive exercises like crosswords, chess, and memory games.",
            "Maintain a structured routine to reduce forgetfulness.",
            "Encourage social interactions to keep the brain active.",
            "Regular sleep schedule and stress management to support brain function.",
            "Monitor for progression with regular cognitive assessments."
        ]
    },
    2: {
        "category": "Mild Demented",
        "description": "Mild Dementia due to Alzheimer's Disease, where individuals begin to experience noticeable cognitive impairments affecting daily life.",
        "characteristics": [
            "Memory problems such as difficulty remembering recent conversations, events, and appointments.",
            "Cognitive challenges including struggles with problem-solving and decision-making.",
            "Language & communication issues such as trouble finding words and following conversations.",
            "Mood & behavioral changes including increased anxiety, depression, or irritability.",
            "Loss of orientation leading to getting lost in familiar places or forgetting directions."
        ],
        "advice": [
            "Consider medication for early intervention, such as cholinesterase inhibitors.",
            "Establish a daily routine to reduce confusion.",
            "Use assistive tools like reminders, calendars, and notes to assist memory.",
            "Encourage mild physical activity and brain exercises.",
            "Family and friends should start providing mild supervision."
        ]
    },
    3: {
        "category": "Fully Demented",
        "description": "Severe cognitive decline causing loss of independence, requiring full-time care and assistance.",
        "characteristics": [
            "Severe memory loss, forgetting family members, personal history, and common knowledge.",
            "Loss of motor skills, including difficulty in walking, sitting, or even swallowing food.",
            "Complete disorientation, unable to recognize familiar surroundings or the time of day.",
            "Severe language impairments, unable to communicate effectively.",
            "Extreme mood swings & behavioral changes including aggression, paranoia, or extreme apathy."
        ],
        "advice": [
            "Requires full-time supervision and support.",
            "Ensure a safe living environment, removing hazards and providing a calm space.",
            "Provide nutritional support such as soft or liquid foods for swallowing difficulties.",
            "Medical intervention for symptom management and comfort care.",
            "Emotional and psychological support for caregivers is equally important."
        ]
    }
}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image_array = preprocess_image(image_bytes)

        # Debugging: Print the processed image shape
        print(f"Processed image shape: {image_array.shape}")  

        # Ensure correct shape before passing to the model
        if image_array.shape != (1, 128, 128, 1):  # Fix: Match model input shape
            return {"error": f"Invalid input shape {image_array.shape}, expected (1, 128, 128, 1)"}


        predictions = model.predict(image_array)
        prediction_index = np.argmax(predictions, axis=1)[0]

        prediction_data = class_info.get(prediction_index, {"category": "Unknown", "description": "", "characteristics": [], "advice": []})

        return prediction_data
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}
