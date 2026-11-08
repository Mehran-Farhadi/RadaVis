# RadaVis — AI Interaction Log

**Course:** AI and Visualization — JKU, Winter Semester 2026
**Project:** RadaVis — Radarize Translation Model
**Phase:** Phase I — Model Behavior Analysis
**Pair:** AI-aided
**AI Tool:** Claude AI Agent
**Model:** Radarize Translation ResNet18

---

## 1. Purpose and Documentation Method

This document records significant AI-assisted activities during Phase I of the RadaVis project.

Our research question is:

**Under what conditions does the Radarize Translation model predict velocity accurately or inaccurately?**

We use visualization to investigate prediction errors, motion conditions, and possible data-quality issues.

For each significant interaction, we document:

- The research objective and prompt, where available.
- Suggestions, findings, or code produced with AI assistance.
- Human decisions and changes to the proposed approach.
- Independent verification against source code or experimental data.
- Limitations, failures, and lessons learned.

We distinguish between **AI suggestions**, **observed results**, and **verified conclusions**.

The Claude conversation archive contains the original interactions. Where an exact prompt is not available in the current written record, we provide a summary or explicitly note the missing information rather than inventing a quotation.

Only significant interactions that influenced the project's direction, implementation, or visualization design are documented here.

---

## 2. Interaction Overview

| ID | Topic | Main Outcome | Status |
|---|---|---|---|
| AI-01 | Translation model investigation | Identified the model architecture and inference requirements | Completed |
| AI-02 | Dataset access and sequence selection | Obtained one ROS bag without downloading the complete dataset | Completed |
| AI-03 | Technical validation checkpoint | Reproduced preprocessing and model inference | Completed; human-controlled validation |
| AI-04 | Velocity time-series visualization | Investigated errors over time and identified candidate failure cases | Completed |
| AI-05 | Error vs. speed visualization | Investigated speed-dependent errors and sensitivity to suspicious frames | Completed for one sequence |

**Note on AI-03:** This entry documents the technical work connecting the dataset investigation to the visualizations. The supplied interaction log does not contain a verified Claude prompt for this step. It is included for chronological completeness and is not presented as a separate, confirmed Claude exchange.

---

## 3. AI-01 — Translation Model Investigation

**Date:** October 27, 2026
**Tool:** Claude
**Type:** Source-code and model investigation

### 3.1 Objective

Identify the exact model architecture, checkpoint configuration, input requirements, and dependencies needed to evaluate the pretrained Radarize Translation model.

### 3.2 Prompt

**Recorded prompt summary:**

Investigate Radarize's pretrained Translation model, its input data requirements, checkpoint configuration, and whether inference can run independently of the complete ROS/Cartographer pipeline.

The original prompt and response are retained in the Claude conversation archive.

### 3.3 AI Findings

Claude identified several important technical details:

- The Translation component uses a ResNet18-based neural network.
- The input consists of two Doppler-Azimuth heatmaps: `radar_d` and `radar_de`.
- The expected model input has shape `(B, 2, 60, 181)`.
- The model predicts two velocity components, `vx` and `vy`.
- Multiple pretrained checkpoints correspond to different dataset splits.
- Standalone inference may be possible without executing the complete SLAM system.

Claude also identified checkpoint compatibility and software dependencies as potential difficulties.

### 3.4 Human Verification

We inspected the original Radarize repository:

`https://github.com/ConnectedSystemsLab/radarize_ae`

Relevant files included:

- `radarize/flow/model.py`
- `radarize/flow/dataloader.py`
- `tools/test_flow.py`
- `radarize/config/default.py`

The original evaluation code concatenates the two radar inputs along the channel dimension before passing them to the network.

We subsequently inspected the actual pretrained `main_0` checkpoint and confirmed:

| Parameter | Verified Value |
|---|---|
| Model name | `transnet18` |
| Model type | `ResNet18` |
| Input channels | 2 |
| Output values | 2 |
| Input shape | `(B, 2, 60, 181)` |

Standalone model execution was later confirmed on our Jetson device.

### 3.5 Human Decisions

**Accepted:** Focus on the Translation ResNet18 model for Phase I.

**Modified:** Instead of installing the complete Radarize SLAM environment, investigate the minimum requirements for preprocessing and inference.

**Deferred:** Full ROS/Cartographer-based SLAM evaluation and the complete dataset download.

### 3.6 Reflection

Claude helped us identify relevant source files and reduce the technical scope of the project.

However, reading source code alone was not enough to establish that the model would execute successfully.

We learned that model architecture, preprocessing conventions, checkpoint selection, and dataset split membership must be verified using the actual software and data.

**Status:** Completed. The model configuration and standalone inference were subsequently verified experimentally.

---

## 4. AI-02 — Dataset Access and Sequence Selection

**Period:** Initial dataset investigation, before the first model evaluation
**Tool:** Claude
**Type:** Data-access investigation and selective download

### 4.1 Objective

Obtain a small, usable portion of the official Radarize dataset for testing the Translation model without downloading the complete dataset.

### 4.2 Prompt

**Prompt summary; exact wording not preserved in the supplied log:**

