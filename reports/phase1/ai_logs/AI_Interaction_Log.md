# RadaVis — AI Interaction Log

**Course:** AI and Visualization — JKU, Winter 2026  
**Project:** RadaVis — Radarize Translation Model  
**Phase:** Phase I — Model Behavior Analysis  
**Pair Role:** AI-aided  
**AI Tool:** Claude AI Agent

## Purpose

This log documents significant interactions with Claude that influenced our analysis, implementation, visualization choices, or research decisions.

We record important prompts, AI suggestions, human verification, accepted or rejected recommendations, and observed limitations.

Only significant Claude interactions relevant to the project are included.

---

## AI-01 — Translation Model Investigation

**Date:** October 27, 2026  
**AI Tool:** Claude  
**Task:** Investigate the Radarize Translation model and its inference requirements.

### 1. Objective

Identify the architecture, input data structure, checkpoint requirements, and dependencies needed to evaluate the pretrained Translation model.

### 2. Original Prompt

The original prompt and complete response should be preserved in the Claude conversation archive.

**Prompt summary:** Investigate the pretrained Radarize Translation model, its input requirements, checkpoint configuration, and the possibility of standalone inference without the complete ROS/Cartographer pipeline.

### 3. AI-Generated Findings

Claude reported:

- Translation uses a ResNet18 architecture with two input channels and two velocity outputs.
- The model processes `radar_d` and `radar_de`.
- The expected combined input shape is `(B, 2, 60, 181)`.
- Five pretrained Translation checkpoints are associated with different dataset splits.
- Standalone inference may be possible without running the complete SLAM pipeline.
- Checkpoint loading and software compatibility require further investigation.

### 4. Human Verification

The initial findings were compared with the original Radarize source code.

The input concatenation and the use of `FlowDataset` were consistent with the evaluation implementation.

Other findings, including exact tensor shapes, checkpoint compatibility, and standalone execution, require additional validation using actual data and a successful inference run.

### 5. Decisions

**Accepted:** Continue investigating standalone Translation inference.

**Modified:** Rather than setting up the complete Radarize/ROS environment immediately, first determine the minimum dependencies and dataset requirements.

**Deferred:** Installation of heavy dependencies and extraction of the full dataset until the requirements are confirmed.

### 6. Impact on the Project

The AI-assisted investigation helped narrow the technical scope and identify potential compatibility problems before attempting model execution.

### 7. Limitations and Lessons Learned

- Source-code analysis does not prove that inference will execute successfully.
- AI-generated findings must be checked against the original code and real data.
- Correct train/validation/test split selection is essential for reliable error analysis.

**Status:** Initial code investigation completed; runtime validation pending.

---

## AI-02 — Next Significant Claude Interaction

**Date:**  
**Objective:**  
**Original Prompt / Conversation Reference:**  
**AI Suggestions:**  
**Human Verification:**  
**Accepted / Modified / Rejected:**  
**Impact on Analysis:**  
**Failures or Limitations:**  
**Lessons Learned:**  
**Status:**  



**Human Verification:** The Claude-generated script successfully retrieved and extracted the selected ROS bag from Zenodo. File size, CRC-32, and required ROS topics were verified.

**Decision:** Accepted the selective-download method. We will use this sequence for the initial Translation inference test.

**Impact:** Reduced the initial dataset download from approximately 84 GB to 552 MB.

**Status:** Successfully tested on the actual Radarize dataset.


## AI-04 — Visualization Design and Evaluation
**AI Tool:** Claude  
**Phase:** Phase I — Model Behavior Analysis

### Objective

Explore how visualization can help identify when the Radarize Translation model predicts velocity accurately or inaccurately.

### Original Prompt

> We have run Radarize Translation ResNet18 on 1,798 test frames and saved predicted and ground-truth vx/vy.
>
> I want to understand when the model predicts velocity well or poorly, not just report MAE/RMSE.
>
> What visualizations should we start with? Suggest 3 options, explain what each could reveal, and recommend one to implement first. Don't write code yet.

### AI Suggestions

Claude proposed three visualization approaches:

1. Time-series comparison of predicted and ground-truth velocity, including prediction errors.
2. Error as a function of motion speed and acceleration.
3. Analysis of speed and direction errors.

Claude recommended starting with the time-series view to preserve temporal context and detect error peaks, possible lag, and systematic bias.

### Human Decision

We accepted the time-series recommendation because it provides a useful first view of model behavior and helps identify specific frames for further investigation.

We decided to investigate error versus speed and direction-dependent errors in subsequent analyses.

### Implementation

Claude created an interactive Altair visualization notebook:

`notebooks/phase1/01_velocity_timeseries.ipynb`

The visualization uses the saved predictions for `bot_beckman_5thfloor_1`, evaluated with the pretrained `main_0` Translation checkpoint.

The visualization contains:

