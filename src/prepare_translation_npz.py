
import ast
from pathlib import Path
from collections import defaultdict, deque

import cv2
import numpy as np
import rosbag
from tqdm import tqdm
from scipy.spatial.transform import Rotation as R

from radarize.utils import dsp, radar_config


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT / "radarize_ae"
BAG = ROOT / "data/raw/bot_beckman_5thfloor_1.bag"
OUTPUT = ROOT / "data/processed/bot_beckman_5thfloor_1.npz"

RADAR_TOPIC = "/radar0/radar_data"
POSE_TOPIC = "/tracking/odom/sample"


# Load the original Radarize functions without importing
# create_dataset.py, which requires Open3D.
source_path = REPO / "tools/create_dataset.py"
source = source_path.read_text()
tree = ast.parse(source)

names = {
    "create_radar_doppler",
    "create_radar_doppler_elevation",
    "create_body_velo_gt",
    "sync2topic",
}

functions = [
    node for node in tree.body
    if isinstance(node, ast.FunctionDef)
    and node.name in names
]

assert {f.name for f in functions} == names

namespace = {
    "np": np,
    "cv2": cv2,
    "dsp": dsp,
    "R": R,
    "tqdm": tqdm,
    "deque": deque,
    "defaultdict": defaultdict,
}

module = ast.Module(body=functions, type_ignores=[])
exec(compile(module, str(source_path), "exec"), namespace)

with open(REPO / "calib/1843/1843_v1.cfg") as f:
    params = radar_config.RadarConfig(f.readlines()).get_params()

with rosbag.Bag(str(BAG), "r") as bag:
    print("Generating radar_d...")
    d_ts, d_maps = namespace["create_radar_doppler"](
        bag, params,
        radar_topic=RADAR_TOPIC,
        resize_shape=(181, 60),
        radar_buffer_len=3,
        range_subsampling_factor=1,
    )

    print("Generating radar_de...")
    de_ts, de_maps = namespace["create_radar_doppler_elevation"](
        bag, params,
        radar_topic=RADAR_TOPIC,
        resize_shape=(181, 60),
        radar_buffer_len=3,
        range_subsampling_factor=1,
    )

    print("Generating ground-truth velocity...")
    v_ts, v_values = namespace["create_body_velo_gt"](
        bag, pose_topic=POSE_TOPIC
    )

    # The original synchronization reference is radar_r_3.
    # Its timestamps correspond to radar frames starting
    # with the third message of a three-frame buffer.
    radar_times = [
        ts.to_sec()
        for _, _, ts in bag.read_messages(topics=[RADAR_TOPIC])
    ]
    reference_ts = np.asarray(radar_times[2:])

    # Original sync2topic uses the first pose_gt timestamp
    # to determine the synchronization starting time.
    pose_times = [
        ts.to_sec()
        for _, _, ts in bag.read_messages(topics=[POSE_TOPIC])
    ]

assert len(reference_ts) == len(d_ts) == len(de_ts)
assert len(pose_times) > 0
assert len(v_ts) > 0

frames = {
    "radar_d": (np.asarray(d_ts), np.asarray(d_maps)),
    "radar_de": (np.asarray(de_ts), np.asarray(de_maps)),
    "velo_gt": (np.asarray(v_ts), np.asarray(v_values)),
    "radar_r_3": (reference_ts, np.zeros(len(reference_ts))),
    "pose_gt": (
        np.asarray(pose_times),
        np.zeros(len(pose_times)),
    ),
}

print("Synchronizing with radar_r_3...")
synced = namespace["sync2topic"](frames, "radar_r_3")

result = {
    key: synced[key]
    for key in ("time", "radar_d", "radar_de", "velo_gt")
}

n = len(result["time"])
assert n > 0
assert result["radar_d"].shape == (n, 1, 60, 181)
assert result["radar_de"].shape == (n, 1, 60, 181)
assert result["velo_gt"].shape == (n, 3)
assert all(np.isfinite(value).all() for value in result.values())

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
np.savez_compressed(OUTPUT, **result)

print("\nSaved:", OUTPUT)
for name, value in result.items():
    print(name, value.shape, value.dtype)