Investigate the contents of the Radarize dataset and evaluation archives. Determine whether one suitable test sequence and its pretrained model checkpoint can be accessed without downloading the full dataset.

### 4.3 AI Findings and Suggestions

Claude inspected the archive structure and reported:

- The official `dataset.zip` archive is approximately 84.2 GB.
- It contains individual ROS bag files, rather than ready-to-use Translation input NPZ files.
- Individual ZIP entries can potentially be downloaded through HTTP Range requests.
- The `eval.zip` archive contains pretrained Translation checkpoints for different dataset splits.
- A processed NPZ input must be generated locally from the selected ROS bag.

The selected sequence was:

`bot_beckman_5thfloor_1`

The selected checkpoint was:

`output_main_0/transnet18/transnet18.pth`

Claude suggested downloading only the required archive entry rather than the complete dataset.

### 4.4 Implementation

A Python script was prepared for selective retrieval:

`src/download_bag_range.py`

The script requests the relevant ZIP entry, extracts the ROS bag, and checks the downloaded data.

It also checks the expected archive metadata and verifies the extracted file.

### 4.5 Human Verification

We ran the selective-download procedure using the official Zenodo archive.

The selected file was successfully downloaded and extracted.

Verified details included:

| Item | Result |
|---|---|
| Sequence | `bot_beckman_5thfloor_1` |
| Compressed entry | Approximately 551.5 MB |
| Extracted ROS bag | Approximately 630.8 MB |
| Archive verification | Passed |
| CRC-32 verification | Passed |
| ROS bag readability | Passed |

The ROS bag contained both topics required for our initial analysis:

- `/radar0/radar_data`
- `/tracking/odom/sample`

Using `rosbag`, we confirmed that the selected sequence contains 1,800 radar messages and 11,973 odometry messages.

The selected ROS bag was transferred to the Jetson for preprocessing.

### 4.6 Human Decisions

**Accepted:** Selective retrieval of a single ROS bag.

**Accepted:** Use `bot_beckman_5thfloor_1` for the first Translation inference experiment.

**Modified:** Use an isolated data-preparation workflow rather than the full SLAM pipeline.

**Deferred:** Downloading the full dataset and processing all available sequences.

### 4.7 Reflection

This interaction substantially reduced the amount of data needed to begin the project.

The AI suggestion was useful because it provided a practical solution to the dataset-size problem.

However, the proposed download procedure was not accepted without testing. We independently checked file integrity, ROS bag readability, and required topics.

The main lesson was that **efficient access to data does not automatically guarantee usable model inputs**. Preprocessing and synchronization still had to be verified.

### 4.8 Artifacts

- `src/download_bag_range.py` — local selective-download utility
- `data/raw/bot_beckman_5thfloor_1.bag` — local data, not committed to GitHub
- Official dataset: `https://zenodo.org/records/11093859`

**Status:** Completed. The selected sequence was retrieved and verified.

---

## 5. AI-03 — Data Preparation and Model Inference Validation

**Period:** Before and during the first Phase I visualizations
**Type:** Human-controlled technical validation checkpoint

**Documentation note:** No verified standalone Claude prompt for this stage is available in the supplied AI log. This section records the experimental steps and verification results that made the subsequent AI-assisted visualizations possible. It should not be interpreted as evidence that Claude generated all of the technical code.

### 5.1 Objective

Convert the selected ROS bag into model-compatible inputs, run the pretrained Translation network, and obtain trustworthy predictions for visualization.

### 5.2 Data Preprocessing

We used a lightweight script based on functions from the original Radarize repository:

`src/prepare_translation_npz.py`

The script extracts the two Doppler-Azimuth representations and reference velocity values.

The original Radarize preprocessing functions and calibration files were used.

The processed sequence contains:

| Array | Shape |
|---|---|
| `time` | `(1798,)` |
| `radar_d` | `(1798, 1, 60, 181)` |
| `radar_de` | `(1798, 1, 60, 181)` |
| `velo_gt` | `(1798, 3)` |

The two heatmaps are concatenated to form the model input:

`(1798, 2, 60, 181)`

### 5.3 Model Inference

The pretrained model was executed on an NVIDIA Jetson AGX Orin using PyTorch and CUDA.

We used:

- Model: Translation ResNet18
- Checkpoint: `main_0/transnet18.pth`
- Sequence: `bot_beckman_5thfloor_1`
- Frames: 1,798

The inference script is:

`src/run_translation_inference.py`

The saved output contains:

- `time`
- `flow_pred_xs`
- `flow_pred_ys`
- `flow_gt_xs`
- `flow_gt_ys`

### 5.4 Quantitative Results

| Metric | vx (m/s) | vy (m/s) |
|---|---:|---:|
| MAE | 0.04838 | 0.02498 |
| RMSE | 0.06666 | 0.03462 |

These values describe one held-out robot sequence, not the complete Radarize dataset.

### 5.5 Independent Reproducibility Verification

We subsequently reran both technical stages.

**Preprocessing verification**

The original and reproduced processed NPZ files were compared array by array.

For all four arrays:

