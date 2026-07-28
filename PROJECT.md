# PROJECT.md: The Quantitative Energy & Grid Flexibility Research Manifesto

**Status:** Universal Master Framework & Engineering Constitution  
**Purpose:** Define the research logic, modelling discipline, programming standards, and communication guardrails for all quantitative energy, grid flexibility, and data science projects.

**Core Philosophy:** *Physical reality and auditable math always trump software illusions. We do not build analytical black boxes. We build transparent, reproducible, and physically grounded frameworks.*

---

# Part 1 — Project Definition & Scoping

## 1. The Project Definition Template
Every project must begin by explicitly defining its scope, avoiding the trap of solving every problem at once. 

1. **The Core Thesis:** A single, punchy sentence defining the gap between theory and physical reality (e.g., *"Installed capacity is visible; tenant-safe flexibility is not."*).
2. **The Empirical Deliverability Question:** Do not ask if a concept exists in theory. Ask if the physical assets can *actually deliver* the required service when real-world constraints, consumer behaviour, and hardware limits are applied.
3. **The Boundary of the Model:** Explicitly state what the model *does not* do. (e.g., *"This model evaluates constraint-event locational revenue only, not total battery arbitrage or capacity market revenue."*)

---

# Part 2 — Research Philosophy

## 2. The Golden Heuristics
These are non-negotiable rules for all modelling, simulation, and analytical work.

### 2.1 Physics Before Economics
Physical feasibility and system need must be established before economic conclusions are drawn. Do not jump directly to NPV, revenue sufficiency, or market design before establishing the physical and technological logic. 
*Always begin with: What is constrained? Where? Which direction is power flowing? Can the asset physically perform the action?*

### 2.2 The 'Sledgehammer' Test (Simple Before Complex)
Use the simplest credible method that answers the question. Before implementing advanced algorithms (e.g., GANs, MCMC, MILP, Reinforcement Learning), ask: *"Can a simple, auditable, rule-based or multiplicative model answer the core question?"* If yes, the simple model must be used. Complexity is only justified if it solves a specific, documented gap that the simple model cannot address. We do not use math to dress up simple concepts.

### 2.3 The Physics/Derating Separation (No Double-Counting)
Internal physical constraints (e.g., tenant reserve floors, concurrent heat-pump load, base inverter efficiency) must be modeled directly within the core simulation ($P_{simulated}$). Post-hoc derating multipliers ($\eta$) are strictly reserved for external network, operational, or behavioral frictions. Applying a "baseline load" multiplier on top of a simulation that already models tenant reserve floors is a critical methodological error that artificially crushes flexibility estimates.

### 2.4 The Anti-Correlation Stress Test
Any flexibility, reliability, or risk model must include a "worst-case correlation" scenario (e.g., fleet availability dropping exactly when grid need peaks, or opt-outs rising during extreme weather). If a model only tests average conditions, it is over-promising and will fail in the real world.

### 2.5 Time Flows Forwards (Zero Look-Ahead Bias)
No variable, feature, or model input may use information unavailable at the decision timestamp. For historical simulations, explicitly state what would and would not have been known at the relevant decision point. Strict temporal train/test splits are mandatory. Random K-fold cross-validation is forbidden for time-series/grid data.

### 2.6 Mechanism Before Model
Every model result must be attached to a physical or economic mechanism. Use the project loop: *Model result → discomfort → mechanism → sensitivity → policy lever → caveat*. A model that cannot explain the sign of the effect is not ready for policy use.

### 2.7 Ambiguity Is Informative
Treat uncertainty as a signal that understanding is incomplete. Do not force interpretations before sufficient evidence exists. If the data does not clearly separate winter import stress from summer export stress, that is a result, not a failure.

---

# Part 3 — Analytical Design

## 3. The Universal 6-Stage Pipeline
Every analytical project must follow this logical progression. Do not skip stages.

### Stage A: Empirical Ground Truth
Build the empirical event log or raw data foundation. This is the ground truth for all later modelling. Preserve empirical correlation between variables. Do not use synthetic data before building the empirical register.

### Stage B: Temporal & Distributional Analysis
Characterise the data by time, season, duration, and severity. Identify the physical regimes (e.g., winter import stress vs. summer export stress). 

