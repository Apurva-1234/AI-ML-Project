import cv2
import os

base_path = r'c:\Users\Admin\Documents\AIML\Traffic signal recognization\data\gtsrb\GTSRB\Final_Training\Images'
samples_path = r'c:\Users\Admin\Documents\AIML\Traffic signal recognization\samples'

samples = {
    '00014': 'stop_sign.jpg',
    '00002': 'speed_50.jpg',
    '00017': 'no_entry.jpg'
}

for folder, name in samples.items():
    folder_path = os.path.join(base_path, folder)
    if os.path.exists(folder_path):
        # Get the first ppm file
        ppms = [f for f in os.listdir(folder_path) if f.endswith('.ppm')]
        if ppms:
            img_path = os.path.join(folder_path, ppms[20]) # Pick one that's usually clearer (middle of sequence)
            img = cv2.imread(img_path)
            if img is not None:
                target = os.path.join(samples_path, name)
                cv2.imwrite(target, img)
                print(f"Converted {img_path} to {target}")
            else:
                print(f"Failed to read {img_path}")
        else:
            print(f"No ppm files in {folder_path}")
    else:
        print(f"Folder {folder_path} not found")
