# Tutorial #2 — Environmental Acoustic Intelligence
### From Acoustic Perception towards Context-Aware Sound Intervention
*EUSIPCO 2026 | W.S. Gan, E.L. Tan, J.W. Yeow*

---

## 0. Opening (Slides 1–11)
- Title, presenter introductions, lab overview (Smart Nation TRANS Lab @ NTU)
- **Framing: Hear → Understand → Reason → Act**
  - The four-stage arc: Perception → Contextual Understanding → Context-Aware Action → Purposeful Sound Intervention
- The Chinese character 聽 (听) as a metaphor for intelligent listening — parallel to agentic AI (observe → understand → reason → act)
- Copyright & disclaimer
- **Motivation:** why acoustics matters for smart cities (noise as pollutant + bio-indicator)
  - Health effects of noise (WHO ranking, non-auditory effects)
  - WHO noise guidelines for urban sound
  - Global use cases of smart acoustic sensing (NYC, Paris, Singapore, etc.)
  - Core challenges in environmental acoustic sensing (data scarcity, overlapping sources, real-time constraints)

---

## 1. Spatial Perception — Data-Centric AI for Acoustics (Slides 12–55)
*Speaker: J.W. Yeow*

### 1.1 Foundations of SELD
- Human listening as structured perception (identity–time–location binding)
- **What is SELD?** SED + DOA estimation → joint detection and localization
- Why SELD must be *joint* (association, not just detection + localization)
- Demo: monophonic SELD; early real-world deployment (residential IoT sensor)

### 1.2 The Supervised SELD Pipeline
- End-to-end framework: dataset → features → backbone → predictions → applications
- **Input formats:** FOA vs. MIC vs. Stereo — spatial cue trade-offs
- **Features:** spectral (WHAT) + spatial (WHERE); SALSA / SALSA-Lite
- **Neural backbones:** SELDNet (CRNN) → ResNet-Conformer → CST-Former (factorized attention)
- **Output representations:** Two-branch → ACCDOA → Multi-ACCDOA → Distance-extended (3-D SELD)
- **Evaluation:** joint detection + localization metrics (ER, F-score, LE, LR, RDE, SELD Error)
- SELD benchmarks over time: synthetic (2019–21) → real-world (2022–24) → stereo/video (2025)
- Recap: modern SELD as a chain of interdependent design choices

### 1.3 Label-Efficient / Data-Centric Learning
- Why SELD learning becomes data-centric (label dimensions grow: class → time → direction → distance)
- **Three routes to scalable supervision:**
  1. Synthetic scene generation (benefits vs. domain gap)
  2. Spatial self-supervised learning (invariance vs. equivariance; MC-SimCLR, w2v-SELD, source-aware SSL)
  3. Audio-visual correspondence (vision as training-time supervision)
- Long-tail class imbalance case study → **MAGENTA** (decoupled error + adaptive class weighting)
- Synthetic pretraining for reusable backbones (PSELDNets)

### 1.4 Language as an Interface to SELD
- Rise of Large Audio-Language Models (LALMs): Pengi, LTU, SALMONN → Qwen2-Audio → Kimi-Audio/Step-Audio
- Turning SELD into a queryable interface:
  - Open-vocabulary SELD (embed-ACCDOA)
  - Text-queried localization
  - Spatial question answering (BAT, SPUR)
- **Section recap:** Build Spatial Perception → Learn With Less Supervision → Add Language Interfaces

---

## 2. Contextual Understanding — From Acoustic Perception to Context-Aware Intelligence (Slides 56–79)
*Speaker: E.L. Tan*

### 2.1 The Three Perception Tasks
- ASC (scene) vs. SED (events) vs. SELD (events + location) — core questions, resolution, spatial requirement
- Datasets landscape for ASC / SED / SELD
- Worked example: urban street market (ASC + SED + SELD together)

### 2.2 Integrating ASC + SED
- **Architectural paradigms (increasing integration):**
  1. Parallel models (independent pipelines)
  2. Sequential models (one task conditions another) — historical evolution 2011–2015
  3. Multi-task learning (hard parameter sharing) + enhancements (soft scene labels, weak labels)
  4. Flexible/soft MTL (scene-conditioned loss, multi-focal loss, cooperative feature sharing)
- Architecture summary: independent → uni-directional → shared → dynamic interaction

### 2.3 Integrating ASC + SELD (Context-Aware Spatial Perception)
- From semantic information to contextual understanding (more info ≠ better understanding)
- **Use case:** ASC + SELD for hazard-aware situational awareness (wearables)
- Soft scene-conditioning of SELD models
- ASC as an enabling front-end component — must be accurate, robust, **lightweight**
- **DCASE Task 1** as the benchmark driving lightweight ASC research
- Case study: ultra-lightweight ASC model (Dilated Inception + Frequency Positional Encoding + Spatial Attention)
- **Section takeaways:** complementary tasks → integration evolution → contextual understanding enables action

