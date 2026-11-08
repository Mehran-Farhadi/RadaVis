# RadaVis

### Visualizing and Explaining Radar-Based Velocity Estimation

**Course:** AI and Visualization — JKU, Winter Semester 2026
**University:** Johannes Kepler University Linz (JKU)
**Project:** RadaVis
**Selected Model:** Radarize Translation ResNet18
**Repository:** https://github.com/Mehran-Farhadi/RadaVis

RadaVis is a group project that investigates the behavior and explainability of a radar-based deep learning model.

We study **when the model predicts velocity accurately, when it makes errors, and which properties of the radar inputs may help explain its behavior**.

The project combines black-box model analysis, interactive visualization, and Explainable AI (XAI).

---

## 1. Project Overview

### 1.1 Background

RadaVis is based on **Radarize: Enhancing Radar SLAM with Generalizable Doppler-Based Odometry**, presented at MobiSys 2024.

Radarize is a radar-based simultaneous localization and mapping (SLAM) system that estimates motion and supports indoor mapping using millimeter-wave (mmWave) radar.

The original Radarize system includes three main learning components:

| Component | Architecture | Input | Output |
|---|---|---|---|
| Translation | ResNet18 | Doppler-Azimuth heatmaps | 2D velocity |
| Rotation | ResNet18 | Range-Azimuth heatmaps | Relative rotation |
| Mapping | U-Net | Range-Azimuth heatmaps | Segmentation / occupancy |

### 1.2 Selected Model

We focus on the **Translation ResNet18** network.

The actual pretrained model configuration was verified from the Radarize source code and checkpoint metadata.

| Property | Configuration |
|---|---|
| Model | Translation ResNet18 |
| Model name | `transnet18` |
| Framework | PyTorch |
| Input channels | 2 |
| Input tensor | `(B, 2, 60, 181)` |
| Output | `(vx, vy)` |
| Output units | m/s |
| Task | Two-dimensional velocity regression |

The two input channels are:

- `radar_d`: Doppler-Azimuth heatmap.
- `radar_de`: Doppler-Azimuth heatmap with elevation beamforming.

The model predicts two velocity components from these image-like radar representations.

We selected this network because its inputs can be visualized as heatmaps, while its numerical outputs allow detailed error analysis.

### 1.3 Research Question

**Under what conditions does Radarize accurately or inaccurately estimate velocity, and what has the network learned that may explain this behavior?**

---

## 2. Research Objectives and Project Phases

The project is divided into two phases.

### 2.1 Phase I — How Does the Model Behave?

Phase I investigates the network as a **black box**.

We analyze input-output behavior without using internal activations or model explanations.

The objectives are to:

1. Compare predicted velocity with reference velocity.
2. Measure forward, lateral, and two-dimensional prediction errors.
3. Identify difficult motion conditions and unusual error patterns.
4. Investigate systematic relationships between errors and motion characteristics.
5. Compare representative accurate and inaccurate predictions.
6. Evaluate whether findings remain consistent across additional held-out sequences and platform types.

The emphasis is on understanding model behavior through visualization, rather than reporting only aggregate accuracy metrics.

**Current progress:** Two interactive visualizations have been implemented and independently checked using one held-out robot sequence.

### 2.2 Phase II — What Did the Model Learn?

Phase II will examine the network's internal representations to investigate possible explanations for the behaviors observed in Phase I.

Candidate techniques include:

- **Saliency-based visualization:** Investigating which regions of the Doppler-Azimuth heatmaps influence velocity predictions.
- **Intermediate feature visualization:** Extracting neural features and examining their structure using dimensionality-reduction techniques such as PCA or UMAP.

Each pair must investigate at least two explanation techniques and compare their findings.

The selected XAI methods should address concrete questions arising from the Phase I analysis.

**Current status:** Phase II investigations are planned; the XAI results are not yet available.

---

## 3. Team Workflow and AI Assistance

The project is conducted by four students working in two pairs.

### 3.1 AI-aided Pair

The AI-aided pair uses Claude to support selected activities, including:

- Technical investigation.
- Visualization design.
- Code generation and improvement.
- Interpretation of visual patterns.
- Exploration of alternative analytical approaches.