- Array shapes matched.
- `np.array_equal` returned `True`.
- Maximum numerical difference was zero.

**Inference verification**

The original and reproduced prediction NPZ files were also compared.

All five saved arrays passed the comparison:

- `time`
- `flow_pred_xs`
- `flow_pred_ys`
- `flow_gt_xs`
- `flow_gt_ys`

For each array, the maximum difference displayed to ten decimal places was zero and `np.allclose` returned `True`.

This confirms that our scripts can reproduce the previous results using the same sequence, checkpoint, and computational environment.

### 5.6 Human Decisions and Limitations

We chose to keep preprocessing and inference separate from the Windows visualization environment.

This allowed us to use the Jetson for model execution while developing and reviewing visualizations on Windows.

We also avoided committing large ROS bags, pretrained checkpoints, and processed datasets to GitHub.

The preprocessing script is currently specific to `bot_beckman_5thfloor_1`.

Our verification establishes repeatability of the implemented pipeline for this sequence. It does not establish generalization to other datasets or prove that every behavior of the full Radarize SLAM pipeline has been reproduced.

### 5.7 Reflection

The technical validation was essential because the subsequent visualizations depend on correct inputs and outputs.

We did not rely only on aggregate MAE and RMSE. We also verified the underlying arrays and reproduced both stages of the pipeline.

This distinction is important: **reproducing a prediction does not establish that the prediction or its reference label is physically correct**.

### 5.8 Artifacts

- `src/prepare_translation_npz.py`
- `src/run_translation_inference.py`
- `data/processed/bot_beckman_5thfloor_1.npz` — local
- `results/phase1/main_0/bot_beckman_5thfloor_1_predictions.npz` — local

**Status:** Preprocessing and inference successfully reproduced for the selected sequence.

---

## 6. AI-04 — Velocity Time-Series Visualization

**Date:** November 7, 2026
**Tool:** Claude
**Type:** Visualization design, implementation, and interpretation

### 6.1 Objective

Investigate the model's velocity predictions over time to identify periods of accurate prediction, large errors, motion transitions, and possible systematic behavior.

### 6.2 Recorded Prompt

> We have run Radarize Translation ResNet18 on 1,798 test frames and saved predicted and ground-truth vx/vy.
>
> I want to understand when the model predicts velocity well or poorly, not just report MAE/RMSE.
>
> What visualizations should we start with? Suggest 3 options, explain what each could reveal, and recommend one to implement first. Don't write code yet.

### 6.3 AI Suggestions

Claude proposed three visualization approaches:

1. Time-series comparison of predicted and ground-truth velocity.
2. Error as a function of motion speed and acceleration.
3. Analysis of speed and direction errors.

Claude recommended the time-series visualization first.

The reasons included preserving temporal context, identifying large error intervals, investigating possible lag, and observing systematic bias.

### 6.4 Human Decisions

**Accepted:** Start with the time-series view.

**Accepted:** Include both velocity components and their signed errors.

**Modified:** Treat visually unusual ground-truth values as suspicious observations, not proven sensor failures.

**Deferred:** Detailed speed-dependent and direction-dependent analyses until the first visualization had been examined.

### 6.5 Implementation

Claude developed an interactive Altair visualization.

**Notebook:**

`notebooks/phase1/01_velocity_timeseries.ipynb`

**HTML output:**

`results/phase1/main_0/bot_beckman_5thfloor_1_timeseries.html`

The visualization includes:

- An overview of the velocity-error magnitude.
- Predicted and reference forward velocity (`vx`).
- Signed forward prediction error.
- Predicted and reference lateral velocity (`vy`).
- Signed lateral prediction error.
- Interactive zooming, hovering, and frame selection.

All plots use a shared time axis.

### 6.6 Human Verification

We independently checked:

- The prediction data contain 1,798 frames.
- The sequence lasts approximately 59.9 seconds.
- The sequence belongs to the selected `main_0` test split.
- Predictions were generated using the pretrained checkpoint on the Jetson.
- The notebook executed locally on Windows.
- The HTML file was generated and opened successfully in Chrome.

An earlier execution attempt encountered a Pandas DLL-loading problem inside the Windows VS Code notebook environment.

We avoided changing Windows security policies and used an independent Jupyter execution workflow.

Later, a dedicated Python 3.11 visualization environment was created:

`RadaVisViz311`

The visualization notebooks were then successfully executed using the updated environment.

This was an environment-related problem, not evidence of an error in the trained model.

### 6.7 Observations and Quantitative Checks

**O1 — Large disagreement near frames 546–559**

A large difference between prediction and reference velocity was observed around 18.2–18.6 seconds.

During these 14 frames, the reference velocity remains fixed at approximately:

- `vx = -0.1183 m/s`
- `vy = -0.1450 m/s`

The average predicted forward velocity is approximately `+0.2445 m/s`.

This short interval contributes approximately 23.1% of the total squared forward-velocity error.

Claude suggested that the interval might represent a reference-data anomaly.

**Human interpretation:** The disagreement is established, but the cause is not. Raw odometry or other independent measurements are needed before treating the reference signal as faulty.