### Stage C: Physical / Synthetic Asset Modelling
Model the physical assets (e.g., VPP fleet, battery portfolio). 
*   **Crucial Distinction:** Do not treat different seasonal services as equivalent (e.g., winter discharge capacity vs. summer charging headroom). 
*   **Chemistry & Hardware:** Explicitly model hardware differences (e.g., LFP thermal throttling vs. NGA/LTO resilience) if relevant to the physical outcome.

### Stage D: Dispatch & Scenario Modelling
Run multiple scenarios on the same synthetic fleet so differences are attributable to dispatch rules rather than portfolio composition.
1.  **Baseline/Naive:** What does the market/consumer naturally do?
2.  **Theoretical Ceiling:** Perfect constraint-aware dispatch (no consumer constraints).
3.  **The Realistic Hybrid (Central Case):** Overlay constraint awareness on consumer/physical behaviour (reserve floors, opt-outs, inverter limits).
4.  **The Anti-Correlation Stress Test:** The "Day 4 Cold Spell" scenario where physical and behavioural limits collide.

### Stage E: Value Gap & Derating Framework
Calculate the gap between theoretical value and real-world delivery. Use the multiplicative derating equation for real-world capability:
$$P_{effective} = P_{simulated} \times (\eta_{thermal} \times \eta_{phase} \times \eta_{comms} \times \eta_{primacy})$$
*Never double-count internal physics here.*

### Stage F: Monte Carlo & Uncertainty Propagation
Monte Carlo is used where uncertainty is real (the realistic hybrid scenario). 
*   **Rule:** Simple vectorized Monte Carlo (e.g., NumPy) is the primary uncertainty framework. Do not use MCMC unless solving a complex Bayesian inverse problem. 
*   **Output:** Always calculate and report the **P10, P50, and P90** distributional forms, not just point estimates.

## Analytical Principles: Feynman Approaches

This project applies Richard Feynman's analytical methods to energy policy and AI infrastructure modelling. These principles guide every stage of the framework:

### 1. "The first principle is that you must not fool yourself—and you are the easiest person to fool."
**Application:** We built an adversarial review process specifically to catch our own blind spots. Every assumption is documented, every number is traceable, and we explicitly invite external reviewers to falsify our findings. The "Timescale Mismatch Trap" only has credibility because we subjected it to rigorous pre-publication scrutiny.

### 2. "What I cannot create, I do not understand."
**Application:** We don't just cite "50% flexibility" claims—we built the entire physical model from first principles to understand what that number actually means. The model forces us to confront the physics: checkpointing times, grid event durations, schedulable fractions. If we can't build it, we can't claim to understand it.

### 3. "Knowing the name of something is not the same as knowing something."
**Application:** We don't just label AI workloads as "flexible"—we decompose that flexibility into physical mechanisms: How long does checkpointing take? What's the orchestration overhead? What's the restart verification time? The name "flexibility" is meaningless without the underlying physics.

### 4. "For a successful technology, reality must take precedence over public relations, for nature cannot be fooled."
**Application:** Data centre developers can claim "50% flexibility" in press releases, but the grid doesn't care about PR. If the IT checkpointing timescale exceeds the grid event duration, the flexibility doesn't materialise. Nature (physics) cannot be fooled by marketing. Our model exposes this gap between claim and reality.

### 5. "I would rather have questions that can't be answered than answers that can't be questioned."
**Application:** We explicitly state what we don't know: the 12-hour IT notice is a "conservative engineering estimate" not yet decomposed per-stage; the 50% curtailment proxy is UK-wide, not Scottish-specific; battery storage interactions are deferred to Stage 3. These open questions are more valuable than false certainty.

### 6. "The Feynman Technique": Explain it simply.
**Application:** Every chart, policy brief, and LinkedIn post is written in plain English. The "sprint vs marathon" analogy makes the timescale mismatch intuitive to non-technical readers. If we can't explain it to a planner or policymaker in one breath, we don't understand it well enough to model it.

### 7. "Shut up and calculate."
**Application:** Sometimes the best response to a complex policy debate is to just run the numbers. The adversarial review kit's stress test script does exactly this: it loads the data, runs the calculation, and prints the result. No hand-waving, no opinion—just the math.