Significant AI interactions are documented, including the prompts, AI suggestions, human decisions, verification procedures, limitations, and reflections.

**AI interaction log:**

`reports/phase1/ai_logs/AI_Interaction_Log.md`

AI-generated results are not accepted automatically. We verify relevant outputs against source code, actual prediction files, and independently executed calculations.

### 3.2 Human-only Pair

The Human-only pair investigates the same model and task without Generative AI assistance, following the course rules.

The pair develops its own analysis independently of the AI-aided workflow.

**Human-only Phase I notebook:**

`notebooks/phase1/human_only/RadaVis_Phase1_Human_Only.ipynb`

The Human-only notebook is included in the shared repository. Its detailed scientific results are maintained independently and will be compared with the AI-aided approach during the group review.

### 3.3 Comparison Between Pairs

At the end of each phase, the group compares:

- Analytical methods and visualization designs.
- Observed model behaviors.
- Strengths and limitations of each approach.
- The role of AI assistance in the research process.
- Scientific validity and reproducibility.

---

## 4. Repository Structure

The relevant project structure is:

```text
RadaVis/
├── README.md
├── .gitignore
├── team-info.json
├── workload.json
│
├── src/
│   ├── prepare_translation_npz.py
│   └── run_translation_inference.py
│
├── notebooks/
│   ├── phase1/
│   │   ├── 01_velocity_timeseries.ipynb
│   │   ├── 01_velocity_timeseries_executed.ipynb
│   │   ├── 02_error_vs_speed.ipynb
│   │   ├── 02_error_vs_speed_executed.ipynb
│   │   └── human_only/
│   │       └── RadaVis_Phase1_Human_Only.ipynb
│   └── phase2/
│
├── reports/
│   └── phase1/
│       └── ai_logs/
│           └── AI_Interaction_Log.md
│
├── results/
│   └── phase1/
│       └── main_0/
│           ├── bot_beckman_5thfloor_1_timeseries.html
│           └── bot_beckman_5thfloor_1_error_vs_speed.html
│
├── data/
│   ├── raw/              # Local data, not committed
│   └── processed/        # Local data, not committed
│
├── models/               # Local checkpoints, not committed
│
└── radarize_ae/          # Original Radarize repository,
                          # cloned separately and ignored by Git
```

Some directories contain only placeholder files until later project phases.

The repository includes our analysis code, visualization notebooks, lightweight HTML results, and documentation.

**Large ROS bags, model checkpoints, and processed datasets are not stored in GitHub.**

They must be obtained separately from the official Radarize resources.

---

## 5. Visualization Environment — Windows

The visualization notebooks have been executed successfully on Windows using Python 3.11.

The tested environment is called:

`RadaVisViz311`

### 5.1 Clone the Repository

Open PowerShell or a terminal:

```bash
git clone https://github.com/Mehran-Farhadi/RadaVis.git
cd RadaVis
```

### 5.2 Create the Conda Environment

```bash
conda create -n RadaVisViz311 python=3.11 -y
conda activate RadaVisViz311
```

This creates an environment for visualization without modifying the existing system Python installation.

### 5.3 Install Visualization Dependencies

```bash
python -m pip install "numpy==1.26.4" "pandas==2.2.3" "altair==6.0.0" "matplotlib==3.10.7" "vl-convert-python==1.9.0.post1" matplotlib ipykernel jupyterlab nbconvert nbclient nbformat
```

These libraries provide numerical processing, data analysis, interactive visualization, and Jupyter execution.

### 5.4 Verify the Environment

```bash
python -c "import numpy, pandas, matplotlib, altair, ipykernel; print('RadaVis environment ready!')"
```

Expected output:

```text
RadaVis environment ready!
```

### 5.5 Configure VS Code

1. Open the RadaVis project folder in Visual Studio Code.
2. Install the Microsoft Python and Jupyter extensions.
3. Open a notebook from `notebooks/phase1/`.
4. Select the `RadaVisViz311` Python environment as the Jupyter kernel.
5. Run the notebook.

If the environment does not appear in the kernel list, register it:

```bash
python -m ipykernel install --user --name radavisviz311 --display-name "RadaVis Visualization (Python 3.11)"
```

