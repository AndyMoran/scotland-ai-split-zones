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

## The Scottish Case Study

While the constraint-direction framework is globally applicable, Scotland serves as the empirical testbed. It uniquely combines significant renewable curtailment, distinct transmission boundaries (SCOTEX, SSEN-S), and an active AI Growth Zone policy. 

### Stage 2 Empirical Findings (2023-24 Data)
We tested the "timescale mismatch" hypothesis against real NESO constraint data. 

- **The Reality:** Median Scottish export constraint events last 1.5–2.0 hours. Modern hyperscaler IT stacks (async checkpointing, automated orchestration) can respond in ~1 hour. Therefore, median events are **temporally compatible** with flexible AI training.
- **The Caveat ("Compatibility is not capture"):** This does not mean 100% of value is captured. Actual flexibility depends on site connection capacity, commercial dispatch terms, and **AI-operator friction costs** (e.g., idle GPU amortization, checkpoint overhead). 
- **The Scale:** Using a defensible cost-proportion methodology, the estimated Scottish thermal constraint volume is **~1.76 TWh/year**, with a GB-wide average constraint cost proxy of **~£165/MWh** (applied to Scottish volumes). This represents a theoretical upper bound of **~£290M/year**, though real-world capture will be materially lower due to friction costs and physical incompatibility of short-duration (P10) events.

*For full methodology, data sources, and sensitivity analysis, see [PROJECT.md](PROJECT.md).*

---

## Scope Boundary

This is a grid-constraint framework, not a comprehensive siting model. It explicitly **does not** model:
- Water stress or cooling availability (mentioned only as a critical external constraint).
- Community acceptance, planning risk, or fibre connectivity (flagged as policy considerations, not scored variables).
- Co-located battery storage interactions (deferred to Stage 3).

---

## Repository Structure

This repository is structured to separate the *invitation* from the *specification*.

- **`README.md`**: High-level conceptual overview and empirical summary.
- **`PROJECT.md`**: Detailed project specification, data contracts, methodology, and policy questions.
- **`configs/`**: Reproducible, version-controlled assumptions (e.g., `workload_flexibility_assumptions.yml`, `curtailment_value_proxy.yml`).
- **`notebooks/`**: Executable analytical workflows (site typology, workload response, grid burden, renewable absorption).
- **`src/ai_split_zones/`**: Reusable Python/Polars logic.
- **`figures/`**: Tufte-compliant visualisations of Stage 2 results.

---

## Quick Start

bash

git clone https://github.com/AndyMoran/scotland-ai-split-zones.git

cd scotland-ai-split-zones

uv sync

uv run jupyter lab


---

## Licence

- Code: MIT License
- Documentation: CC BY 4.0