### 8. Distinguish between "map" and "territory."
**Application:** Our model is a map, not the territory. The 50% curtailment proxy is a first-order approximation, not a perfect representation of Scottish constraint events. Stage 2 replaces the map with better data. We never confuse the model with reality—we use the model to understand where reality is different from our assumptions.

---

**How these principles shape the project:**
- Every assumption is documented and falsifiable
- Every number is traceable to a physical mechanism or data source
- Every limitation is stated upfront, not hidden
- Every claim is scoped honestly (worst-case stress test, not "realistic")
- Every generalisation is hedged appropriately
- Every model output is checked against independent reality

This is not just a technical framework—it's a discipline of thought.

---

# Part 4 — Engineering & Programming Discipline

## 4. The Modern Stack & Environment Rules
*   **Environment Management:** `uv` is strictly enforced for speed and reproducibility.
*   **Dataframes:** Polars is strictly enforced over Pandas for performance, lazy evaluation, and strict schema validation.
*   **Math/Simulation:** NumPy (vectorized operations), SciPy (distributions).
*   **Visualization:** Matplotlib (publication-ready).

### 4.1 Environment Locking & Isolation
All notebooks must be executed via the project-specific virtual environment (e.g., `uv run jupyter lab` from the project root). Cross-project kernel usage is strictly prohibited. The first cell of every notebook must verify the active Python executable path to prevent dependency collisions.

### 4.2 The Parquet Handoff Rule
Notebooks must not pass massive dataframes in memory across different logical stages. Projects must be split into a minimum of 4 modular notebooks. Each notebook must save its output to `data/intermediate/*.parquet` and the subsequent notebook must read from it.

### 4.3 Polars Quirks & Gotchas
*   **No `.item()` needed:** In modern Polars, aggregations like `.sum()`, `.mean()`, and `.quantile()` return native Python floats. Do not append `.item()`.
*   **Parallel Evaluation:** `.with_columns()` evaluates expressions in parallel. You cannot reference a column alias created in the same `.with_columns()` block. Do the math directly inside the `.then()` statement.

## 5. NASA/JPL-Inspired Coding Standards
The project follows a Python/data-science adaptation of the NASA/JPL “Power of Ten” discipline. *Make wrong results hard to produce silently.*

1.  **Small Functions, Clear Contracts:** Each function does one thing. No hidden global state.
2.  **Assertions Protect Physics:** Use assertions to check physical boundaries (e.g., `assert 0 <= soc <= 1`, `assert discharge_mwh <= available_mwh`).
3.  **Fail Loudly:** No silent failures. No broad `except: pass`. Re-raise errors with context.
4.  **Schema Before Analysis:** Each major intermediate dataset needs an explicit schema (column name, type, unit, allowed range).
5.  **Deterministic Baseline Before Randomness:** Before running 10,000 Monte Carlo iterations, run one transparent, deterministic example to explain the mechanism.
6.  **Configuration, Not Magic Numbers:** Material assumptions belong in configuration files or explicitly named variables at the top of the script, not buried in logic.
7.  **Warnings Are Evidence:** Do not suppress warnings globally. Fix them or document why they are harmless.

---

# Part 5 — Communication, Traceability, & Reporting

## 6. The Traceability Mandate
Every headline metric in the final output must be reproducible via a documented, row-by-row traceability table mapping specific input assumptions to final outputs. If a reviewer cannot reproduce your headline number in a spreadsheet in under 60 seconds using your documented inputs, the model is a black box and is rejected.

## 7. Translate to Physical Units
Percentages are for data scientists; Megawatts (MW) and £/MWh are for grid operators and traders. Every headline percentage must be accompanied by its physical MW or financial equivalent for the target scale.

## 8. Writing Principles: Strunk & White, Zinsser, and the Human Voice

### 8.1 Strunk & White — Precision Through Constraint
Omit needless words. Every word must earn its place. If it can be removed without losing meaning, remove it.
Use the active voice. "The model calculates flexibility" not "Flexibility is calculated by the model."
Put statements in positive form. Say what is, not what is not. "The battery discharges" not "The battery does not charge."
Use definite, specific, concrete language. Avoid vague qualifiers (rather, very, little, pretty, somewhat). Say "3.5%" not "approximately 3-4%."
Do not overstate. Avoid superlatives unless mathematically justified. "Significant" means statistically significant, not "big."
Be clear. If a sentence requires re-reading, rewrite it. Technical writing is not a puzzle.

