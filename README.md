# Brain Tumor MRI Segmentation with nnU-Net

This project automates the full pipeline for downloading brain MRI scans + tumor segmentations from Flywheel, formatting them for `nnU-Net`, training a model, and visualizing predictions.


*Disclaimer: This project is completely independent of my research position.
_______________________________________________________________________________________________________________________________________________________

Sample Output from compare_predictions.py

This comparison shows an axial slice from a brain MRI scan with the predicted tumor segmentation (right) alongside the annotated ground truth (left). The Dice similarity coefficient quantifies overlap accuracy.

![image alt](https://github.com/Veeru102/NYUMets-mri-tumor-segmentation/blob/main/dice_comparison.png?raw=true)

---

Project Structure

```bash
.
├── config.py                 # All paths and constants
├── flywheel_downloader.py    # Downloads data via Flywheel SDK
├── organize_nnunet_data.py   # Converts to nnU-Net format
├── resample_utils.py         # Resamples segmentations to match MRI headers
├── run_nnunet.py             # CLI wrapper for nnU-Net training + prediction
├── visualize_predictions.py  # Overlays predictions on MRI slices
├── compare_predictions.py    # Creates side-by-side comparison plots w/ Dice scores
├── main.py                   # Full end-to-end pipeline
├── requirements.txt
├── .gitignore

