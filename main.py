"""
main.py

Runs the full Flywheel + nnU-Net pipeline:
1. Download from Flywheel
2. Organize files
3. Resample masks
4. Plan + Train + Predict
5. Visualize output
"""

import flywheel_downloader
import organize_nnunet_data
import resample_utils
import run_nnunet
import visualize_predictions


def main():
    print("\nStarting full pipeline...\n")
    flywheel_downloader.download_from_flywheel()
    organize_nnunet_data.organize_nnunet_folders()
    organize_nnunet_data.create_dataset_json()
    resample_utils.resample_all_segmentations()
    run_nnunet.plan_and_preprocess()
    run_nnunet.train_model()
    run_nnunet.predict_model()
    visualize_predictions.visualize_all()
    print("\nPipeline complete!\n")


if __name__ == "__main__":
    main()