### 8.2 Zinsser — Humanity in Technical Prose
Clarity is the foundation. Clear thinking becomes clear writing. If your explanation is muddy, your understanding is incomplete.
Cut clutter. Every extra word is a tax on the reader's attention. Fight for every word you keep.
Write for the reader, not for yourself. The reader has an attention span of about 30 seconds. Earn it. Respect it.
Use active verbs. "The fleet delivers 5 MW" not "5 MW is delivered by the fleet."
Be yourself. Technical writing can still sound human. Do not hide behind jargon or passive constructions.
Simplify, simplify, simplify. Complexity in the subject matter does not require complexity in the explanation.

### 8.3 Modelling Prose — The Standard Pattern
Every major claim in the README or policy summary must have:
Number (the quantitative result)
Unit (MW, MWh, %, £)
Denominator (what is this relative to?)
Mechanism (why does this happen?)
Scope boundary (what does this not cover?)
Caveat (what could make this wrong?)
Example:
"A 50 MWh VPP offsets 12% of winter constraint-event MWh under Scenario 4 assumptions (P10: 8%, P50: 12%, P90: 15%), because price-led evening discharge partially aligns with import-stress periods. This does not imply equivalent summer value, where charging headroom rather than discharge capacity is the relevant service. The 12% figure assumes 30% tenant opt-out during cold spells; if opt-outs rise to 40%, deliverability falls to 9%."

## 9. Visual Design Principles: Tufte's Standards for Analytical Graphics

### 9.1 Maximize the Data-Ink Ratio
Every pixel must convey information. Decorative gridlines, 3D effects, drop shadows, and ornamental borders are chartjunk. Delete them.
Erase non-data ink. If removing an element does not reduce understanding, remove it.
Erase redundant data ink. Do not show the same data twice in different forms unless the comparison is essential.

### 9.2 Show the Data, Not the Decoration
Avoid chartjunk: No pie charts (unless part-to-whole is essential), no 3D bars, no decorative icons, no gradient fills without meaning.
Label directly. Place labels on or near the data, not in a legend that forces eye-travel.
Use small multiples. When comparing scenarios or time periods, use a series of small, identical charts rather than one overloaded chart.

### 9.3 Show Causation, Comparison, and Context
Always show the denominator. A percentage without its base is meaningless. "3.5% of 150 MW" not just "3.5%."
Integrate text and graphics. The caption should explain the takeaway, not just describe the axes.
Show causation where possible. Use annotations to mark events, thresholds, or regime changes. "Cold spell begins here" → arrow on timeline.

### 9.4 Use Appropriate Scales and Proportions
Do not distort the data. The y-axis should start at zero unless there is a specific, justified reason not to. If you truncate, mark it clearly.
Use aspect ratios that reveal structure. A time-series should have enough horizontal space to show trends, not compress them into noise.
Show uncertainty when it changes the decision. Error bars, confidence bands, or P10/P90 shading should be included when the uncertainty range affects the policy conclusion.

### 9.5 The Tufte Checklist for Every Plot
Before including a chart, verify:
Does it answer one clear question?
Is every pixel necessary?
Are units visible on axes?
Is the denominator shown?
Are labels direct (not in a distant legend)?
Is the sample period stated?
Is the data source cited?
Does the caption explain the takeaway, not just the axes?
Would a table be clearer? (If yes, use a table.)

### 9.6 Preferred Plot Types for Energy Analysis
Event-frequency heatmaps (settlement period × month)
Duration distributions (histogram or ECDF)
Winter/summer comparison bars (grouped or small multiples)
Scenario 1–4 value comparison (grouped bars with error bands)
Monte Carlo percentile bands (P10/P50/P90 shaded area)
Event severity versus deliverability scatter (with regression or trend line)
Time-series with annotations (marking constraint events, cold spells, opt-out spikes)

### 9.7 Forbidden Visualizations
Pie charts (unless showing a strict part-to-whole relationship)
3D bars or surfaces (distort perception)
Overloaded multi-axis charts (confuse causation)
Decorative dashboards (style over substance)
Plots without units
Plots where the denominator is unclear
"Waterfall" charts that hide negative values

