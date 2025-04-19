"""
resample_utils.py

Resamples segmentation masks to match the reference MRI scan's spatial metadata
using SimpleITK. This ensures compatibility with nnU-Net and avoids alignment errors.
"""

import os
import glob
import numpy as np
import SimpleITK as sitk
import config


def resample_seg_to_image(seg_path, ref_image_path, output_path):
    """
    Resamples a segmentation mask to match the header of a reference image.

    Parameters:
    - seg_path: path to the original segmentation
    - ref_image_path: path to the reference MRI image
    - output_path: path to save the resampled segmentation
    """
    ref_img = sitk.ReadImage(ref_image_path)
    seg_img = sitk.ReadImage(seg_path)

    # Create resample filter
    resample = sitk.ResampleImageFilter()
    resample.SetReferenceImage(ref_img)
    resample.SetInterpolator(sitk.sitkNearestNeighbor)

    # Perform resampling and hard-set header
    resampled_seg = resample.Execute(seg_img)
    resampled_seg.CopyInformation(ref_img)

    sitk.WriteImage(resampled_seg, output_path)


def directions_match(dir1, dir2, tol=1e-7):
    """Returns True if image directions match within tolerance."""
    return np.allclose(np.array(dir1), np.array(dir2), rtol=0, atol=tol)


def origins_match(org1, org2, tol=1e-4):
    """Returns True if image origins match within tolerance."""
    return np.allclose(np.array(org1), np.array(org2), rtol=0, atol=tol)


def resample_all_segmentations():
    """
    Loops through all subject segmentation files and resamples them
    to match the corresponding MRI images. Also verifies alignment post-resampling.
    """
    image_paths = sorted(glob.glob(os.path.join(config.images_tr_dir, "*_0000.nii.gz")))
    issues_found = []
    total_checked = 0

    print("Resampling segmentation masks to match MRI headers...\n")

    for img_path in image_paths:
        subject_id = os.path.basename(img_path).replace("_0000.nii.gz", "")
        seg_path = os.path.join(config.labels_tr_dir, f"{subject_id}.nii.gz")

        if not os.path.exists(seg_path):
            continue

        # Perform resampling in-place
        resample_seg_to_image(seg_path, img_path, seg_path)

        # Integrity check
        total_checked += 1
        img = sitk.ReadImage(img_path)
        seg = sitk.ReadImage(seg_path)

        spacing_mismatch = (img.GetSpacing() != seg.GetSpacing())
        origin_mismatch = not origins_match(img.GetOrigin(), seg.GetOrigin())
        direction_mismatch = not directions_match(img.GetDirection(), seg.GetDirection())

        if spacing_mismatch or origin_mismatch or direction_mismatch:
            issues_found.append(subject_id)
            print(f"[MISMATCH:] {subject_id}")

    print(f"\n Resampling complete. {total_checked} pairs processed.")
    if issues_found:
        print(f"{len(issues_found)} mismatches still found:")
        for sid in issues_found:
            print(f"  - {sid}")
    else:
        print("All segmentations match their MRI headers")


if __name__ == "__main__":
    resample_all_segmentations()