Then select the registered kernel in VS Code.

### 5.6 Separation of Environments

The Windows environment is intended for visualization and analysis.

It does not need the complete Radarize SLAM software stack.

The heavier radar preprocessing and model inference tasks are performed separately on the NVIDIA Jetson device.

---

## 6. Dataset and Pretrained Model

### 6.1 Official Resources

The original Radarize dataset and evaluation archives are available from:

https://zenodo.org/records/11093859

| Archive | Approximate Size | Contents |
|---|---:|---|
| `dataset.zip` | 84.2 GB | Original radar dataset |
| `eval.zip` | 1.3 GB | Evaluation artifacts and pretrained models |

It is not necessary for every team member to download the complete dataset.

### 6.2 Selected Experimental Sequence

We selected:

`bot_beckman_5thfloor_1`

The sequence comes from the robot platform and belongs to the selected `main_0` test split.

Only the required ROS bag was downloaded from the large dataset archive using a selective-download approach.

The extracted ROS bag is approximately 630.8 MB.

We verified that it was readable and contained the required radar and odometry topics:

- `/radar0/radar_data`
- `/tracking/odom/sample`

### 6.3 Selected Checkpoint

The pretrained Translation checkpoint was obtained from the official evaluation archive.

Its location inside the evaluation artifacts is:

`output_main_0/transnet18/transnet18.pth`

For local execution, it is stored as:

`models/main_0/transnet18.pth`

The checkpoint contains the ResNet18 model configuration and trained weights used for our evaluation.

### 6.4 Local Data Locations

On the Jetson, the pipeline uses the following structure:

```text
RadaVis/
├── data/
│   ├── raw/
│   │   └── bot_beckman_5thfloor_1.bag
│   └── processed/
│       └── bot_beckman_5thfloor_1.npz
├── models/
│   └── main_0/
│       └── transnet18.pth
└── results/
    └── phase1/
        └── main_0/
            └── bot_beckman_5thfloor_1_predictions.npz
```

The processed NPZ and prediction NPZ files are generated or transferred locally; they are not committed to GitHub.

---

## 7. Radarize Preprocessing and Model Inference

### 7.1 Tested Jetson Environment

The preprocessing and inference pipeline was tested using an NVIDIA Jetson AGX Orin.

| Component | Tested Configuration |
|---|---|
| Operating system | Ubuntu 20.04 LTS |
| Architecture | ARM64 / aarch64 |
| Python | 3.8.10 |
| PyTorch | NVIDIA Jetson build, 2.1.0a0 |
| Torchvision | 0.16.0 |
| CUDA | Available |
| Model execution | GPU |

A separate virtual environment named `radavis_preprocess` was used for radar preprocessing.

The tested preprocessing dependencies included NumPy 1.23.5, Numba 0.56.4, SciPy 1.10.1, OpenCV 4.8.1, `rosbag-standalone` 1.17.4.1, and tqdm 4.66.5.

The Jetson-specific PyTorch installation must be compatible with its NVIDIA software environment. It should not be replaced with an arbitrary desktop PyTorch package.

### 7.2 Obtain the Original Radarize Code

The original source code is required for radar preprocessing.

From the RadaVis project directory:

```bash
git clone https://github.com/ConnectedSystemsLab/radarize_ae.git
```

This creates the local `radarize_ae/` directory.

The original repository is not included inside our Git history.

### 7.3 Preprocess the ROS Bag

The preprocessing script is:

`src/prepare_translation_npz.py`

It uses selected original Radarize processing functions and the radar calibration files.

The current script is specifically configured for `bot_beckman_5thfloor_1`.

From the Jetson terminal:

```bash
source ~/venvs/radavis_preprocess/bin/activate
unset PYTHONPATH

cd ~/RadaVis/radarize_ae
PYTHONPATH="$PWD" python ../src/prepare_translation_npz.py
```

The script creates:

`data/processed/bot_beckman_5thfloor_1.npz`

Its arrays have the following shapes:

| Array | Shape | Description |
|---|---|---|
| `time` | `(1798,)` | Frame timestamps |
| `radar_d` | `(1798, 1, 60, 181)` | Doppler-Azimuth inputs |
| `radar_de` | `(1798, 1, 60, 181)` | Elevation-beamformed Doppler inputs |
| `velo_gt` | `(1798, 3)` | Reference body velocity |