## 10. The README Standard

Every repository must have a README.md that includes:
The Core Thesis (one sentence).
The Traceability Table (Inputs 
→
→ Outputs).
Explicit documentation of the "No Double-Counting" rule.
A "Limitations & Future Work" section that honestly addresses what the model doesn't do.
At least one Tufte-compliant figure that shows the key result.

## 11. External Communication (LinkedIn / Briefings)
Timing: Tuesday or Wednesday, 8:00 AM – 9:30 AM (UK Time).
Link Placement: GitHub link in the first comment, not the main post body (to avoid algorithmic suppression).
Visuals: Attach one high-quality, Tufte-compliant chart directly to the post. No decorative elements. Show the data.
Tone: Confident but humble. Acknowledge the physical limitations of the model. Pre-empt expert critiques by addressing them in the text (e.g., "Note: These figures represent constraint-event revenue only...").
Writing Style: Apply Strunk & White and Zinsser. Omit needless words. Use active voice. Cut clutter. Be clear.
The "Build in Public" Pivot: If a highly technical post fails to gain traction, pivot to a "Lessons Learned" or "Contrarian Take" angle (e.g., "Why we scrapped a complex GAN for a simple multiplicative derating equation").


# Part 6 — Forbidden Shortcuts & Known Risks

## 12. Forbidden Shortcuts
Do not:
*   Use synthetic data before building the empirical event register.
*   Apply a generic "efficiency loss" multiplier on top of a simulation that already models the underlying physics (Double-Counting).
*   Use MCMC, GANs, or MILP when a simple Monte Carlo or rule-based dispatcher answers the question (Math-Washing).
*   Treat summer charging-headroom value as equivalent to winter discharge capacity.
*   Condition on post-event outcomes in a predictive model.
*   Hide material assumptions inside notebook cells.
*   Claim locational value without an event-level counterfactual.

## 13. Known Risks & Mitigations
*   **Risk:** Public data may not reveal distribution-level constraints. *Mitigation:* Report transmission-level value separately from distribution-level inferred value.
*   **Risk:** Household reserve behaviour may dominate technical capacity. *Mitigation:* Model the tenant reserve floor explicitly and run the Anti-Correlation Stress Test.
*   **Risk:** Synthetic fleet assumptions may overstate coordinated response. *Mitigation:* Apply strict derating factors ($\eta_{phase}$, $\eta_{comms}$) and report P10/P50/P90 distributions.

---

# Part 7 — The Final Discipline

Do not let the model become clever before the mechanism becomes clear.

The project order is:Physics → Event Register → Mechanism → Scenario Model → Sensitivity → Monte Carlo → Policy Lever → Caveat

**The Final Project Loop:**

Model result → discomfort → mechanism → sensitivity → policy lever → caveat

---

# Part 8 — Current Project Application: Scotland AI Split-Zones (Stage 2)

This section applies the Manifesto's principles to the immediate next phase of the Scotland AI Split-Zones project: replacing the conservative 50% curtailment proxy with empirical NESO constraint data.

## Stage 2 Milestones: The Scottish Reality Upgrade

### Milestone 2.1: Reconciliation Spike (In Progress)
*Applies: Mechanism Before Model, Fail Loudly, Configuration Not Magic Numbers*
- [ ] Identify correct CKAN resource ID for NESO Constraint Breakdown dataset.
- [ ] Pull one sample year of data and verify schema.
- [ ] Confirm boundary column presence and distinct `SCOTEX` / `SSEN-S` values.
- [ ] Check for the 22 April 2024 methodology break and flag if data is non-comparable.
- [ ] Sanity-check Thermal-category volume magnitude against independent published reports.
- [ ] **Decision Gate:** If data is a system-wide aggregate with no boundary breakdown, halt pipeline construction and initiate Milestone 2.1b (BOALF join).

### Milestone 2.2: Scottish Event Profiler
*Applies: Temporal & Distributional Analysis, Translate to Physical Units*
- [ ] Calculate actual average duration of Scottish export constraint events.
- [ ] Replace UK-wide statistics ("68% <4 hours") with Scottish-specific, boundary-level data.
- [ ] Update policy briefs with empirically grounded duration distributions.

