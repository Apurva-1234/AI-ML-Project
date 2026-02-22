import os
import zipfile
import requests
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import cv2
from backend.utils import CLASSES

DATA_DIR = os.path.join(os.getcwd(), 'data', 'gtsrb')
MODEL_PATH = os.path.join(os.getcwd(), 'models', 'traffic_sign_model.h5')

def download_dataset():
    """
    Downloads GTSRB dataset if not present.
    """
    
    url = "https://sid.erda.dk/public/archives/daaeac0d7ce1152aea9b61d9f1e19370/GTSRB_Final_Training_Images.zip"
    zip_path = os.path.join(DATA_DIR, "GTSRB_Final_Training_Images.zip")
    
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
        
    if not os.path.exists(zip_path) or os.path.getsize(zip_path) < 1000000:
        print("Downloading GTSRB dataset (~260MB)... this will take a moment.")
        try:
            
            response = requests.get(url, stream=True, timeout=60, verify=True)
            response.raise_for_status()
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=65536):
                    if chunk:
                        f.write(chunk)
            print("Download complete.")
        except Exception as e:
            print(f"Download failed: {e}")
            print("Please try downloading manually from: https://sid.erda.dk/public/archives/daaeac0d7ce1152aea9b61d9f1e19370/GTSRB_Final_Training_Images.zip")
            print(f"And place it in: {zip_path}")
            return

    if not os.path.exists(os.path.join(DATA_DIR, 'GTSRB')):
        print("Extracting dataset... please wait.")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(DATA_DIR)
            print("Extraction complete.")
        except zipfile.BadZipFile:
            print("Error: The downloaded file is corrupt. Deleting it for a retry.")
            if os.path.exists(zip_path):
                os.remove(zip_path)

def build_model(input_shape=(32, 32, 3), num_classes=43):
    from tensorflow.keras.models import Sequential
    model = Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def load_data(data_dir, target_size=(32, 32)):
    images = []
    labels = []
    
    
    base_path = os.path.join(data_dir, 'GTSRB', 'Final_Training', 'Images')
    if not os.path.exists(base_path):
        base_path = os.path.join(data_dir, 'Final_Training', 'Images')

    if not os.path.exists(base_path):
       
        for root, dirs, files in os.walk(data_dir):
            if '00000' in dirs:
                base_path = root
                break

    if not os.path.exists(base_path):
        raise Exception(f"Dataset path not found inside {data_dir}. Please ensure it extracted correctly.")

    print(f"Loading data from: {base_path}")
    for class_id in range(43):
        class_folder = format(class_id, '05d')
        class_path = os.path.join(base_path, class_folder)
        if not os.path.exists(class_path):
            continue
            
        count = 0
        img_names = os.listdir(class_path)
        
        for img_name in img_names:
            if img_name.lower().endswith(('.ppm', '.jpg', '.png')):
                img = cv2.imread(os.path.join(class_path, img_name))
                if img is None: continue
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, target_size)
                images.append(img)
                labels.append(class_id)
                count += 1
                if count >= 300: break
                
    return np.array(images), np.array(labels)

def train_traffic_sign_model(epochs=10, batch_size=64):
    try:
        download_dataset()
        X, y = load_data(DATA_DIR)
        if len(X) == 0:
            raise Exception("No images found in dataset!")
            
        X = X / 255.0
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        
        datagen = ImageDataGenerator(
            rotation_range=10,
            zoom_range=0.1,
            width_shift_range=0.1,
            height_shift_range=0.1,
            shear_range=0.1
        )
        
        model = build_model()
        history = model.fit(
            datagen.flow(X_train, y_train, batch_size=batch_size),
            epochs=epochs,
            validation_data=(X_val, y_val),
            verbose=1
        )
        
        if not os.path.exists(os.path.dirname(MODEL_PATH)):
            os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
            
        model.save(MODEL_PATH)
        return history.history
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    train_traffic_sign_model()
