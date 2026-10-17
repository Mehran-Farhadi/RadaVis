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

- **Input:** Single-channel Doppler-Azimuth Heatmap (96 × 180)
- **Output:** Two-dimensional velocity (vx, vy)
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
- Error vs. Motion Speed
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

The planned approach is to use an NVIDIA Jetson AGX Orin running Ubuntu for computationally intensive tasks. Its software compatibility and model setup still need to be verified.

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
conda create -n RadaVis python=3.9 pip -y
conda activate RadaVis
```

This creates a dedicated Python environment without modifying your existing base environment.

### Step 3 — Install Visualization Libraries

Run:

```bash
conda install -c conda-forge numpy=1.23.5 pandas matplotlib=3.6.3 jupyterlab ipykernel -y
```

These packages support numerical analysis, visualization, and Jupyter Notebooks.

### Step 4 — Verify Installation

```bash
python -c "import numpy, pandas, matplotlib, jupyterlab, ipykernel; print('RadaVis environment ready!')"
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

### Midpoint Submission

Required:

- Code from both pairs
- AI interaction record from the AI-aided pair
- Recorded progress update of up to 5 minutes

The video should introduce the problem, summarize the findings of both pairs, show important visualizations, and outline the Phase II plan.

### Final Submission

Required:

- Complete code from both pairs
- AI interaction records from both phases
- A recorded presentation of up to 10 minutes
- Presentation slide deck