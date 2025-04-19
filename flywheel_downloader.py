"""
flywheel_downloader.py

Downloads MRI and segmentation files from Flywheel and stores them locally
using subject ID–based filenames. Uses secure API key loading from environment.
"""

import os
import flywheel
from tqdm import tqdm
import config


def download_from_flywheel():
    """
    Connects to Flywheel and downloads up to `max_scans` pairs of
    RTSTRUCT_MRI and RTSTRUCT_segmentation NIfTI files.
    Files are stored in config.output_dir and skipped if already downloaded.
    """
    fw = flywheel.Client(config.api_key)
    project = fw.lookup(f"{config.flywheel_group}/{config.flywheel_project}")
    os.makedirs(config.output_dir, exist_ok=True)

    file_types = {"RTSTRUCT_MRI.nii.gz", "RTSTRUCT_segmentation.nii.gz"}
    scan_count = 0

    sessions = project.sessions.iter_find()
    for session in tqdm(sessions, desc="Downloading Sessions"):
        if scan_count >= config.max_scans:
            break

        subject = session.subject
        subject_label = subject.label if subject else None
        if not subject_label or not subject_label.isdigit():
            continue

        acquisitions = session.acquisitions.iter_find()
        for acq in acquisitions:
            if scan_count >= config.max_scans:
                break

            for file in acq.files:
                if file.name in file_types:
                    output_path = os.path.join(config.output_dir, f"{subject_label}_{file.name}")
                    if os.path.exists(output_path):
                        continue

                    print(f"Downloading {scan_count + 1}/{config.max_scans}: {subject_label}, {file.name}")
                    file.download(output_path)
                    scan_count += 1

    print(f"\nDownload complete. {scan_count} files saved in '{config.output_dir}'.")


if __name__ == "__main__":
    download_from_flywheel()

