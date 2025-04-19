"""
run_nnunet.py

Handles the final nnU-Net CLI pipeline:
1. Planning & Preprocessing
2. Training
3. Prediction
"""

import argparse
import os
import subprocess
import config


def run_command(cmd):
    print(f "Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")


def plan_and_preprocess():
    run_command(f"nnUNetv2_plan_and_preprocess -d 500 --verify_dataset_integrity -c 3d_fullres")


def train_model():
    run_command(f"nnUNetv2_train {config.task_name} 3d_fullres all")


def predict_model(output_dir="predicted_masks"):
    os.makedirs(output_dir, exist_ok=True)
    run_command(
        f"nnUNetv2_predict -i {config.images_tr_dir} "
        f"-o {output_dir} -d 500 -c 3d_fullres -f all"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--step", choices=["preprocess", "train", "predict", "all"], default="all")
    args = parser.parse_args()

    if args.step in ("preprocess", "all"):
        plan_and_preprocess()
    if args.step in ("train", "all"):
        train_model()
    if args.step in ("predict", "all"):
        predict_model()