### Milestone 2.3: IT Notice Decomposition
*Applies: Physics Before Economics, Ambiguity Is Informative*
- [ ] Research per-stage checkpointing times from hyperscaler documentation (Azure, Google, etc.).
- [ ] Update `configs/workload_flexibility_assumptions.yml` with a structured, multi-stage notice model.
- [ ] Replace the current "conservative engineering estimate" with a decomposed, evidence-based breakdown (e.g., checkpoint + orchestration + protocol + verification + safety margin).

### Milestone 2.4: Economic Layer
*Applies: Traceability Mandate, Translate to Physical Units*
- [ ] Pin constraint cost proxy (£/MWh) from official NESO publications.
- [ ] Calculate the annual financial cost of the timescale mismatch for Scottish consumers.
- [ ] Update policy outputs to show both the physical MW loss and the financial £ impact.

## Stage 2 Explicit Guardrails
1. **No building before data contracts are defined.** The ingestion pipeline will not be written until the Reconciliation Spike confirms the schema.
2. **Precise NESO terminology only.** Target boundaries are `SCOTEX` (B6) and `SSEN-S` (B2). Asset names (e.g., "Caithness-Moray") are for commentary only, not query keys.
3. **NKILGRMO is explicitly excluded** due to poor tracking of its notional boundary. This is a documented design choice, not a silent omission.

## Part 9 - Project Specification

## 1. What this project is / is not

### This project is

A constraint-direction siting framework for AI compute in Scotland.

It asks whether different AI workloads should be separated into training, inference, batch and edge categories, then sited according to grid function:

- flexible training near renewable-surplus, export-constrained zones;
- latency-sensitive inference near users, fibre and public-service demand;
- batch inference where limited scheduling flexibility can reduce system stress;
- tenant-safe VPPs as event-time support layers, not baseload substitutes.

### This project is not

- It is not a claim that domestic VPPs can power hyperscale data centres.
- It is not a generic "green data centre" pitch.
- It is not a vendor-specific Tesla, Powerwall or Autobidder study.
- It is not an assumption that AI training jobs can be interrupted every settlement period.
- It is not an argument that AI load "solves" transmission constraints. In export-constrained zones, the constraint remains; flexible demand may reduce curtailment and economic waste by consuming renewable power that the grid cannot otherwise move.
- It is not a bet on static compute intensity. It explicitly accounts for technological velocity risk: algorithmic efficiency gains (e.g., Mixture-of-Experts, FP8 quantization, architectural light-weighting) can slash MW demand faster than 20-year grid assets depreciate.

## 2. Workload split

The project distinguishes AI workloads by their grid behaviour.

| Workload type | Grid behaviour | Likely siting logic | Baseline flexibility assumption |
|---|---|---|---|
| Large-model training | High power demand; long-running; potentially schedulable at job level | Renewable-rich/export-constrained zones | Schedulable at start/stop level, not freely interruptible |
| Real-time inference | Latency-sensitive; service-level driven | Lowlands, fibre routes, users, public services | Mostly inflexible |
| Batch inference | Queueable; partly shiftable | Could follow grid-aware scheduling | Shiftable within limited window |
| Edge AI | Smaller, localised, service-specific | Near operational need | Case-specific |

## 3. Site typology

| Site type | Grid condition | Best AI workload | Main metric |
|---|---|---|---|
| Export-constrained renewable-surplus zone | Local generation exceeds export capability | Flexible training | Avoided curtailment / renewable absorption |
| Import-constrained Lowlands site | New demand may worsen local grid stress | Inference / smaller clusters | Residual grid burden |
| Balanced industrial zone | Some grid access, but strategic load still matters | Mixed compute | Net grid impact |
| VPP-rich community zone | Distributed flexibility available | Inference / support services | Event-time flexibility support |

## 4. Policy questions

The project is about strategic demand connection design, not just data centres.

**Questions for policy:**

