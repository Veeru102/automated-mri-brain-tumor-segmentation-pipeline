"""
organize_nnunet_data.py

Organizes MRI and segmentation files downloaded from Flywheel into the nnU-Net
raw data structure and generates a valid dataset.json metadata file.
"""

import os
import shutil
import glob
import json
import config


def organize_nnunet_folders():
    """
    Copies and renames MRI and segmentation files into the nnU-Net format:
    - MRI → sub-<ID>_0000.nii.gz (imagesTr)
    - Segmentation → sub-<ID>.nii.gz (labelsTr)
    """
    os.makedirs(config.images_tr_dir, exist_ok=True)
    os.makedirs(config.labels_tr_dir, exist_ok=True)

    mri_files = sorted(glob.glob(os.path.join(config.output_dir, "*_RTSTRUCT_MRI.nii.gz")))

    for mri_file in mri_files:
        subject_id = os.path.basename(mri_file).split("_")[0]
        seg_file = mri_file.replace("RTSTRUCT_MRI.nii.gz", "RTSTRUCT_segmentation.nii.gz")

        if not os.path.exists(seg_file):
            print(f"[WARN] No segmentation for subject {subject_id}. Skipping.")
            continue

        # Copy and rename files to nnU-Net format
        shutil.copy(mri_file, os.path.join(config.images_tr_dir, f"sub-{subject_id}_0000.nii.gz"))
        shutil.copy(seg_file, os.path.join(config.labels_tr_dir, f"sub-{subject_id}.nii.gz"))

    print(f"\nData organized into nnU-Net folders:\n  - {config.images_tr_dir}\n  - {config.labels_tr_dir}")


def create_dataset_json():
    """
    Generates a nnU-Net compatible dataset.json file with the list of training samples,
    channel configuration, label map, and basic metadata.
    """
    dataset = {
        "channel_names": {
            "0": "MRI"
        },
        "labels": {
            "background": 0,
            "tumor": 1
        },
        "file_ending": ".nii.gz",
        "dataset_name": config.task_name,
        "description": "NYU Brain MRI + Segmentation Dataset from Flywheel",
        "numTraining": 0,
        "training": [],
        "test": []
    }

    train_image_paths = sorted(glob.glob(os.path.join(config.images_tr_dir, "*_0000.nii.gz")))

    for img_path in train_image_paths:
        subject_id = os.path.basename(img_path).split("_")[0].replace("sub-", "")
        label_path = os.path.join(config.labels_tr_dir, f"sub-{subject_id}.nii.gz")

        if os.path.exists(label_path):
            dataset["training"].append({
                "image": f"./imagesTr/sub-{subject_id}_0000.nii.gz",
                "label": f"./labelsTr/sub-{subject_id}.nii.gz"
            })

    dataset["numTraining"] = len(dataset["training"])

    with open(config.dataset_json_path, "w") as f:
        json.dump(dataset, f, indent=4)

    print(f"dataset.json created at {config.dataset_json_path} ({dataset['numTraining']} training cases)")


if __name__ == "__main__":
    organize_nnunet_folders()
    create_dataset_json()