- An overview of the velocity-error magnitude.
- Predicted and ground-truth velocity along the x-axis.
- Signed prediction error along the x-axis.
- Predicted and ground-truth velocity along the y-axis.
- Signed prediction error along the y-axis.
- Interactive zoom, hover information, and frame selection.

### Human Verification

We verified the following:

- The input contains 1,798 frames over approximately 59.9 seconds.
- The selected sequence belongs to the `main_0` test split.
- The prediction file was generated by the model on the Jetson GPU.
- The notebook executed successfully using Jupyter nbconvert on Windows.
- The local execution generated an HTML visualization.
- The generated HTML opened successfully in Chrome and displayed the velocity and error plots.

The original notebook initially failed inside VS Code with a Pandas DLL-loading error related to Windows application-control restrictions. Pandas imported successfully in PowerShell, so we executed the notebook outside the VS Code notebook interface.

### Initial Observations

**O1 — High-error interval**

A large disagreement appears near frames 546–559, approximately 18.2–18.6 seconds into the sequence.

Claude identified this interval as a possible ground-truth anomaly because the reference velocity changes unusually while the predicted velocity remains relatively stable.

We consider this an unverified hypothesis. The interval must be checked against the raw odometry data before assigning the error to the model or the reference signal.

**O2 — Stop-and-start motion**

The sequence contains repeated reductions in forward velocity to near zero. The predictions appear to follow these changes, although differences occur around some transitions.

This motivates a closer examination of response timing and transient error.

**O3 — Cruising behavior**

During periods of approximately steady forward motion, the predicted x-velocity appears smoother than the ground truth and sometimes remains near 0.25 m/s while the reference varies.

This suggests a possible speed-dependent prediction bias that should be tested quantitatively.

**O4 — Lateral velocity**

The y-velocity is generally much smaller than the forward x-velocity in this sequence. Both the ground truth and predictions fluctuate around relatively small values.

A comparison across additional sequences is needed before making general conclusions about lateral-motion accuracy.

**O5 — Individual low-error example**

At frame 738 (approximately 24.60 seconds), the visualization tooltip shows:

- Ground-truth vx: 0.265 m/s
- Predicted vx: 0.267 m/s
- Ground-truth vy: 0.020 m/s
- Predicted vy: 0.024 m/s
- Velocity-error magnitude: approximately 0.005 m/s

This provides one candidate low-error sample for later comparison with high-error radar heatmaps.

### Quantitative Results

| Metric | vx | vy |
|---|---:|---:|
| MAE (m/s) | 0.0484 | 0.0250 |
| RMSE (m/s) | 0.0667 | 0.0346 |

These values describe one held-out sequence and must not be interpreted as overall performance across the full Radarize dataset.

### Accepted, Modified, and Deferred Suggestions

**Accepted:** Interactive time-series visualization as the first Phase I analysis.

**Modified:** We treat the suspected ground-truth issue as a hypothesis rather than a confirmed explanation.

**Deferred:** Error-versus-speed analysis, verification of temporal lag, and investigation of additional sequences and platforms.

### Reflection

Claude was useful for proposing alternative visual representations, implementing the interactive chart, and identifying candidate patterns.

Human verification was essential for confirming that the visualization could be reproduced locally and for distinguishing observed disagreements from unverified causal explanations.

The first visualization has helped turn aggregate error metrics into more specific questions about motion transitions, speed-dependent bias, and reference-data quality.

### Artifacts

- `notebooks/phase1/01_velocity_timeseries.ipynb`
- `notebooks/phase1/01_velocity_timeseries_executed.ipynb`
- `results/phase1/main_0/bot_beckman_5thfloor_1_predictions.npz`
- `results/phase1/main_0/bot_beckman_5thfloor_1_timeseries.html`

**Status:** First visualization implemented and locally executed. Initial observations recorded; scientific validation and broader analysis ongoing.

### Independent Verification of Initial Observations

**Verification date:** November 7, 2026  
**Dataset:** `bot_beckman_5thfloor_1` — 1,798 frames, checkpoint `main_0`.

The initial observations suggested by Claude were checked quantitatively against the data embedded in the generated HTML visualization.

- **O1 — High-error interval:** Frames 546–559 (18.20–18.63 s) contain constant reference velocities of vx = -0.1183 and vy = -0.1450 m/s. Mean predicted vx is +0.2445 m/s. These 14 frames account for 23.1% of total squared vx error. This is a suspected reference-data anomaly, not a confirmed ground-truth failure.
- **O2 — Stops:** Predictions generally approach zero during stops. Across 46 frames with reference speed below 0.05 m/s, median predicted speed is 0.0276 m/s. Timing accuracy remains to be investigated.
- **O3 — Cruising:** During 51–58 s, mean true vx is 0.2847 m/s and mean predicted vx is 0.2196 m/s, giving a mean signed error of -0.0651 m/s. During 12–16 s, the mean signed error is +0.0440 m/s.
- **O4 — Lateral velocity:** The standard deviations of true and predicted vy are 0.0326 and 0.0153 m/s, respectively. Predictions are smoother, but this alone does not establish their physical accuracy.
- **O5 — Low-error frame:** Frame 738 (24.60 s) has a 2D velocity-error magnitude of approximately 0.0053 m/s.

