"""
run_pipeline.py

Main entry point for the full data preparation pipeline:
1. Download data from Flywheel
2. Organize into nnU-Net format
3. Resample segmentations
4. Generate dataset.json
"""

import flywheel_downloader
import organize_nnunet_data
import resample_utils


def main():
    print("\n Starting full data pipeline...\n")
    flywheel_downloader.download_from_flywheel()
    organize_nnunet_data.organize_nnunet_folders()
    organize_nnunet_data.create_dataset_json()
    resample_utils.resample_all_segmentations()
    print("\n Pipeline complete. Data ready for nnU-Net\n")


if __name__ == "__main__":
    main()

