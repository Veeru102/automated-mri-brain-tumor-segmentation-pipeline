"""
compare_predictions.py

Generates side-by-side visualizations of MRI scans with:
- Ground truth mask (green)
- Predicted segmentation mask (red)

Displays the Dice score on each image and saves the output for the
top 10 scans with the highest predicted tumor volume.
"""

import os
import glob
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import config

# Output directory for saved visualizations
output_dir = "outputs/comparisons"
os.makedirs(output_dir, exist_ok=True)


def compute_pred_volume(pred_mask):
    """Returns the number of voxels in the predicted segmentation."""
    return np.count_nonzero(pred_mask)


def compute_dice(pred, gt):
    """Computes Dice Similarity Coefficient (DSC) between two masks."""
    pred_bin = (pred > 0).astype(np.uint8)
    gt_bin = (gt > 0).astype(np.uint8)

    intersection = np.sum(pred_bin * gt_bin)
    denom = np.sum(pred_bin) + np.sum(gt_bin)

    if denom == 0:
        return 1.0 if intersection == 0 else 0.0

    return (2.0 * intersection) / denom


def get_top_n_predictions(n=10):
    """Returns the top N prediction file paths with the largest predicted volumes."""
    pred_paths = sorted(glob.glob("predicted_masks/*.nii.gz"))
    volume_list = []

    for path in pred_paths:
        try:
            mask