**Human interpretation:** We accept the observed numerical patterns but do not yet accept causal explanations such as ground-truth failure, model smoothing, or speed-dependent bias as proven.

**Next investigation:** Visualize error versus speed and compare results with and without the suspected anomalous interval. Validate the reference signal and repeat the analysis on additional held-out sequences.

## AI-05 — Error vs. Speed Visualization
  
**Phase:** Phase I — Model Behavior Analysis

### 1. Objective

Investigate whether the Radarize Translation model's velocity prediction errors depend on motion speed, and examine the influence of the suspected ground-truth anomaly at frames 546–559.

### 2. Prompt Given to Claude

> Using our existing `bot_beckman_5thfloor_1` predictions, create an interactive Error vs. Speed visualization for Phase I.
>
> Show signed error and absolute error across speed ranges, and compare results with and without frames 546–559 (suspected GT anomaly). Use binned summaries to avoid overplotting.
>
> Save the notebook in `notebooks/phase1/` and generate an HTML output. Explain what the plot reveals, but don't assume the GT anomaly is confirmed.

### 3. AI Suggestions and Implementation

Claude developed an interactive Error vs. Speed visualization using Altair.

The visualization includes:

- Speed bins of 0.05 m/s.
- Signed forward velocity error (`vx`).
- Signed lateral velocity error (`vy`).
- Absolute velocity error.
- Median, mean, interquartile range, and 10–90% interval summaries.
- Comparison of all frames against results excluding frames 546–559.
- Interactive bin selection to inspect when errors occur in the time series.
- Alternative speed definitions for examining the robustness of observed patterns.

### 4. Initial Findings

**Speed-dependent bias:** Claude reported that the median forward prediction error changes from approximately +0.075 m/s at 0.15–0.20 m/s to −0.12 m/s at 0.35–0.40 m/s. This suggests overestimation at some lower speeds and underestimation at higher speeds.

**Absolute error:** Errors appear lowest around 0.20–0.30 m/s and increase toward the lower and higher ends of the observed speed range.

**Suspected ground-truth anomaly:** Excluding frames 546–559 changes the results mainly in the 0.15–0.20 m/s speed bin. The broader speed-dependent pattern appears to remain.

**Lateral velocity:** Claude reported relatively small median lateral prediction errors across speed bins.

These are initial findings from one test sequence and should not be generalized to other environments or platforms without further evaluation.

### 5. Human Verification and Decisions

We downloaded and saved the notebook and HTML visualization in the RadaVis repository.

We opened the HTML locally in Chrome and visually confirmed that the speed-bin plots, error summaries, and comparison groups are displayed.

We accepted the binned visualization because it makes systematic error patterns easier to inspect than a dense scatterplot.

We also accepted the comparison with and without the suspected anomalous frames as a sensitivity analysis.

However, we did not accept the claim that the ground-truth signal is faulty as a confirmed explanation. The underlying odometry and radar data require further investigation.

The second notebook has not yet been independently re-executed by the team, and the reported statistics still require independent numerical verification.

### 6. Reflection

Claude helped transform observations from the first time-series visualization into a more specific, testable research question.

The second visualization suggests that the model may predict velocity less accurately at some speeds and that the definition of motion speed can influence the interpretation.

The main limitation is that the analysis is based on only one robot sequence. Furthermore, correlation between prediction error and ground-truth speed does not establish the cause of the error.

Human judgment remains important for selecting meaningful comparisons, checking the model outputs, and avoiding unsupported conclusions.

### 7. Artifacts

- `notebooks/phase1/02_error_vs_speed.ipynb`
- `results/phase1/main_0/bot_beckman_5thfloor_1_error_vs_speed.html`
- `results/phase1/main_0/bot_beckman_5thfloor_1_predictions.npz`

### 8. Next Steps

1. Independently execute the second notebook and verify its reported statistics.
2. Investigate the suspected ground-truth anomaly using raw odometry data.
3. Repeat the analysis on additional held-out sequences.
4. Compare high-error and low-error radar heatmaps.

**Status:** Visualization implemented and inspected locally. Further numerical validation pending.

---

## Overall AI-Assisted Workflow Reflection

*To be completed after Phase I.*

### Benefits of AI Assistance

To be documented.

### Problems and Incorrect Suggestions

To be documented.

### Human Verification and Corrections

To be documented.

### Lessons for Future AI-Assisted Visualization

To be documented.

