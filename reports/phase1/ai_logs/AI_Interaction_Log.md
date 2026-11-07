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



## AI-04 — Visualization Design Exploration

**Objective:** Explore visualizations for understanding Translation model errors.

**AI Suggestions:** Time-series comparison, error versus motion, and speed/direction error analysis.

**Human Decision:** Selected the time-series view as the first visualization because it preserves temporal context and helps identify possible lag, bias, and error peaks.

**Deferred:** Motion-dependent and direction-dependent analyses until the first visualization is inspected.

**Reflection:** Claude helped compare design alternatives. We retained control over the choice and will verify all interpretations against actual model outputs.

**Status:** Design selected; implementation pending.

AI-04b — Time-series visualization execution
Objective: Execute the Phase I time-series notebook on the real prediction output and generate a shareable HTML visualization.

AI Suggestion: Use the notebook to render an interactive HTML chart showing vx, vy, and their signed errors over time. Keep the preview HTML only as a reference and use the locally generated HTML as the official result.

Human Action: Installed Altair in the local RadaVis environment, executed the notebook with jupyter nbconvert, and confirmed that the HTML output was created successfully.

Artifacts produced:
- notebooks/phase1/01_velocity_timeseries_executed.ipynb
- results/phase1/main_0/bot_beckman_5thfloor_1_timeseries.html
- results/phase1/main_0/bot_beckman_5thfloor_1_predictions.npz
Result: The visualization was generated successfully. Both prediction and ground-truth velocity can now be inspected over time, together with signed error.

Reflection: Running the notebook locally was more reliable than using the VS Code notebook UI on Windows, which was affected by environment/security issues. The HTML export is a stable way to inspect the visualization without depending on notebook execution inside the editor.

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