**O2 — Stop-and-start motion**

The robot repeatedly slows down to near-zero forward velocity.

The model generally follows these stops, though some discrepancies occur around transitions.

For 46 frames with reference speed below 0.05 m/s, the median predicted speed was approximately 0.0276 m/s.

This suggests that stopping behavior deserves separate investigation.

**O3 — Cruising behavior**

During some periods of sustained movement, the model prediction is smoother than the reference velocity.

For example:

- At 51–58 seconds, the mean signed forward error is approximately `−0.0651 m/s`.
- At 12–16 seconds, the corresponding mean error is approximately `+0.0440 m/s`.

This motivates investigation of speed-dependent error.

**O4 — Lateral velocity**

The lateral velocity component is generally smaller than the forward component in this sequence.

The reference and predicted lateral-velocity standard deviations were approximately:

- Reference: `0.0326 m/s`
- Prediction: `0.0153 m/s`

The prediction is less variable, but this does not by itself prove better accuracy or establish the reason for the difference.

**O5 — Individual low-error example**

Frame 738, approximately 24.60 seconds into the sequence, provides a candidate low-error example.

| Quantity | Value |
|---|---:|
| True vx | 0.265 m/s |
| Predicted vx | 0.267 m/s |
| True vy | 0.020 m/s |
| Predicted vy | 0.024 m/s |
| 2D error magnitude | Approximately 0.0053 m/s |

This frame can later be compared with high-error inputs.

### 6.8 Reflection

Claude helped us turn a prediction file into a visual investigation of model behavior.

The time-series view revealed patterns that would have been difficult to understand from MAE and RMSE alone.

However, an unusual visual pattern does not automatically reveal its cause.

Our independent checks confirmed the numerical observations, while human judgment was needed to avoid prematurely classifying the suspected reference anomaly as a model failure or a sensor failure.

The visualization also helped define the next research question: **Does prediction error depend systematically on motion speed?**

### 6.9 Artifacts

- `notebooks/phase1/01_velocity_timeseries.ipynb`
- `notebooks/phase1/01_velocity_timeseries_executed.ipynb`
- `results/phase1/main_0/bot_beckman_5thfloor_1_timeseries.html`
- Local prediction NPZ used to generate the visualization

**Status:** Implemented, independently executed, and inspected. Interpretation remains limited to the selected sequence.

---

## 7. AI-05 — Error vs. Speed Visualization

**Date:** November 7, 2026
**Tool:** Claude
**Type:** Follow-up visualization, numerical verification, and interpretation

### 7.1 Objective

Determine whether the Translation model's prediction errors vary with motion speed.

Also examine whether the findings depend on frames 546–559, the interval identified as suspicious in the time-series visualization.

### 7.2 Recorded Prompt

> Using our existing `bot_beckman_5thfloor_1` predictions, create an interactive Error vs. Speed visualization for Phase I.
>
> Show signed error and absolute error across speed ranges, and compare results with and without frames 546–559 (suspected GT anomaly). Use binned summaries to avoid overplotting.
>
> Save the notebook in `notebooks/phase1/` and generate an HTML output. Explain what the plot reveals, but don't assume the GT anomaly is confirmed.

### 7.3 AI Suggestions

Claude proposed a binned error-versus-speed visualization rather than plotting all 1,798 points as a dense scatterplot.

The implementation includes:

- Speed bins of 0.05 m/s.
- Signed forward velocity error.
- Signed lateral velocity error.
- Two-dimensional absolute velocity error.
- Median and mean error estimates.
- Interquartile and 10–90% error ranges.
- Comparison of all frames against results excluding frames 546–559.
- A time strip linked to the selected speed bin.
- Alternative definitions of speed for sensitivity analysis.

The signed errors are defined as:

`e_x = predicted vx − true vx`

`e_y = predicted vy − true vy`

The 2D absolute error is:

`|e| = sqrt(e_x² + e_y²)`

### 7.4 Human Decisions

**Accepted:** Binned summaries instead of a dense scatterplot.

**Accepted:** The three error measures because they distinguish forward, lateral, and total prediction errors.

**Accepted:** Comparison with and without frames 546–559.

**Modified:** The suspicious interval is excluded only as a sensitivity experiment. We have not corrected or replaced the original ground truth.

**Accepted with caution:** Alternative speed definitions to examine whether the interpretation depends on the chosen horizontal-axis variable.

**Deferred:** Generalizing the findings until more held-out sequences are evaluated.

### 7.5 Implementation

**Notebook:**

`notebooks/phase1/02_error_vs_speed.ipynb`

**Executed notebook:**

`notebooks/phase1/02_error_vs_speed_executed.ipynb`

**HTML output:**

`results/phase1/main_0/bot_beckman_5thfloor_1_error_vs_speed.html`

The visualization contains three main error panels and an interactive time strip.

The chart compares all frames with a second version excluding the suspicious interval.

### 7.6 Independent Visualization Verification

The HTML visualization was opened and visually inspected in Chrome.

The inspection confirmed the presence of:

- Forward Error.
- Lateral Error.
- Absolute Error.
- All Frames and Excluding Frames 546–559 comparisons.
- A speed-bin selection linked to the time strip.
- A speed-axis menu with three options.

The interactive control specifications were inspected in the generated HTML.

**Limitation:** Complete manual testing of every browser interaction has not been independently documented.

The HTML was regenerated locally after the notebook was executed.

### 7.7 Independent Numerical Verification

We independently recomputed the visualization's central statistics from:

`results/phase1/main_0/bot_beckman_5thfloor_1_predictions.npz`

Using NumPy, we confirmed:

| Check | Result |
|---|---|
| Original frame count | 1,798 |
| All timestamp and velocity values finite | Yes |
| Frames excluded | 14 |
| Frames remaining | 1,784 |
| Forward MAE | 0.04838 m/s |
| Lateral MAE | 0.02498 m/s |
| Independent speed-bin counts | Matched visualization |

The default speed axis uses the magnitude of the reference velocity.

The independently verified bin counts were:

| GT Speed (m/s) | All Frames | Excluding 546–559 |
|---|---:|---:|
| 0.00–0.05 | 46 | 46 |
| 0.05–0.10 | 144 | 144 |
| 0.10–0.15 | 74 | 74 |
| 0.15–0.20 | 216 | 202 |
| 0.20–0.25 | 476 | 476 |
| 0.25–0.30 | 517 | 517 |
| 0.30–0.35 | 278 | 278 |
| 0.35–0.40 | 44 | 44 |
| 0.40–0.45 | 3 | 3 |

The counts confirm that the 14 excluded frames belong to the 0.15–0.20 m/s bin under the default GT-speed definition.

### 7.8 Main Findings

**F1 — Speed-dependent forward error**

The median signed forward error changes systematically across speed ranges.

| GT Speed (m/s) | Median Forward Error (m/s) |
|---|---:|
| 0.15–0.20 | +0.0746 |
| 0.20–0.25 | +0.0236 |
| 0.25–0.30 | −0.0217 |
| 0.30–0.35 | −0.0685 |
| 0.35–0.40 | −0.1204 |

Positive error indicates that the predicted forward velocity is above the reference value.

Negative error indicates that it is below the reference value.

The pattern suggests that, in this sequence, the model overestimates some lower forward speeds and underestimates higher forward speeds.

**F2 — Sensitivity to the suspicious interval**

Removing frames 546–559 reduces the number of samples in the 0.15–0.20 m/s speed bin from 216 to 202.

The median forward error in that bin changes only slightly, from approximately +0.0746 to +0.0718 m/s.

The broader speed-dependent pattern remains visible.

This means the main trend is not explained solely by those 14 frames.

However, their removal does not prove that the ground-truth values are incorrect.

**F3 — Lateral error**

Median lateral errors remain relatively small over the well-populated speed bins.

The lateral and forward components show different error characteristics in this sequence.

**F4 — Absolute error**

The 2D absolute error varies with speed and is higher in several speed ranges outside the main cruising region.

Bins with very few observations, especially 0.40–0.45 m/s with only three frames, should not be used to draw strong conclusions.

**F5 — Choice of speed axis**

The visualization includes alternative speed definitions, such as smoothed reference speed and predicted speed.

Changing the speed definition can change the apparent relationship between speed and error.

This is important because error is calculated relative to the same reference velocity used for default speed binning.

We therefore treat the observed trend as descriptive rather than a demonstrated causal effect.

### 7.9 Human Verification of the Notebook

The notebook was executed using the local Windows visualization environment with Python 3.11.

Additional NumPy verification cells were run independently of the visualization's binned-summary code.

These checks confirmed:

- Correct prediction and reference array lengths.
- Correct error formulas.
- Correct number of excluded frames.
- Correct bin counts.
- Consistent median and mean calculations.

The output was also compared with the results of the original model execution on Jetson.

No numerical discrepancy was identified in the checks reported above.

### 7.10 Reflection

This interaction was particularly useful because it transformed a visual observation from AI-04 into a quantitative question.

Instead of stating only that the predictions appeared too smooth, we investigated how the direction and magnitude of errors changed across different reference speeds.

We also learned that a visualization can produce a convincing pattern without establishing why that pattern occurs.

The speed-dependent error could be influenced by model behavior, reference-signal characteristics, or the distribution of motion conditions.

Our sensitivity analysis helped identify the influence of suspicious frames without silently modifying the dataset.

Independent calculations were essential for checking the AI-generated visualization.

**Human conclusion:** We accept the measured error pattern as a finding for the selected sequence, but not as proof of a general model limitation across the complete dataset.

### 7.11 Artifacts

- `notebooks/phase1/02_error_vs_speed.ipynb`
- `notebooks/phase1/02_error_vs_speed_executed.ipynb`
- `results/phase1/main_0/bot_beckman_5thfloor_1_error_vs_speed.html`
- Local prediction NPZ used for numerical verification

**Status:** Implemented, independently executed, and numerically verified for the selected sequence. Additional data and causal investigation remain necessary.

## 8. AI-06 — Radar Input and Error Explorer