- Should Scotland distinguish between AI training and inference in planning policy?
- Should AI Growth Zones be assessed by residual grid burden, not just investment and jobs?
- Should flexible training load receive faster connection where it absorbs curtailed renewables?
- Should hyperscale Lowlands data centres face stronger tests on power, water and local grid impact?
- Could verified flexible demand be treated as a constraint-management asset?
- Should data-centre developers be required to show workload flexibility and grid-response capability?
- Can tenant-safe VPP support be accredited as part of strategic demand connection planning?
- Should public benefit tests include heat reuse, community value, water stewardship and local energy impact?
- Should data centre connection agreements in import-constrained zones require phased, non-firm, or flexible connections to protect ratepayers from stranded network asset risk?
- How should Scottish planning policy balance the risk of speculative queue-hoarding against genuine, flexible renewable-absorption demand?

**Challenging questions the framework does not resolve:**
- Should Scotland be cautious about overbuilding AI training capacity that may become obsolete within 5–10 years, given the pace of algorithmic efficiency gains (Mixture-of-Experts, FP8 quantization, architectural light-weighting)?
- Could diverting AI training to remote export-constrained sites undermine Scotland's AI services economy, which benefits from proximity to users, universities, and enterprise demand in the Central Belt?
- Are there better uses for curtailed renewable energy than AI training (e.g., green hydrogen production, industrial electrification, grid-scale storage) that deliver more durable economic or decarbonisation value per MWh?
- If flexible AI training proves economically unviable due to operator friction costs, should export-constrained zones instead pursue direct renewable-to-industry connections (e.g., data centres co-located with wind farms via private wire) rather than relying on Balancing Mechanism dispatch?

## 5. Definition of Done

### Stage 1 MVP ✅ COMPLETE
- [x] `configs/data_sources.yml` populated and source vintages recorded
- [x] Candidate Scottish AI sites classified by constraint direction
- [x] Workload assumptions config-driven and validated
- [x] Duration Compatibility Factor implemented
- [x] Import-constrained residual grid burden calculated
- [x] Export-constrained renewable absorption calculated using `site_connection_capacity_mw`
- [x] No monetary curtailment result published without pinned value proxy
- [x] Site scorecard reproducible from clean execution
- [x] All core assumptions visible in config files
- [x] README and PROJECT.md state what the model does **not** prove

### Stage 2: Scottish Reality Upgrade ✅ COMPLETE
- [x] Empirical constraint event register built and duration distributions calculated (SCOTEX median: 2.0h, SSEN-S median: 1.5h)
- [x] IT notice period decomposed into per-stage components (~0.93h total, hyperscaler lower bound)
- [x] Duration Compatibility Factor updated to 1.0 for median events
- [x] Defensible constraint volume proxy calculated (3.01 TWh for Scotland via cost-proportion method)
- [x] Empirical constraint cost proxy pinned (£164.89/MWh average)
- [x] Theoretical maximum addressable market identified (£495.7M/year)
- [x] AI-side friction costs and symmetric stranded-asset risks explicitly documented
- [x] Tufte-compliant visualizations produced (4 figures)
- [x] README updated with empirical findings and strict caveats

### Stage 3: Battery Storage Interaction (Planned)
- [ ] Model co-located battery storage dispatch
- [ ] Evaluate IT checkpointing + battery hybrid strategies
- [ ] Quantify additional flexibility from storage-backed AI sites

## 6. Notebook plan

### Notebook 01 — `01_site_register_and_typology.ipynb`

Purpose:

- build candidate site register;
- classify site by constraint direction;
- assign candidate workload suitability;
- produce initial Scotland site typology.

Outputs:

- `candidate_site_register.parquet`;
- `site_typology_summary.csv`;
- `figures/scotland_site_typology_map.png`.

### Notebook 02 — `02_workload_response_curves.ipynb`

Purpose:

- read `workload_flexibility_assumptions.yml`;
- generate flexible-load response curves;
- compare schedulable fractions;
- compare notice periods;
- compare event durations.

Outputs:

- `outputs/workload_response_sensitivity.csv`;
- `figures/workload_response_by_notice_period.png`.

### Notebook 03 — `03_residual_grid_burden_model.ipynb`

Purpose:

- evaluate import-dependent sites;
- calculate residual grid burden under workload/VPP/storage assumptions;
- test sensitivity to load size and flexibility assumptions.

Outputs:

- `outputs/residual_grid_burden_by_site.csv`;
- `figures/residual_grid_burden_chart.png`.

### Notebook 04 — `04_renewable_absorption_model.ipynb`

Purpose:

