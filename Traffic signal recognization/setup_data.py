from backend.train import download_dataset
import os

print("Starting dataset download and extraction...")
download_dataset()
print("Process completed.")

base_path = os.path.join('data', 'gtsrb', 'GTSRB', 'Final_Training', 'Images')
if os.path.exists(base_path):
    print(f"Success! Folder found at: {os.path.abspath(base_path)}")
    print(f"Number of class folders: {len(os.listdir(base_path))}")
else:
    print(f"Error: Folder still not found at {base_path}")