**Phase:** Phase I — Black-box Model Behavior Analysis
**Status:** Implemented, executed, and independently inspected on Windows.

### 8.1 Objective

Investigate how the actual radar inputs differ between low-error and high-error predictions under similar reference-speed conditions.

This visualization extends the previous time-series and error-versus-speed analyses by connecting model outputs with the two input heatmaps, `radar_d` and `radar_de`.

The purpose is exploratory: to identify visible differences and formulate questions for future investigation, without making causal or explainability claims.

### 8.2 AI Prompts

Two significant Claude interactions were used.

**Interaction A — Visualization design and implementation**

Claude was asked to create an interactive Radar Input & Error Explorer using a real NPZ file containing ten selected frames organized into five low-error/high-error pairs.

The requirements included:

- Side-by-side visualization of both radar channels.
- Consistent color scales within each channel.
- Ground-truth and predicted velocities.
- Two-dimensional prediction errors.
- Interactive pair selection.
- An overview of all five pairs.
- A presentation-quality static figure.
- Numerical verification and scientific limitations.

**Interaction B — Technical and scientific audit**

Claude was subsequently asked to audit the original Radarize normalization, color-scale comparability, offline HTML reproducibility, displayed numerical values, and scientific interpretation.

The audit was restricted to the three AI-06 deliverables. No modification of the Human-only notebook was requested.

*The complete original prompts and AI responses are retained in the Claude conversation. The descriptions above summarize their objectives rather than presenting reconstructed wording as verbatim prompts.*

### 8.3 Input Data and Case Selection

The source file is:

`results/phase1/main_0/bot_beckman_5thfloor_1_matched_cases.npz`

It contains ten frames from the held-out `bot_beckman_5thfloor_1` sequence, organized into five pairs.

| Pair | Low-error frame | High-error frame |
|---|---:|---:|
| 1 | 192 | 386 |
| 2 | 1681 | 667 |
| 3 | 656 | 1050 |
| 4 | 1676 | 1378 |
| 5 | 188 | 62 |

Each frame includes:

- The two radar input channels, each of shape `(1, 60, 181)`.
- Ground-truth velocity `(vx, vy)`.
- Predicted velocity `(vx, vy)`.
- Reference speed.
- Two-dimensional prediction error.
- Frame index and timestamp.

Pairs were selected within narrow reference-speed intervals. However, their lateral velocities and recording times are not identical.

Frames 546–559, previously identified as suspicious, were excluded.

### 8.4 Visualization Design

Claude implemented an interactive visualization featuring:

1. An overview of all five pairs, comparing prediction errors, reference speeds, and lateral reference velocities.
2. A selector that switches between the five pairs.
3. Numerical detail panels for the selected low-error and high-error frames.
4. A 2×2 grid of actual radar heatmaps.
5. Separate colorbars for `radar_d` and `radar_de`.
6. Mean intensity profiles over Doppler and azimuth bins.
7. A static figure suitable for the midpoint presentation.

Pair 3 is the default example.

The heatmaps use a fixed numerical color range of 0–1. This supports consistent comparisons between frames within the same radar channel.

The original Radarize preprocessing treats `radar_d` and `radar_de` differently. Therefore, equal displayed color values across the two channels should not be interpreted as physically equivalent measurements.

### 8.5 AI-generated Corrections

During the technical audit, Claude reported and corrected several issues:

- Clarified that color-scale comparisons are valid within each radar channel, not directly between channels.
- Corrected documentation of the actual radar input ranges.
- Required `vl-convert-python==1.9.0.post1` for self-contained offline HTML export.
- Removed the silent fallback to an internet-dependent HTML file.
- Recomputed displayed velocity errors from full-precision values.
- Corrected confusing numerical formatting, including negative zero.
- Distinguished measured observations from untested hypotheses.
- Clarified that the ten frames were selected based on their errors and are not a representative random sample.

These changes were made before the team's independent Windows execution.

### 8.6 Human Decisions

**Accepted:** Interactive comparison of the five matched-speed pairs.

**Accepted:** Pair 3 as the default presentation example.

**Accepted:** Fixed color scales for comparisons within each channel.

**Accepted:** Separate presentation of radar-input patterns, numerical velocity errors, and motion differences.

**Modified:** Restricted cross-channel color interpretation after reviewing the preprocessing differences.

**Deferred:** Any claim that visible radar patterns caused the observed prediction errors.

**Deferred:** Generalizing conclusions from these ten selected frames to the complete dataset.

The Human-only notebook was not modified.

### 8.7 Independent Windows Verification

The notebook was executed in the team's `RadaVisViz311` environment.

Verified environment:

| Package | Version |
|---|---|
| Python | 3.11.18 |
| NumPy | 1.26.4 |
| Pandas | 2.2.3 |
| Altair | 6.0.0 |
| Matplotlib | 3.10.7 |
| vl-convert-python | 1.9.0.post1 |

The Jupyter execution completed successfully and produced the executed notebook, HTML visualization, and PNG figure.

The generated PNG was inspected in VS Code.

The HTML was opened successfully in Chrome.

**The team manually verified that:**