- evaluate export-constrained renewable-surplus sites;
- estimate absorbable curtailed renewable energy;
- apply site connection capacity proxy;
- defer monetary value until curtailment proxy is pinned.

Outputs:

- `outputs/renewable_absorption_by_site.csv`;
- `figures/renewable_absorption_potential.png`.

### Notebook 05 — `05_site_scorecard.ipynb`

Purpose:

- combine site typology, workload suitability, grid burden and absorption metrics;
- produce public-facing site scorecard;
- identify candidate sites for Stage 2 modelling.

Outputs:

- `outputs/site_scorecard.csv`;
- `figures/site_scorecard.png`.

## 7. References and source anchors

The project specification is designed around public, auditable sources. Source URLs should be pinned in `configs/data_sources.yml` before analysis.

Initial source anchors:

- UK Government — AI Growth Zones open for applications: https://www.gov.uk/government/publications/ai-growth-zones/ai-growth-zones-open-for-applications
- UK Government — Delivering AI Growth Zones: https://www.gov.uk/government/publications/delivering-ai-growth-zones/delivering-ai-growth-zones
- Scottish Government — Scotland's Artificial Intelligence Strategy 2026-2031: https://www.gov.scot/publications/scotlands-ai-strategy-2026-2031/
- Scottish Government — AI Strategy Actions: https://www.gov.scot/publications/scotlands-ai-strategy-2026-2031/pages/6/
- UK Parliament Written Statement HCWS1289 — Lanarkshire AI Growth Zone: https://questions-statements.parliament.uk/written-statements/detail/2026-01-29/hcws1289
- DataVita — Lanarkshire AI Growth Zone FAQs: https://www.datavita.co.uk/lanarkshire-ai-growth-zone/faqs
- NESO — Local Constraint Market: https://www.neso.energy/industry-information/balancing-services/local-constraint-market
- NESO — Constraint Management Intertrip Service: https://www.neso.energy/industry-information/balancing-services/network-services/constraint-management-intertrip-service
- NESO — Day Ahead Constraint Flows and Limits: https://www.neso.energy/data-portal/day-ahead-constraint-flows-and-limits
- NESO — Connections Reform Results: https://www.neso.energy/industry-information/connections-reform/connections-reform-results
- Ofgem — Demand Connections Reform: https://www.ofgem.gov.uk/call-for-input/demand-connections-reform
- DESNZ / data.gov.uk — Renewable Energy Planning Database: https://www.gov.uk/government/publications/renewable-energy-planning-database-quarterly-extract
- Ofcom — Connected Nations: https://www.ofcom.org.uk/research-and-data/multi-sector-research/infrastructure-research/connected-nations
- Williams et al. — Power-Flexible AI Data Centers: https://arxiv.org/abs/2606.25098

## 8 The "Plain English" Translation Guide

Translation matrix by audience

| Audience | Technical Term (Internal/Repo) | Plain English Translation (Public/Policy) |
| :--- | :--- | :--- |
| **Grid Engineers / Academics** | Constraint-Direction Computing | "Classifying compute workloads by whether they add to import pressure or absorb export curtailment." |
| **Government Ministers / Policymakers** | Export-Constrained Renewable Absorption | "Putting flexible AI training where the wind is blowing but the wires are full, turning wasted energy into an economic asset." |
| **Government Ministers / Policymakers** | Import-Constrained Residual Grid Burden | "Ensuring new AI data centres in the Lowlands don't overload local grids or drive up bills for existing residents and businesses." |
| **Journalists / General Public** | Duration Compatibility Factor | "Making sure the AI can actually pause and restart fast enough to match how long the grid constraint lasts." |
| **Journalists / General Public** | AI-Operator Friction Costs | "The real-world cost to an AI company of pausing their servers, which means we can't just assume they will do it for free." |
| **Community Groups** | Scope Boundary (Water/Fibre excluded) | "This tool looks specifically at the electricity grid. We know that water use, local traffic, and community impact are equally important and must be assessed separately." |

**The Golden Rule for Public Comms:** 
Always lead with the **problem** (wasted wind power in the North, grid stress in the Lowlands), then introduce the **mechanism** (flexible AI training vs. inflexible inference), and only use the **technical term** ("Constraint-Direction") as a shorthand label *after* the concept is understood.
