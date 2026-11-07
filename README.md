# RadaVis

### Visualizing and Explaining Radar-Based Velocity Estimation

**JKU — AI and Visualization | Winter Semester 2026**

RadaVis is a group project for the AI and Visualization course at Johannes Kepler University Linz (JKU).

Our goal is to investigate the behavior of a deep learning model from **Radarize**, a radar-based simultaneous localization and mapping (SLAM) system.

We focus on understanding when the model predicts velocity accurately, when it makes errors, and what it has learned from radar signals.

## 1. Project Overview

Radarize is a radar-based SLAM system that estimates motion and maps indoor environments using millimeter-wave (mmWave) radar.

Original research paper:

**Radarize: Enhancing Radar SLAM with Generalizable Doppler-Based Odometry**

Authors: Emerson Sie, Xinyu Wu, Heyu Guo, and Deepak Vasisht (MobiSys 2024).

- [Original Radarize GitHub Repository](https://github.com/ConnectedSystemsLab/radarize_ae)
- [Research Paper](https://arxiv.org/abs/2311.11260)
- [Original Dataset and Evaluation Files](https://zenodo.org/records/11093859)

Radarize includes three main learning models:

| Component | Model | Input | Output |
|---|---|---|---|
| Translation | ResNet18 | Doppler-Azimuth Heatmap | 2D velocity |
| Rotation | ResNet18 | Two Range-Azimuth Heatmaps | Relative rotation |
| Mapping | UNet | Range-Azimuth Heatmaps | Segmentation / occupancy |

### Our Selected Model

We focus on the **Translation Model (ResNet18)**.

- **Input:** Two Doppler-Azimuth heatmaps (`radar_d` and `radar_de`), combined into a tensor of shape `(B, 2, 60, 181)`.
- **Output:** Two-dimensional velocity (`vx`, `vy`) in m/s.
- **Task:** Radar-based velocity estimation
- **Framework:** PyTorch

We selected this model because it has image-like inputs and numerical outputs, making it suitable for behavioral visualization and Explainable AI (XAI).

### Main Research Question

**Under what conditions does Radarize accurately or inaccurately predict velocity, and what has the neural network learned that may explain this behavior?**

## 2. Project Objectives

The project consists of two phases.

### Phase I — How Does the Model Behave?

In Phase I, we treat the model as a **black box**.

We investigate its inputs and outputs without examining its internal layers or weights.

Our goals are to:

- Compare predicted velocity with reference velocity.
- Calculate and visualize prediction errors.
- Identify systematic error patterns across a sufficiently large dataset.
- Investigate model behavior under different motion conditions.
- Compare results across available platform types, such as handheld, cart, and robot.
- Examine whether particular input characteristics are associated with larger errors.

Possible visualizations include:

- Ground Truth vs. Predicted Velocity
- Velocity Error Distributions
- Error by Platform Type
- Comparison of Low-Error and High-Error Samples
- Interactive Filtering and Exploration

**Important:** Phase I is not just a performance benchmark. We must discover and investigate meaningful patterns that cannot be explained by aggregate metrics alone.

### Phase II — What Did the Model Learn?

In Phase II, we investigate the model's internal representations and learned features.

The goal is to understand the behaviors discovered in Phase I by examining how the model processes Doppler-Azimuth Heatmaps.

Possible techniques include:

**1. Saliency Maps**

Visualize which regions of the input heatmap influence the model's velocity predictions.

**2. Feature Visualization with PCA or UMAP**

Extract intermediate features from ResNet18 and project them into a lower-dimensional space.

Possible investigations:

- Compare internal representations of accurate and inaccurate predictions.
- Investigate whether high-error samples form identifiable groups.
- Examine how learned features differ across motion conditions.
- Compare explanations across multiple samples to identify consistent patterns.

Each pair must use **at least two explanation techniques** and compare or combine their findings.

The analyses should connect directly to behaviors discovered in Phase I.


### AI-aided Pair

Uses Generative AI tools such as ChatGPT to support analysis, visualization design, coding, and interpretation.

This pair must document:

- Important prompts
- AI-generated suggestions
- Which suggestions were accepted, modified, or rejected
- How AI influenced analytical decisions
- Errors, limitations, and lessons learned

### Human-only Pair

Conducts the analysis without Generative AI assistance.

Limited AI-based code completion and documentation lookup are allowed under the course instructions.

Both pairs must investigate the same model and task, but should develop their analyses independently after agreeing on a shared research direction.

At the end of each phase, the pairs compare their processes, visualizations, results, and the advantages and limitations of AI assistance.

## 4. Development Tools

We use **Visual Studio Code (VS Code)** as the main development environment.

Jupyter Notebooks can be executed directly inside VS Code, so using JupyterLab in a browser is optional.

### Required Tools for Team Members

- Git
- Miniconda or Anaconda
- Visual Studio Code
- VS Code Python extension (Microsoft)
- VS Code Jupyter extension (Microsoft)
- Python 3.9 in a separate Conda environment
- NumPy
- Pandas
- Matplotlib
- JupyterLab
- ipykernel

### Not Required on Personal Laptops Yet

Please do not install the following heavy dependencies unless we decide they are necessary:

- ROS
- CUDA Toolkit
- Cartographer
- Full Radarize PyTorch environment
- Large Radarize Dataset
- Open3D

These dependencies may be needed later for model execution and advanced analysis.

We use an NVIDIA Jetson AGX Orin running Ubuntu 20.04 for Radarize preprocessing and model inference. The Translation ResNet18 checkpoint has been successfully evaluated using PyTorch with CUDA. Visualization notebooks are executed separately on Windows.

## 5. Installation Guide

### Step 1 — Clone the RadaVis Group Repository

Open PowerShell or a terminal:

```bash
git clone https://github.com/Mehran-Farhadi/RadaVis.git
cd RadaVis
```

This downloads our group project files.

### Step 2 — Create the Conda Environment

Run:

```bash
conda create -n RadaVisViz311 python=3.11 -y
conda activate RadaVisViz311

python -m pip install "numpy==1.26.4" "pandas==2.2.3" "altair==6.0.0" ipykernel jupyterlab nbconvert nbclient nbformat
```

This creates a dedicated Python environment without modifying your existing base environment.

### Step 3 — Install Visualization Libraries

Run:

```bash
python -m pip install "numpy==1.26.4" "pandas==2.2.3" "altair==6.0.0" matplotlib ipykernel jupyterlab nbconvert nbclient nbformat
```

These packages support numerical analysis, visualization, and Jupyter Notebooks.

### Step 4 — Verify Installation

```bash
python -c "import numpy, pandas, matplotlib, altair, ipykernel; print('RadaVis environment ready!')"
```

Expected output:

```text
RadaVis environment ready!
```

### Step 5 — Configure VS Code

1. Open VS Code.
2. Select **File → Open Folder** and open your RadaVis project.
3. Install the Python and Jupyter extensions from Microsoft.
4. Press `Ctrl + Shift + P`.
5. Select **Python: Select Interpreter**.
6. Choose the `RadaVis` Conda environment.
7. For Jupyter Notebooks, also select the corresponding Python kernel.

### Step 6 — Obtain the Original Radarize Source Code

The original Radarize code is maintained in a separate repository.

If needed, clone it inside the local RadaVis folder:

```bash
git clone https://github.com/ConnectedSystemsLab/radarize_ae.git
```

The `radarize_ae/` folder is excluded from our group Git repository through `.gitignore`.

This prevents mixing the original Radarize repository with our own project code.

Cloning the source repository does not automatically download the full radar dataset.

## 6. Dataset and Model Files

The official Radarize files are available on [Zenodo](https://zenodo.org/records/11093859).

| File | Approximate Download Size | Purpose |
|---|---|---|
| dataset.zip | 84.2 GB | Original Radarize dataset |
| eval.zip | 1.3 GB | Evaluation artifacts and saved models |

**Team members do not need to download the complete dataset at this stage.**

Our planned workflow is to:

1. Inspect the available pretrained models and evaluation artifacts.
2. Identify the files required for Translation Model inference.
3. Verify access to model inputs and reference velocity labels.
4. Run the model on the Jetson device when its environment is ready.
5. Export suitable prediction results and selected heatmaps for shared analysis.
6. Use these smaller outputs for visualization on personal laptops.

Data availability, model checkpoint compatibility, and the final processing workflow are still being investigated.

## 7. Phase I — Initial Experimental Results

### Experiment Setup

We evaluated the pretrained Radarize Translation ResNet18 model on a real held-out robot sequence.

| Item | Configuration |
|---|---|
| Sequence | `bot_beckman_5thfloor_1` |
| Platform | Robot |
| Checkpoint | `transnet18`, `main_0` |
| Input | Two Doppler-Azimuth heatmaps |
| Tensor shape | `(N, 2, 60, 181)` |
| Output | Predicted `vx` and `vy` |
| Frames | 1,798 |
| Duration | Approximately 59.9 seconds |
| Inference hardware | NVIDIA Jetson AGX Orin |
| Framework | PyTorch |

We selectively obtained one ROS bag from the official Radarize dataset and processed it into model-compatible radar heatmaps and reference velocity arrays.

The pretrained checkpoint was loaded and evaluated on the Jetson GPU. The resulting predictions were transferred to Windows for interactive visualization.

### Prediction Accuracy

| Metric | vx (m/s) | vy (m/s) |
|---|---:|---:|
| MAE | 0.0484 | 0.0250 |
| RMSE | 0.0667 | 0.0346 |

These results are preliminary and refer to a single held-out sequence. They are not intended to represent performance across the complete dataset.

### Visualization 1 — Interactive Velocity Time Series

Our first Phase I visualization was developed with Claude assistance and implemented using Altair.

It compares predicted and ground-truth velocities over time, together with signed errors in both velocity components.

The visualization supports interactive zooming, hovering, and frame selection.

**Notebook:** `notebooks/phase1/01_velocity_timeseries.ipynb`

**Prediction file:** `results/phase1/main_0/bot_beckman_5thfloor_1_predictions.npz`

**HTML visualization:** `results/phase1/main_0/bot_beckman_5thfloor_1_timeseries.html`

### Initial Findings

The first visualization reveals several patterns worth investigating:

- A substantial prediction/reference disagreement near frames 546–559, around 18.2–18.6 seconds.
- Repeated stop-and-start motion, with predictions broadly following changes in forward velocity.
- Smoother model predictions compared with the reference signal during cruising.
- Possible speed-dependent prediction bias.
- Differences between forward and lateral velocity behavior.

These observations are preliminary. In particular, the suspected reference-data anomaly has not yet been confirmed.

### Reproducing the Visualization

The visualization notebook was successfully executed on Windows using the `RadaVisViz311` Conda environment and Altair 6.0.

From the repository root:

```bash
conda activate RadaVisViz311
python -m pip install "altair==6.0.0"
python -m jupyter nbconvert --to notebook --execute "notebooks/phase1/01_velocity_timeseries.ipynb" --output "01_velocity_timeseries_executed.ipynb"
```

The notebook requires the prediction NPZ at the path listed above. It produces an interactive HTML visualization in the results directory.

The original radar dataset and pretrained checkpoint are not required for viewing the HTML, but are required to reproduce the upstream inference pipeline.

### Limitations and Next Steps

The initial analysis has several limitations:

- Only one robot sequence has been analyzed so far.
- Ground-truth anomalies and potential temporal misalignment must be investigated.
- Additional held-out sequences and different platforms are needed to test generalizability.

Next, we will investigate prediction errors as a function of motion speed and acceleration, compare representative low- and high-error samples, and expand the analysis to more held-out sequences.

### AI-Assisted Workflow

Claude was used to propose and implement the initial visualization. The team independently ran the notebook, inspected the HTML output, and identified which interpretations require further verification.

Significant Claude interactions and the team's decisions are documented in:

`reports/phase1/ai_logs/AI_Interaction_Log.md`

## 8. Reproducibility — Radarize Translation Model

We reproduced the Radarize Translation model pipeline using the real `bot_beckman_5thfloor_1` sequence and the pretrained `main_0` checkpoint.

### Data Preprocessing

The script `src/prepare_translation_npz.py` converts the original ROS bag into a model-compatible NPZ file containing:

- `time`: `(1798,)`
- `radar_d`: `(1798, 1, 60, 181)`
- `radar_de`: `(1798, 1, 60, 181)`
- `velo_gt`: `(1798, 3)`

The script uses the original Radarize radar-processing functions and calibration files.

It runs on our Jetson Ubuntu environment with the necessary ROS bag and scientific Python dependencies.

Example preprocessing command (Jetson Ubuntu):

source ~/venvs/radavis_preprocess/bin/activate
unset PYTHONPATH
cd ~/RadaVis/radarize_ae
PYTHONPATH="$PWD" python ../src/prepare_translation_npz.py

The script requires the original Radarize repository, radar calibration files, and the selected ROS bag.

Note: The current script is specific to bot_beckman_5thfloor_1 and writes to data/processed/bot_beckman_5thfloor_1.npz. Running it again will overwrite that output file, so existing results should be backed up first.

We verified reproducibility by running a separate test copy and comparing the generated arrays against the original processed NPZ.

### Model Inference

The script `src/run_translation_inference.py` loads the pretrained Translation ResNet18 checkpoint and predicts two-dimensional velocity.

Example command, from the RadaVis project root on Jetson:

```bash
python3 src/run_translation_inference.py \
  --input data/processed/bot_beckman_5thfloor_1.npz \
  --checkpoint models/main_0/transnet18.pth \
  --output results/phase1/main_0/bot_beckman_5thfloor_1_predictions_reproduced.npz
```

The script supports CPU or CUDA inference and produces predictions, ground-truth velocities, and timestamps.

### Reproducibility Verification

Both stages were independently rerun on the NVIDIA Jetson AGX Orin.

**Preprocessing:** All four output arrays matched the original processed data exactly (`np.array_equal=True`, maximum difference = 0).

**Inference:** All five saved prediction-output arrays matched the original inference results, with no differences at the reported numerical precision.

The reproduced evaluation results were:

| Metric | vx (m/s) | vy (m/s) |
|---|---:|---:|
| MAE | 0.04838 | 0.02498 |
| RMSE | 0.06666 | 0.03462 |

These checks establish reproducibility for this sequence, checkpoint, and environment. Additional sequences remain to be evaluated.

The original ROS bags, pretrained checkpoints, and large processed datasets are not committed to GitHub. They must be obtained separately from the official Radarize resources.

## 9. Midpoint Submission

Required:

- Code from both pairs
- AI interaction record from the AI-aided pair
- Recorded progress update of up to 5 minutes

The video should introduce the problem, summarize the findings of both pairs, show important visualizations, and outline the Phase II plan.

## 10. Final Submission

Required:

- Complete code from both pairs
- AI interaction records from both phases
- A recorded presentation of up to 10 minutes
- Presentation slide deck