- Pair 3 opens by default, showing frames 656 and 1050.
- Pair 1 changes the displayed frames to 192 and 386.
- Pair 5 changes the displayed frames to 188 and 62.
- The numerical details, heatmaps, and profiles update when the pair changes.
- Both radar channels are displayed.
- The colorbars show the fixed 0–1 range.
- The overview of all five pairs is visible.

Chrome's Network panel was also inspected with Offline mode enabled. The displayed resources were local or embedded data, with no visible failed external requests.

Claude additionally reported successful numerical, browser, and heatmap-pixel verification during its own audit. These AI-reported checks are distinguished from the team's manually observed Windows checks.

### 8.8 Main Observations

**O1 — Large error differences at similar speeds**

Pair 3 compares frames 656 and 1050.

| Property | Frame 656 | Frame 1050 |
|---|---:|---:|
| Reference speed | 0.225 m/s | 0.228 m/s |
| 2D prediction error | 0.003 m/s | 0.076 m/s |

Although the reference speeds are close, the prediction errors differ substantially.

**O2 — Visually similar radar patterns do not guarantee similar prediction errors**

In Pair 3, the two radar inputs share several visible structural patterns, but the errors are different.

This is an observation, not proof of why the model behaves differently.

**O3 — Differences in radar intensity**

Claude reported differences in overall input values for several selected pairs.

The relationship between input intensity and model error has not yet been tested over the complete sequence.

**O4 — Residual matching limitations**

Even with similar speed magnitudes, the selected frames can differ in lateral velocity, time, scene, and environmental conditions.

Therefore, the comparison does not isolate a single cause of prediction error.

### 8.9 Reflection

This interaction improved the visual quality and scientific relevance of our Phase I analysis.

The first two visualizations investigated when errors occur and how they vary with motion speed. The third visualization allows us to inspect the actual radar inputs corresponding to selected prediction outcomes.

Claude was useful for designing an interactive comparison, implementing the visualizations, and identifying weaknesses in the original color-scale interpretation.

Human verification was still necessary. We independently executed the notebook on Windows and checked the main browser interactions.

An important lesson is that **visually similar inputs can accompany different model errors, but visual similarity alone does not explain the internal reasoning of the network**.

This motivates further black-box investigation and provides questions for Phase II XAI analysis.

### 8.10 Deliverables

**Notebook:**

`notebooks/phase1/03_radar_error_explorer.ipynb`

**Executed notebook:**

`notebooks/phase1/03_radar_error_explorer_executed.ipynb`

**Interactive HTML:**

`results/phase1/main_0/bot_beckman_5thfloor_1_radar_error_explorer.html`

**Static presentation figure:**

`results/phase1/main_0/bot_beckman_5thfloor_1_radar_comparison.png`

**Local input data:**

`results/phase1/main_0/bot_beckman_5thfloor_1_matched_cases.npz`

The NPZ input is stored locally and is not intended for GitHub.

**Final status:** Visualization implemented and successfully executed on Windows. Main browser interactions and displayed structure were inspected by the team. Findings remain exploratory and limited to five selected frame pairs.

## 9. Overall Reflection on AI-Assisted Work

### 9.1 Benefits of AI Assistance

Claude was useful at several stages of our work.

**Technical exploration:** It helped identify relevant model files, data requirements, and practical approaches for working with large archives.

**Visualization design:** It proposed multiple views rather than immediately generating a single chart.

**Implementation:** It helped develop interactive Altair visualizations from saved prediction data.

**Research direction:** It connected observations in the time series to more specific questions about speed-dependent prediction errors.

**Efficiency:** The selective-download approach avoided downloading the complete Radarize dataset just to begin the project.

### 9.2 Problems and Limitations

AI assistance did not eliminate technical or scientific difficulties.

The main challenges included:

- Large datasets and pretrained model files.
- Differences between Python environments on Windows and Jetson.
- An initial Pandas DLL-loading problem inside the Windows notebook environment.
- The need to reconstruct model-compatible radar inputs from ROS bags.
- The danger of treating unusual reference values as confirmed ground-truth errors.
- The risk of generalizing from one test sequence.

We also found that a visualization can be technically correct while its interpretation remains uncertain.

### 9.3 Human Verification and Corrections

We independently checked important technical results instead of relying only on AI-generated descriptions.

Our verification included:

- Inspecting the original Radarize model and evaluation code.
- Checking checkpoint metadata.
- Validating the downloaded ROS bag and required topics.
- Running preprocessing and inference on Jetson.
- Comparing reproduced preprocessing arrays with the originals.
- Comparing reproduced inference outputs with the originals.
- Executing the visualization notebooks on Windows.
- Inspecting the HTML outputs.
- Recomputing error statistics and speed bins independently.

These checks allowed us to separate implementation correctness from scientific interpretation.

### 9.4 Accepted, Modified, and Deferred Decisions