**Important:** The current preprocessing script writes to a fixed output path. Running it again may replace the existing processed NPZ file. Back up an existing output before repeating the preprocessing step.

The model uses the first two velocity components from `velo_gt`.

### 7.4 Run Translation Inference

The inference script is:

`src/run_translation_inference.py`

It loads the pretrained ResNet18 checkpoint, combines the two radar channels, and predicts forward and lateral velocity.

Inference does not require the complete ROS/Cartographer SLAM pipeline once the processed NPZ is available.

From the RadaVis project root on Jetson, using the Python environment with working PyTorch:

```bash
cd ~/RadaVis

python3 src/run_translation_inference.py \
  --input data/processed/bot_beckman_5thfloor_1.npz \
  --checkpoint models/main_0/transnet18.pth \
  --output results/phase1/main_0/bot_beckman_5thfloor_1_predictions_reproduced.npz
```

The script automatically selects CUDA when available, otherwise CPU.

The example output name uses `_reproduced` to avoid overwriting the original predictions.

### 7.5 Prediction Output Format

The inference script saves five arrays:

| Array | Shape | Description |
|---|---|---|
| `time` | `(1798,)` | Frame timestamps |
| `flow_pred_xs` | `(1798,)` | Predicted forward velocity |
| `flow_pred_ys` | `(1798,)` | Predicted lateral velocity |
| `flow_gt_xs` | `(1798,)` | Reference forward velocity |
| `flow_gt_ys` | `(1798,)` | Reference lateral velocity |

The visualization notebooks expect the original analysis file at:

`results/phase1/main_0/bot_beckman_5thfloor_1_predictions.npz`

A reproduced prediction file can be used for the same analysis after placing it at the expected location or updating the notebook's input path.

---

## 8. Phase I — Experimental Results and Visualizations

### 8.1 Experiment Setup

We evaluated the pretrained Translation ResNet18 model on one held-out robot sequence.

| Property | Value |
|---|---|
| Sequence | `bot_beckman_5thfloor_1` |
| Platform | Robot |
| Checkpoint | `main_0` |
| Number of evaluated frames | 1,798 |
| Duration | Approximately 59.9 seconds |
| Model input | Two 60 × 181 radar heatmaps |
| Model output | `vx`, `vy` |
| Inference device | Jetson GPU |

### 8.2 Prediction Accuracy

The measured component-wise prediction errors were:

| Metric | vx (m/s) | vy (m/s) |
|---|---:|---:|
| MAE | 0.04838 | 0.02498 |
| RMSE | 0.06666 | 0.03462 |

These are results for this sequence and checkpoint only.

They should not be interpreted as overall model performance across the complete Radarize dataset.

### 8.3 Visualization 1 — Velocity Time Series

**Notebook:**

`notebooks/phase1/01_velocity_timeseries.ipynb`

**HTML output:**

`results/phase1/main_0/bot_beckman_5thfloor_1_timeseries.html`

The first visualization compares predicted and reference velocities over time.

It includes:

- An overview of velocity-error magnitude.
- Predicted and reference `vx`.
- Signed forward error.
- Predicted and reference `vy`.
- Signed lateral error.
- Interactive zooming, hovering, and frame selection.

**Main observations:**

- Repeated stop-and-start motion is visible.
- Predictions generally follow major forward-velocity changes.
- The predicted forward velocity appears smoother than the reference during some cruising intervals.
- A large prediction/reference disagreement appears near frames 546–559.
- Forward and lateral prediction errors have different characteristics.

The suspected reference-data anomaly at frames 546–559 has not been confirmed.

### 8.4 Visualization 2 — Error vs. Speed

**Notebook:**

`notebooks/phase1/02_error_vs_speed.ipynb`

**HTML output:**

`results/phase1/main_0/bot_beckman_5thfloor_1_error_vs_speed.html`

The second visualization investigates whether velocity-estimation errors depend on motion speed.

It displays:

