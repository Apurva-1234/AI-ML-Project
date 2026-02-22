import cv2
import numpy as np
import tensorflow as tf
import os
from backend.utils import preprocess_image, get_class_name

MODEL_PATH = os.path.join('models', 'traffic_sign_model.h5')

def run_webcam_demo():
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model not found at {MODEL_PATH}. Please train the model first.")
        return

    print("Loading model...")
    model = tf.keras.models.load_model(MODEL_PATH)
    
    cap = cv2.VideoCapture(0)
    
    print("Webcam started. Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Draw detection box/text placeholder
        # In a real app, you might want to crop the sign, but here we'll just classify the center or whole frame
        
        # Preprocess frame
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # We'll take a center crop for better results on small signs
        h, w, _ = rgb_frame.shape
        size = min(h, w)
        start_x = (w - size) // 2
        start_y = (h - size) // 2
        crop = rgb_frame[start_y:start_y+size, start_x:start_x+size]
        
        # Resizing and normalizing as done in utils
        processed = cv2.resize(crop, (32, 32)) / 255.0
        processed = np.expand_dims(processed, axis=0)
        
        # Prediction
        preds = model.predict(processed, verbose=0)
        class_id = np.argmax(preds)
        confidence = np.max(preds)
        
        class_name = get_class_name(class_id)
        
        # Display results on frame
        label = f"{class_name} ({confidence*100:.1f}%)"
        cv2.putText(frame, label, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.rectangle(frame, (start_x, start_y), (start_x+size, start_y+size), (255, 0, 0), 2)
        
        cv2.imshow('Traffic Sign Recognition - Local Demo', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_webcam_demo()