| Decision | Outcome |
|---|---|
| Use standalone Translation inference | Accepted and tested |
| Download the entire dataset immediately | Rejected for the initial experiment |
| Use selective ZIP-entry download | Accepted and verified |
| Start with time-series visualization | Accepted |
| Investigate error as a function of speed | Accepted and implemented |
| Treat frames 546–559 as confirmed faulty GT | Not accepted |
| Exclude suspicious frames for sensitivity analysis | Accepted |
| Generalize findings from one sequence | Deferred |
| Investigate more held-out sequences | Planned |
| Compare low-error and high-error radar heatmaps | Planned |

### 9.5 Lessons Learned

Our experience highlights four important lessons.

**1. AI can accelerate exploration, but cannot replace verification.**

AI suggestions became useful research results only after we checked them against code, real data, and reproducible experiments.

**2. Visualization should reveal questions, not just display metrics.**

The time-series view helped identify unusual intervals. The error-versus-speed view then tested a more specific hypothesis.

**3. Data quality and model behavior must be distinguished.**

A large prediction error does not automatically mean that the neural network is responsible. The reference signal and measurement process also need investigation.

**4. Reproducibility is part of trustworthy AI-assisted analysis.**

We preserved the preprocessing and inference scripts, validated their outputs, and documented the environment used for visualization.

### 9.6 Comparison with Human-only Work

The group also maintains a separate Human-only Phase I notebook:

`notebooks/phase1/human_only/RadaVis_Phase1_Human_Only.ipynb`

The two pairs work on the same model and task but develop their analyses independently.

The Human-only notebook is stored in the shared repository. Its scientific methods, findings, and execution results have not yet been reviewed in this AI-aided log.

A comparison of both pairs' approaches, visualizations, and conclusions will be prepared for the group midpoint presentation without retroactively influencing the independent Human-only analysis.

---

## 10. Phase I Summary and Remaining Work

### 10.1 Completed Work

- Selected the Radarize Translation ResNet18 model.
- Investigated its architecture and checkpoint requirements.
- Obtained one official ROS bag through selective download.
- Generated valid Doppler-Azimuth inputs and reference velocity arrays.
- Executed pretrained model inference on Jetson.
- Reproduced preprocessing outputs exactly.
- Reproduced inference outputs with matching numerical results.
- Developed the interactive velocity time-series visualization.
- Developed the interactive error-versus-speed visualization.
- Independently checked the main error and binning calculations.
- Stored the notebooks, code, and documentation in the group GitHub repository.

### 10.2 Remaining Limitations

Our Phase I results currently cover only:

- One robot sequence: `bot_beckman_5thfloor_1`.
- One pretrained checkpoint: `main_0`.
- Approximately 59.9 seconds and 1,798 frames.

We have not yet established whether the observed behavior generalizes to other environments, platforms, or recordings.

The suspected reference-data anomaly also requires additional investigation.

### 10.3 Next Steps

1. Investigate the suspicious interval using available odometry or independent motion measurements.
2. Evaluate additional held-out sequences and, where feasible, other platform types.
3. Compare low-error and high-error radar heatmaps.
4. Consolidate the Human-only pair's independent results for the midpoint presentation.
5. Relate the main Phase I findings to planned Phase II explainability investigations.

For Phase II, candidate techniques include saliency-based analysis and intermediate feature visualization. The final techniques will be selected and evaluated according to the course requirements.

---

## 11. Reproducibility and Evidence

### 11.1 Original Sources

**Radarize repository:**
https://github.com/ConnectedSystemsLab/radarize_ae

**Radarize dataset:**
https://zenodo.org/records/11093859

**RadaVis group repository:**
https://github.com/Mehran-Farhadi/RadaVis

### 11.2 Key Project Files

**Preprocessing and inference**

- `src/prepare_translation_npz.py`
- `src/run_translation_inference.py`

**Visualization notebooks**

- `notebooks/phase1/01_velocity_timeseries.ipynb`
- `notebooks/phase1/01_velocity_timeseries_executed.ipynb`
- `notebooks/phase1/02_error_vs_speed.ipynb`
- `notebooks/phase1/02_error_vs_speed_executed.ipynb`

**HTML visualizations**

- `results/phase1/main_0/bot_beckman_5thfloor_1_timeseries.html`
- `results/phase1/main_0/bot_beckman_5thfloor_1_error_vs_speed.html`

**Human-only analysis**

- `notebooks/phase1/human_only/RadaVis_Phase1_Human_Only.ipynb`

**Documentation**

- `README.md`
- `reports/phase1/ai_logs/AI_Interaction_Log.md`

The raw radar data, model checkpoints, and large processed NPZ files are not included in the group repository.

### 11.3 Evidence and Provenance Notes

The original Claude conversation should be retained as the primary record of prompts and AI responses.

The prompts reproduced in AI-04 and AI-05 are the wording recorded in the project's existing AI log. Their exact correspondence with the Claude conversation should be checked before final submission.

AI-01 and AI-02 contain prompt summaries because the precise original wording was not available in the supplied written log.

AI-03 is explicitly a technical validation checkpoint, not a verified additional Claude prompt.

The verification results documented here come from the team's recorded execution and comparison outputs.

This distinction is maintained to avoid presenting reconstructed prompts or unverified conclusions as original evidence.