- Signed forward error.
- Signed lateral error.
- Two-dimensional error magnitude.
- Binned summaries using 0.05 m/s speed ranges.
- Median, mean, and error-spread estimates.
- All-frame results compared with results excluding frames 546–559.
- Speed-bin selection linked to a time strip.
- Alternative speed-axis definitions.

The signed prediction errors are:

`e_x = predicted vx − reference vx`

`e_y = predicted vy − reference vy`

The 2D error magnitude is:

`|e| = sqrt(e_x² + e_y²)`

**Main findings:**

The median forward error changes from positive at some lower reference speeds to negative at higher reference speeds.

For example:

| Reference Speed (m/s) | Median Forward Error (m/s) |
|---|---:|
| 0.15–0.20 | +0.0746 |
| 0.20–0.25 | +0.0236 |
| 0.25–0.30 | −0.0217 |
| 0.30–0.35 | −0.0685 |
| 0.35–0.40 | −0.1204 |

This suggests a speed-dependent pattern in this sequence.

However, it does not establish whether the cause lies in the network, reference-signal characteristics, or motion distribution.

### 8.5 Sensitivity Analysis — Frames 546–559

Frames 546–559 were identified as suspicious during the time-series analysis because the reference velocity remained constant during a period of large disagreement.

Rather than modifying the reference data, we performed a sensitivity analysis.

| Condition | Number of Frames |
|---|---:|
| All frames | 1,798 |
| Excluding frames 546–559 | 1,784 |

Under the default reference-speed binning, the excluded frames all belong to the 0.15–0.20 m/s range.

Removing them changes the statistics of that speed bin but does not eliminate the broader observed forward-error pattern.

The exclusion is an analytical comparison, **not a claim that the 14 reference measurements are incorrect**.

### 8.6 Visualization 3 — Radar Input and Error Explorer

**Notebook:**

`notebooks/phase1/03_radar_error_explorer.ipynb`

**Interactive HTML:**

`results/phase1/main_0/bot_beckman_5thfloor_1_radar_error_explorer.html`

**Static figure:**

`results/phase1/main_0/bot_beckman_5thfloor_1_radar_comparison.png`

The third visualization investigates the radar inputs associated with accurate and inaccurate velocity predictions.

It compares five low-error/high-error frame pairs selected within narrow reference-speed intervals.

Features include:

- Interactive selection of five frame pairs.
- Side-by-side visualization of `radar_d` and `radar_de`.
- Fixed 0–1 color scales for comparison within each radar channel.
- Ground-truth and predicted velocity values.
- Two-dimensional prediction errors.
- Overview plots comparing error, speed, and lateral velocity.
- Doppler and azimuth intensity profiles.

Pair 3 compares frames 656 and 1050, which have similar reference speeds (approximately 0.225 and 0.228 m/s) but substantially different prediction errors (approximately 0.003 and 0.076 m/s).

The selected frames are exploratory examples, not a statistically representative sample. Visible input differences cannot establish what caused the model's prediction errors.

The notebook was executed successfully on Windows using Python 3.11.18.

For self-contained HTML export, the notebook requires:

`vl-convert-python==1.9.0.post1`

It was tested with Matplotlib 3.10.7.

The HTML was inspected in Chrome, and pair selection was manually verified by the team.

### 8.7 Running the Visualization Notebooks

First activate the tested Windows environment:

```bash
conda activate RadaVisViz311
```

Ensure that the prediction NPZ exists at the expected path:

`results/phase1/main_0/bot_beckman_5thfloor_1_predictions.npz`

From the repository root, run the first notebook:

```bash
python -m jupyter nbconvert --to notebook --execute "notebooks/phase1/01_velocity_timeseries.ipynb" --output "01_velocity_timeseries_executed.ipynb" --ExecutePreprocessor.timeout=300
```

Run the second notebook:

```bash
python -m jupyter nbconvert --to notebook --execute "notebooks/phase1/02_error_vs_speed.ipynb" --output "02_error_vs_speed_executed.ipynb" --ExecutePreprocessor.timeout=300
```

The executed notebooks are written in the `notebooks/phase1/` directory.

The visualization code saves HTML outputs under:

`results/phase1/main_0/`

Both notebooks have also been executed successfully using the Python 3.11 environment on Windows.

