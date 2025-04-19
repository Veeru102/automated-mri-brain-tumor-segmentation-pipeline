"""
visualize_predictions.py

Loads predicted segmentation masks and their corresponding MRIs
and displays them slice-by-slice using matplotlib overlays.
"""

import os
import glob
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import config


def show_overlay(mri_data, mask_data, subject_id, slice_idx=None):
    """Displays a single overlay of mask on MRI."""
    if slice_idx is None:
        slice_idx = mri_data.shape[2] // 2  # middle slice

    plt.figure(figsize=(6, 6))
    plt.imshow(mri_data[:, :, slice_idx], cmap='gray')
    plt.imshow(mask_data[:, :, slice_idx], cmap='Reds', alpha=0.5)
    plt.title(f"Overlay for {subject_id} (slice {slice_idx})")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def visualize_all(prediction_dir="predicted_masks", max_cases=5):
    pred_paths = sorted(glob.glob(os.path.join(prediction_dir, "*.nii.gz")))
    shown = 0

    for pred_path in pred_paths:
        subject_id = os.path.basename(pred_path).replace(".nii.gz", "")
        mri_path = os.path.join(config.images_tr_dir, f"{subject_id}_0000.nii.gz")

        if not os.path.exists(mri_path):
            print(f"[Skip] MRI not found for {subject_id}")
            continue

        # Load data
        mri = nib.load(mri_path).get_fdata()
        pred = nib.load(pred_path).get_fdata()

        print(f"Displaying {subject_id}")
        show_overlay(mri, pred, subject_id)

        shown += 1
        if shown >= max_cases:
            break


if __name__ == "__main__":
    visualize_all()

