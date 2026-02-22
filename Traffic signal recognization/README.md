# DriveSense AI | Traffic Sign Recognition System

DriveSense AI is a complete end-to-end Traffic Sign Recognition system built for autonomous vehicle research. It uses a Deep Convolutional Neural Network (CNN) trained on the German Traffic Sign Recognition Benchmark (GTSRB) to classify 43 categories of traffic signs.

## Features
- CNN Classification: High-accuracy classifier built with TensorFlow/Keras.
- FastAPI Backend: High-performance REST API for inference and training.
- Premium Frontend: Clean, modern dashboard using Tailwind CSS and Vanilla JS.
- Real-time Detection: Webcam integration using OpenCV and browser media API.
- Automated Training: Background training task with progress tracking and performance charts.

## Tech Stack
- Backend: Python, FastAPI, TensorFlow, OpenCV, NumPy, Scikit-learn.
- Frontend: HTML5, Tailwind CSS, Vanilla JavaScript, Chart.js.
- Model: CNN (Conv2D -> BatchNormalization -> MaxPooling -> Dropout -> Dense).

##  Project Structure
```text
/
├── backend/
│   ├── app.py          # FastAPI application
│   ├── train.py        # Model training and data loading
│   └── utils.py        # Image preprocessing and class mapping
├── frontend/
│   ├── index.html      # Main dashboard UI
│   └── app.js          # Frontend logic and API calls
├── models/             # Directory for saved .h5 models
├── data/               # Directory for GTSRB dataset
└── requirements.txt    # Python dependencies
```

## Setup Instructions

### 1. Install Dependencies
Ensure you have Python 3.8+ installed. Run:
```bash
pip install -r requirements.txt
```

### 2. Run the Backend
Start the FastAPI server:
```bash
python -m backend.app
```
The API will be available at `http://localhost:8000`.

### 3. Open the Frontend
You can open `frontend/index.html` directly in your browser or serve it using any local web server (e.g., Live Server in VS Code or `python -m http.server`).

### 4. Training the Model
- You can trigger training via the **"Retrain Model"** button in the UI.
- The system will automatically download the GTSRB dataset (~300MB) to the `data/` folder if it's not present.
- Training progress will be shown in the "Model Training Portal" section.

## Usage
- **Upload:** Use the "Upload Image" button to test the model on a single image.
- **Webcam:** Click "Start Webcam" to toggle real-time recognition.
- **Metrics:** After training, accuracy curves will be displayed in the dashboard.

## 📘 Model Details
The architecture consists of three convolutional blocks with batch normalization and dropout to prevent overfitting. It achieves >95% accuracy on the GTSRB validation set after 10-20 epochs.