**HTML note:** The currently generated Altair visualizations may load Vega-related JavaScript libraries from a CDN. Internet access may therefore be required when opening them. A fully self-contained offline version is not yet part of the verified deliverables.

---

## 9. Verification, Limitations, and Next Steps

### 9.1 Independent Technical Verification

We reproduced the preprocessing and inference pipeline on the Jetson.

**Preprocessing verification**

The original and reproduced NPZ files were compared.

All four arrays matched exactly:

- `time`
- `radar_d`
- `radar_de`
- `velo_gt`

For every array:

`np.array_equal = True`

Maximum difference:

`0`

**Inference verification**

The original and reproduced inference outputs were compared across all five saved arrays.

All arrays passed `np.allclose`, and the maximum differences displayed to ten decimal places were zero.

The reproduced MAE and RMSE values matched the previous evaluation results.

### 9.2 Independent Visualization Verification

The team independently executed the visualization notebooks and checked the numerical calculations used for the Error vs. Speed analysis.

Verification included:

- Frame counts.
- Finite prediction and reference values.
- Forward and lateral error formulas.
- Two-dimensional error magnitude.
- Speed-bin counts.
- Exclusion of frames 546–559.
- Median and mean error calculations.

The HTML charts were visually inspected in Chrome.

The interactive controls are present in the generated implementation. A complete manual browser-interaction test of every control has not yet been documented.

### 9.3 Current Limitations

The current experimental findings have several limitations:

1. Only one held-out robot sequence has been analyzed.
2. Only the `main_0` Translation checkpoint has been evaluated in this investigation.
3. The suspected reference-data anomaly remains unresolved.
4. Some speed bins contain relatively few samples.
5. The observed relationship between reference speed and prediction error is descriptive, not causal.
6. Performance across other platforms and environments remains to be investigated.

The exact reproducibility checks establish repeatability for the tested data, checkpoint, and environment. They do not establish generalization to new recordings.

### 9.4 Planned Investigations

Our next priorities are:

1. Investigate suspicious reference velocities using the available odometry and other motion measurements.
2. Evaluate additional held-out sequences.
3. Compare the model's behavior across available platform types.
4. Examine representative high-error and low-error radar heatmaps.
5. Use Phase I findings to guide the selection of Phase II XAI techniques.
6. Compare the independent AI-aided and Human-only results.

---

## 10. Submission and Project Documentation

### 10.1 Midpoint Submission — Phase I

The midpoint submission includes:

- Phase I code and analysis from both pairs.
- The AI interaction log from the AI-aided pair.
- A recorded progress presentation of up to five minutes.

The presentation should introduce the model and research question, summarize the work of both pairs, demonstrate important visualizations, reflect on AI assistance, and explain the planned Phase II direction.

### 10.2 Final Submission

The final submission includes:

- Completed code and analysis.
- AI interaction records covering both phases.
- Presentation slides.
- A recorded presentation of up to ten minutes.

The final work should connect the model behaviors investigated in Phase I to the explainability findings obtained in Phase II.

### 10.3 AI Interaction Documentation

Significant Claude interactions, accepted and rejected suggestions, independent checks, technical problems, and reflections are recorded in:

`reports/phase1/ai_logs/AI_Interaction_Log.md`

This documentation distinguishes AI-generated suggestions from human verification and final research decisions.

---

## 11. References and Acknowledgments

### 11.1 Original Research

**Radarize: Enhancing Radar SLAM with Generalizable Doppler-Based Odometry**

Emerson Sie, Xinyu Wu, Heyu Guo, and Deepak Vasisht. MobiSys 2024.

- [Radarize Research Paper](https://arxiv.org/abs/2311.11260)
- [Original Radarize GitHub Repository](https://github.com/ConnectedSystemsLab/radarize_ae)
- [Official Dataset and Evaluation Files](https://zenodo.org/records/11093859)

### 11.2 RadaVis Repository

[RadaVis — Group GitHub Repository](https://github.com/Mehran-Farhadi/RadaVis)

The original Radarize architecture, data, and pretrained checkpoints belong to their respective authors.

Our project focuses on model-behavior analysis, reproducible evaluation, interactive visualization, explainability, and comparison of AI-assisted and Human-only workflows.
