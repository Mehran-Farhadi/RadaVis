"""Run Radarize Translation ResNet18 inference on a processed NPZ."""

import argparse
from pathlib import Path

import numpy as np
import torch
from torchvision.models import resnet18


def load_model(checkpoint_path, device):
    # Load only trusted Radarize checkpoints.
    checkpoint = torch.load(checkpoint_path, map_location="cpu")

    if checkpoint.get("model_type") != "ResNet18":
        raise ValueError("Expected Radarize ResNet18 checkpoint")

    kwargs = checkpoint["model_kwargs"]
    if kwargs.get("n_channels") != 2 or kwargs.get("n_outputs") != 2:
        raise ValueError(f"Unexpected model configuration: {kwargs}")

    network = resnet18(weights=None)
    network.conv1 = torch.nn.Conv2d(
        2, 64, kernel_size=7, stride=2, padding=3, bias=False
    )
    network.fc = torch.nn.Linear(512, 2)

    prefix = "resnet18."
    state = checkpoint["model_state_dict"]

    if not all(key.startswith(prefix) for key in state):
        raise ValueError("Unexpected checkpoint parameter names")

    state = {
        key[len(prefix):]: value
        for key, value in state.items()
    }

    network.load_state_dict(state, strict=True)
    return network.to(device).eval()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args()

    if args.batch_size <= 0:
        parser.error("--batch-size must be positive")

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    network = load_model(args.checkpoint, device)

    with np.load(args.input) as data:
        time = data["time"].copy()
        radar_d = data["radar_d"].copy()
        radar_de = data["radar_de"].copy()
        gt = data["velo_gt"][:, :2].copy()

    n = len(time)

    if radar_d.shape != (n, 1, 60, 181):
        raise ValueError(f"Unexpected radar_d shape: {radar_d.shape}")

    if radar_de.shape != (n, 1, 60, 181):
        raise ValueError(f"Unexpected radar_de shape: {radar_de.shape}")

    if gt.shape != (n, 2):
        raise ValueError(f"Unexpected ground truth shape: {gt.shape}")

    if not all(np.isfinite(x).all() for x in
               (time, radar_d, radar_de, gt)):
        raise ValueError("Input contains non-finite values")

    predictions = []

    with torch.inference_mode():
        for start in range(0, n, args.batch_size):
            end = min(start + args.batch_size, n)

            x = np.concatenate(
                [radar_d[start:end], radar_de[start:end]],
                axis=1
            )

            x = torch.from_numpy(x).float().to(device)
            y = network(x)
            predictions.append(y.cpu().numpy())

    pred = np.concatenate(predictions, axis=0)

    if not np.isfinite(pred).all():
        raise ValueError("Predictions contain non-finite values")

    error = pred - gt
    mae = np.mean(np.abs(error), axis=0)
    rmse = np.sqrt(np.mean(error ** 2, axis=0))

    args.output.parent.mkdir(parents=True, exist_ok=True)

    np.savez_compressed(
        args.output,
        time=time,
        flow_pred_xs=pred[:, 0],
        flow_pred_ys=pred[:, 1],
        flow_gt_xs=gt[:, 0],
        flow_gt_ys=gt[:, 1],
    )

    print("Device:", device)
    print("Frames:", n)
    print("MAE (vx, vy):", mae)
    print("RMSE (vx, vy):", rmse)
    print("Saved:", args.output)


if __name__ == "__main__":
    main()