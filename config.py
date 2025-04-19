# config.py

import os

# Load API key from environment variable
api_key = os.getenv("FLYWHEEL_API_KEY")
if not api_key:
    raise EnvironmentError("Environment variable 'FLYWHEEL_API_KEY' is not set.")

# Flywheel project details
flywheel_group = "baschnagelgroup"
flywheel_project = "NYU_MRI_Dataset"

# Local output for raw downloads
output_dir = "NYU_MRI_Scans"
max_scans = 100

# nnU-Net configuration
task_name = "Dataset500_NYU"
nnunet_raw_data = "nnUNet_raw_data"

# Derived paths
task_folder = os.path.join(nnunet_raw_data, task_name)
images_tr_dir = os.path.join(task_folder, "imagesTr")
labels_tr_dir = os.path.join(task_folder, "labelsTr")
dataset_json_path = os.path.join(task_folder, "dataset.json")

