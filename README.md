# Scotland AI Split-Zones

## A Constraint-Direction Framework for Grid-Responsive AI Compute

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Polars](https://img.shields.io/badge/polars-1.0+-75c7d6.svg)](https://pola.rs/)
[![uv](https://img.shields.io/badge/managed%20with-uv-10c9a8.svg)](https://docs.astral.sh/uv/)

> **Traditional energy planning classifies data centres by geography and total MW demand. This project classifies AI workloads by *constraint direction*.**

---

## The Core Insight

The grid-relevant unit is not "the data centre". It is the workload. 

Large-model training, real-time inference, and batch processing have fundamentally different power, latency, and flexibility characteristics. Treating them as a monolith leads to inefficient siting and unnecessary grid stress. 

This framework bifurcates AI siting into two distinct grid cases:

1. **Import-Constrained Sites (e.g., Central Lowlands):** New AI load adds to local import pressure. The objective is to **minimise residual grid burden** through workload scheduling, local storage, or flexible connection agreements.
2. **Export-Constrained Sites (e.g., Renewable-Rich North):** Local generation exceeds export capability. Here, flexible compute can act as **renewable absorption demand**, consuming power that would otherwise be curtailed.

*Note: This framework classifies workload behaviour rather than specific AI models, ensuring the underlying grid logic remains durable as algorithmic efficiency evolves.*

---

## Framework Evolution: Stages 1–6

While the constraint-direction framework is globally applicable, Scotland serves as the empirical testbed. It uniquely combines significant renewable curtailment, distinct transmission boundaries (SCOTEX, SSEN-S), and an active AI Growth Zone policy. 

- **Stage 1: Constraint Direction Thesis** – Bifurcating AI siting into import-constrained and export-constrained zones to align workload flexibility with local grid physics.
- **Stage 2: Empirical Timescale Mismatch** – Corrected synthetic data contamination to establish a verified ~1.76 TWh/year Scottish constraint volume (~£291M theoretical upper bound). Proved median events are temporally compatible with AI (~1hr checkpointing), but short-duration (P10) events are not.
- **Stage 3: Battery Sizing & Economic Limits** – Defended the 2-hour battery spec using empirical event-clustering data. Proved that constraint avoidance alone yields a 31.5-year simple payback, making multi-revenue merchant stacking an absolute necessity.
- **Stage 4: Grounded Merchant Stacking** – Replaced "sum-of-parts" financial assumptions with observed Modo Energy blended benchmarks (£41k–£73k/MW/year). Forced explicit declaration of the AI constraint commercial mechanism, revealing a realistic 8.6–18.7 year payback depending on market conditions and contract structures.
- **Stage 5: Behind-the-Meter Structural Limits** – Sourced real SSEN SHEPD tariffs to prove DUoS peak-shaving value is structurally limited at hyperscale voltages (£1.58/MWh differential). Identified the TNUoS ASC Band Step as the dominant (£1.8M/yr, PROVISIONAL) but contingent value driver. Wholesale peak-shaving is constrained by battery duration and price volatility, not load/price overlap — the site's baseline load always exceeds battery capacity, so the battery can shave any price peak regardless of whether a training spike is running.
- **Stage 6: The Inference Archetype** – Paired Stage 5's training site with its structural opposite: a 5MW inference site at HV in the Central Belt. Found DUoS value runs in the *opposite* direction from Stage 5 — 27.6× larger, not smaller, at the lower voltage tier (£43.67/MWh differential). Tested Ofgem's proposed data centre commitment fee against Ofgem's own queue capex data and found it holds up. Identified a coordination gap between Ofgem's viability-focused *Curate* reforms and its emerging *Connect Operate* flexibility workstream — arguably the stage's most useful contribution to the live consultation. Full detail in [`stage6/`](./stage6/).

*For full Stage 1–5 methodology, data sources, sensitivity analysis, and the complete adversarial review log, see: `PROJECT.md` and `docs/adversarial_review_log.md`. Stage 6 is documented separately — see [`stage6/README.md`](./stage6/README.md) for the narrative summary and [`stage6/STAGE6_SYNTHESIS.md`](./stage6/STAGE6_SYNTHESIS.md) for the full working record, including every correction made along the way.*

---

## Scope Boundary & Modelling Discipline

This is a grid-constraint framework, not a comprehensive siting model. It explicitly **does not** model:
- Water stress, cooling availability, or fibre connectivity (flagged as critical external constraints, not scored variables).
- Community acceptance or local planning risk.

Stages 5 and 6 are **paired archetype studies**, not a survey of Scottish data centres — one hyperscale training site, one smaller inference site, chosen because they sit at opposite ends of the axes that matter (workload type, connection voltage, constraint direction), not because either is statistically representative of the full range of proposed developments.

Furthermore, this framework enforces strict **modelling discipline** to prevent "finance-bro" double-counting:
- **No Sum-of-Parts Fantasy:** Baseline revenues use observed, blended market actuals, not theoretical maximums of stacked products.
- **Behavioural Separation:** Behind-the-meter savings are explicitly separated into *continuous* (DUoS), *step-function* (TNUoS ASC Band Step), and *partial residual* mechanisms. They are never blended into a single misleading total.
- **Explicit Omissions:** Known costs (e.g., augmentation CAPEX) and synthetic inputs (e.g., illustrative price shapes) are explicitly flagged in the Assumptions Ledger of every synthesis script.

---

## Repository Structure

This repository is structured to separate the *invitation* from the *specification*, prioritising radical transparency.

- **`README.md`**: High-level conceptual overview and empirical summary.
- **`PROJECT.md`**: Detailed project specification, data contracts, methodology, and policy questions (Stages 1–5).
- **`docs/adversarial_review_log.md`**: A transparent, living log of all data corrections, stress-tests, and modelling choices (e.g., the Stage 2 synthetic data correction, Stage 4 augmentation CAPEX omission).
- **`configs/`**: Reproducible, version-controlled assumptions (e.g., `battery_storage_assumptions.yml`).
- **`scripts/`**: Core Python/Polars logic for data processing, event clustering, and economic synthesis (Stages 2–5).
- **`notebooks/`**: Executable analytical workflows and publication-ready visualizations (e.g., `06_hybrid_ai_battery_response.ipynb`, `08_stage4_merchant_stacking_synthesis.ipynb`, `09_stage5_behind_the_meter_synthesis.ipynb`).
- **`figures/`**: Tufte-compliant visualisations of empirical findings, economic verdicts, and value stack breakdowns.
- **`stage6/`**: Self-contained module for the inference-archetype study — narrative `README.md`, full working record (`STAGE6_SYNTHESIS.md`), its own `scripts/`, `notebooks/`, and `figures/`. Kept separate from the Stage 1–5 flat structure above because Stage 6 targets a live, time-boxed consultation response rather than the ongoing programme documents.

---

## Quick Start

```bash
git clone https://github.com/AndyMoran/scotland-ai-split-zones.git
cd scotland-ai-split-zones
uv sync
uv run jupyter lab
```

To run the final economic synthesis and view the assumptions ledger:

```bash
uv run python scripts/10_stage4_merchant_stacking_synthesis.py
uv run python scripts/11_stage5_behind_the_meter_synthesis.py
uv run python stage6/scripts/12_stage6_central_belt_synthesis.py
```

## Licence
Code: MIT License
Documentation & Data: CC BY 4.0

This framework is provided as an open-source public good to elevate the standard of evidence in AI infrastructure planning.