---

## 3. Context-Aware Action, Part I — Active Noise Control (Slides 80–152)
*Largest technical section — organized around 4 core ANC challenges*

### 3.1 ANC Fundamentals
- Physics of destructive interference; feedforward digital ANC system design
- Commercial applications; ANC at source / propagation path / receiver
- Portable/distributed ANC (MOV-MFxLMS with penalty factor)
- Scaling to infrastructure: Active Soft Edge noise barriers
- **The Open-Window Paradox** (ventilation vs. noise in tropical cities)
- ANC windows: distributed vs. boundary actuator layouts, real prototypes, performance results

### 3.2 Key Challenges Motivating AI in Multi-Channel ANC
1. Nonlinearity
2. Slow adaptation
3. Acoustic-path variation
4. Generalization / online tracking
- Categorization of DNN roles in ANC; datasets for ANC research

### 3.3 (a) NN-Based Direct Anti-Noise Generation — *Challenge 1: Nonlinearity*
- Attentive Recurrent Network (ARN) — near-zero-latency time-domain control
- Deep Multi-Channel ANC (Deep MCANC)
- Adaptive WaveNet–VNN controller with online adapters (road noise)
- Remarks: advantages, limitations, deployment challenges, future directions

### 3.4 (b) NN-Based Control Filter Prediction — *Challenge 2: Slow Adaptation*
- Selective Fixed-Filter ANC (SFANC): Markov/HMM framing, CNN-based filter selection
- Field validation: non-stationary noise, university hostel deployment, real-time demo
- Transferable Latent SFANC (cross-system generalization)
- Frequency-Direction-aware Multichannel SFANC (integrating SELD into ANC)
- Dynamic/moving noise sources → co-forecasting with Bhattacharyya Distance Matrix + Dynamic Factor Graph
- Generative Fixed-Filter ANC (GFANC) — "ChatGPT for ANC" filter generation
  - GFANC-Bayes, Unsupervised-GFANC
- Reinforcement Learning-based SFANC / GFANC-RL
- Transformer-based end-to-end control filter generation
- Real-world adoption survey; remarks and trade-off summary

### 3.5 (c) NN-Based Acoustic Path Modelling — *Challenge 3: Path Variation*
- AI-assisted secondary path estimation via head tracking + PCA + DNN
- Head-Tracking Active Road Noise Control (HARNC) — virtual ear sensing
- Remarks: compression benefits vs. extrapolation/calibration limits

### 3.6 (d) NN-Based Adaptive Coordination (Hybrid) — *Challenge 4: Generalization*
- Hybrid SFANC–FxNLMS (fast selection + continuous adaptive refinement)
- Remarks: best-of-both-worlds performance vs. coordination complexity

---

## 4. Context-Aware Action, Part II — Soundscape Augmentation (Slides 153–162)
- Paradigm shift: beyond silence → **positive soundscapes** (ISO 12913)
- Sense → Analyse → Augment loop ("acoustic perfume")
- ARAUS dataset (affective response to augmented soundscapes) + related datasets
- Automatic Masker Selection System (AMSS) — feature-domain augmentation, probabilistic pleasantness prediction
- Cloud/IoT deployment (AWS) with real-time dashboard
- Multi-site in-situ evaluation — quality & restorativeness outcomes

---

## 5. Towards Intelligent Sound Management (Slides 163–186)
- AR/MR audio processing framework for hearables (sense, control, render)
- **oPEAR**: intelligent open-ear smart glasses research thrusts
  - **(A)** Direction-Preserving ANC via FiLM-conditioned control filter estimation
  - **(B)** ANC for open-ear smart glasses (no in-ear mic → virtual sensing, U-Net filter estimation)
  - **(C)** Semantic Hearing — class-conditioned target sound extraction/suppression; integration with ANC
  - **(D)** Sound Bubble — programmable personal listening-zone hearables
  - **(E)** Biosensing in hearables — physiological/emotional state sensing for human-aware intervention

---

## 6. Conclusions and New Research Activities (Slides 187–191)
- **Capability Ladder for Active Sound Intervention (ASI):**
  Physical Layer → Acoustic/Spatial Features → Semantic Understanding → Context-Aware Decision → Human-Aware & Adaptive
- Unified dual-rate framework: fast **Perceive→Act** control loop + slower **Intelligence & Adaptation** plane (ASC/SELD, human feedback, continual learning)
- Closing message: **"Listen with Understanding and Act with Purpose"**

---

## High-Level Arc (One-Line Summary)

```
Perception (SELD)  →  Integration (ASC+SED+SELD → Context)  →  Action
                                                                  ├── Active Noise Control
                                                                  ├── Soundscape Augmentation
                                                                  └── Intelligent Sound Management (hearables)
        ↓ underpinned throughout by:
   Label-efficient / data-centric learning  +  Language interfaces  +  Human/context awareness
```
