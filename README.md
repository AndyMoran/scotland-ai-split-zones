# Scotland AI Split-Zones

## A training/inference siting framework for grid-constrained Scotland

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Polars](https://img.shields.io/badge/polars-1.0+-75c7d6.svg)](https://pola.rs/)
[![uv](https://img.shields.io/badge/managed%20with-uv-10c9a8.svg)](https://docs.astral.sh/uv/)
[![Project status](https://img.shields.io/badge/status-project%20specification-orange.svg)](#)

> **Scotland should not ask only where it can fit AI data centres. It should ask what kind of AI compute each site should host, and whether that load adds to grid stress or absorbs renewable power that the grid cannot otherwise move.**

---

## 1. Core thesis

Scotland's AI infrastructure debate risks treating "data centres" as a single category.

That is the mistake.

AI compute is not one thing. Large-model training, real-time inference, batch inference and edge AI have different power, latency, flexibility, planning and grid characteristics. They should not automatically be sited in the same places or judged by the same grid criteria.

This project develops an open-source framework to classify candidate Scottish AI sites by:

- AI workload suitability;
- constraint direction;
- renewable absorption value;
- residual grid burden;
- fibre and latency suitability;
- planning and land-use constraints;
- credible flexibility support, including tenant-safe VPP contribution where relevant.

The central distinction is:

```text
Flexible AI training load may belong near trapped renewable power.

Latency-sensitive inference may belong near users, fibre, public services,
universities, hospitals and enterprise demand.

Tenant-safe VPPs may help at the margin, but they are support layers,
not baseload substitutes for hyperscale AI.
```

---

## 2. Why this project exists

AI infrastructure is increasingly treated as a strategic national asset. The UK Government's AI Growth Zone programme explicitly links data centre deployment to electricity-system issues, including grid connections, planning support, power availability, water availability, land availability and connectivity. The Government's delivery paper states that timely electricity connections are the single biggest blocker for establishing AI Growth Zones and proposes reforms to accelerate grid connections and support data centre build-out.

Scotland is now part of that live policy landscape. The Scottish Government's AI Strategy 2026-2031 says it will work with partners to promote Scotland as a centre for green data centres and maximise the economic potential of the Lanarkshire AI Growth Zone. The Lanarkshire AI Growth Zone has been described by UK Government and DataVita/CoreWeave as a major AI infrastructure investment centred on up to 500 MW of compute capacity, private-wire renewable ambitions, fibre connectivity and industrial regeneration.

But the current debate risks compressing several different questions into one phrase: "AI data centres".

This project starts from a different premise:

> **The grid-relevant unit is not "the data centre". It is the workload.**

---

## 3. What this project is / is not

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

---

## 4. The Scottish siting problem

Scotland appears to be facing two overlapping problems.

### 4.1 The Lowlands hyperscale problem

Should Scotland host very large AI data centre campuses in the Lowlands, where grid, water, planning, community and renewable-supply claims may be contentious?

North Lanarkshire is the live policy case. It matters because it is politically salient, industrially significant and already designated as an AI Growth Zone.

However, North Lanarkshire should not automatically be treated as the optimal site for all AI workloads. It may be a useful site for some forms of AI infrastructure, but a generic Lowlands hyperscale model risks obscuring the difference between:

- flexible training demand;
- real-time inference demand;
- batch inference;
- edge AI;
- storage-backed support;
- renewable absorption demand.

#### 4.1.1 Technological velocity and stranded asset risk

Grid infrastructure depreciates over 15–30 years. AI algorithmic efficiency cycles run on 18-month horizons.
Hard-allocating 500 MW of firm import capacity in the Lowlands creates two structural risks:
Stranded ratepayer cost: If model light-weighting cuts compute intensity by 50–80%, socialized grid upgrade costs remain on utility balance sheets while the physical demand evaporates.
Opportunity cost: Reserving firm capacity for speculative, high-density AI campuses freezes out immediate, inelastic electrification needs (industrial decarbonisation, heat networks, transport).

### 4.2 The renewable absorption opportunity

In renewable-surplus, export-constrained Scottish zones, flexible AI training load may not be a grid burden in the same way.

North of major transmission boundaries, renewable output can exceed the capacity of the grid to move power southward. When that happens, wind farms may be constrained off and consumers ultimately pay for constraint management.

A flexible AI training hub located near trapped renewable output may:

- consume renewable power that might otherwise be curtailed;
- reduce the amount of power that needs to flow across constrained boundaries;
- allow renewable generators to run more often;
- reduce avoided-curtailment cost, depending on market design;
- provide a strategic demand sink in the right place.

This does not remove the transmission constraint. It changes the economic and operational consequence of the constraint.

---

## 5. Workload split

The project distinguishes AI workloads by their grid behaviour.

| Workload type | Grid behaviour | Likely siting logic | Baseline flexibility assumption |
|---|---|---|---|
| Large-model training | High power demand; long-running; potentially schedulable at job level | Renewable-rich/export-constrained zones | Schedulable at start/stop level, not freely interruptible |
| Real-time inference | Latency-sensitive; service-level driven | Lowlands, fibre routes, users, public services | Mostly inflexible |
| Batch inference | Queueable; partly shiftable | Could follow grid-aware scheduling | Shiftable within limited window |
| Edge AI | Smaller, localised, service-specific | Near operational need | Case-specific |

The project deliberately treats workload flexibility as an assumption to be tested, not a magic capability.

---

## 6. Constraint-direction framework

The project bifurcates AI siting into two grid cases.

## Case A — Import-dependent sites

For Lowlands, urban or industrial sites where new AI load adds to local import pressure, the key metric is:

```text
Residual Grid Burden
```

These sites may need mitigation through:

- workload scheduling;
- local storage;
- tenant-safe VPP support;
- private-wire renewables;
- grid reinforcement;
- demand response obligations;
- flexible connection agreements.

## Case B — Export-constrained renewable-surplus sites

For renewable-rich constrained zones, the key metric is:

```text
Renewable Absorption Value
```

In these zones, flexible AI training load may:

- consume local renewable power that would otherwise be curtailed;
- reduce wasted renewable energy;
- reduce export pressure across constrained boundaries;
- provide a demand-side alternative to simply turning generators down.

This bifurcation is the structural backbone of the project.

---

## 7. Site typology

| Site type | Grid condition | Best AI workload | Main metric |
|---|---|---|---|
| Export-constrained renewable-surplus zone | Local generation exceeds export capability | Flexible training | Avoided curtailment / renewable absorption |
| Import-constrained Lowlands site | New demand may worsen local grid stress | Inference / smaller clusters | Residual grid burden |
| Balanced industrial zone | Some grid access, but strategic load still matters | Mixed compute | Net grid impact |
| VPP-rich community zone | Distributed flexibility available | Inference / support services | Event-time flexibility support |

---

## 8. Candidate demonstrator areas

### Renewable absorption demonstrators

These are the strongest candidates for the training-load thesis:

- Peterhead / North East Scotland;
- Caithness / wider northern Scotland;
- SSEN-N renewable-rich zones;
- other high-curtailment / export-constrained locations.

Purpose:

> Test whether flexible training load can act as renewable absorption demand.

### Policy and Lowlands demonstrators

These are politically and economically important but may not be optimal for renewable absorption:

- North Lanarkshire / AI Growth Zone;
- Glasgow;
- Edinburgh;
- Fife;
- Lanarkshire.

Purpose:

> Test whether inference clusters or mixed compute sites can be designed with lower residual grid burden.

North Lanarkshire remains important because it is the live policy case. Analytically, however, it should not be treated as the automatic best-fit site for renewable-curtailment absorption.

---

## 9. Workload flexibility assumptions

The first version of the project uses a configuration-led assumption module, not an overconfident AI workload orchestration model.

Assumptions live in:

```text
configs/workload_flexibility_assumptions.yml
```

Baseline structure:

```yaml
real_time_inference:
  flexibility: low
  assumption: "must run when requested"
  shift_window_hours: 0

batch_inference:
  flexibility: medium
  assumption: "can be queued or delayed"
  shift_window_hours: [1, 2, 4]

training_jobs:
  flexibility: medium_high
  assumption: "schedulable at job start/stop level"
  schedulable_fraction: [0.1, 0.3, 0.5]
  notice_required_hours: [4, 12, 24]

active_training_runs:
  flexibility: low_medium
  assumption: "not freely interruptible mid-run"
  checkpoint_interruptibility: false_in_baseline

geographic_migration:
  flexibility: sensitivity_only
  assumption: "not assumed in baseline"
```

Notebook 02 is therefore not an assumptions notebook. It is a validation notebook that reads the YAML and produces response curves.

```text
notebooks/02_workload_response_curves.ipynb
```

---

## 10. Simple workload response model

To avoid an undefined "workload shifting" term, the project translates workload assumptions into an estimated MW response.

Schedulable AI Load MW =
Total Compute Load MW × Schedulable Fraction × Duration Compatibility Factor

Renewable Absorption MW =
min(
    Schedulable AI Load MW,              # Demand-side ceiling (e.g., 250 MW)
    Available Curtailed Renewable MW,    # Supply-side ceiling (e.g., 269.5 MW)
    Site Connection Capacity MW          # Physical infrastructure limit
)

Where:

- **Schedulable Fraction** is the share of workload that can be delayed, started, stopped or queued.
- **Event Response Availability** reflects whether the site has enough notice to respond.
- **Duration Compatibility Factor** reflects whether the grid event is long enough to matter relative to workload scheduling timescales.

### Duration Compatibility Factor

The MVP uses a soft duration compatibility factor:

```text
duration_compatibility_factor =
min(1, event_duration_hours / minimum_scheduling_notice_hours)
```

Examples:

| Event duration | Notice requirement | Factor |
|---:|---:|---:|
| 2 hours | 4 hours | 0.50 |
| 4 hours | 4 hours | 1.00 |
| 8 hours | 4 hours | 1.00 |

This is deliberately simple and auditable.

It does **not** imply that active AI training jobs are freely interruptible within settlement-period timescales. It only estimates whether the event duration is compatible with the assumed workload scheduling timescale.

A hard-gate sensitivity can also be run:

```text
duration_compatibility_factor =
1 if event_duration_hours >= minimum_scheduling_notice_hours else 0
```

Config example:

```yaml
duration_compatibility:
  method: "soft_ratio"
  formula: "min(1, event_duration_hours / minimum_scheduling_notice_hours)"
  hard_gate_available: true
  hard_gate_formula: "1 if event_duration_hours >= minimum_scheduling_notice_hours else 0"
```

---

## 11. Grid-impact models

## 11.1 Model A — import-constrained sites

For import-dependent Lowlands, urban or industrial sites:

```text
Residual Grid Burden =
AI Compute Load
- On-site / private-wire renewable supply
- Workload flexibility response
- Local storage contribution
- Tenant-safe VPP contribution
+ Backup / resilience requirement
```

This model applies where new demand may increase local peak import.

## 11.2 Model B — export-constrained renewable-surplus sites

For renewable-rich constrained zones:

```text
Renewable Absorption =
min(
    Flexible AI Load,
    Available Curtailed Renewable Output,
    Site Connection Capacity
)
```

Associated value:

```text
Renewable Absorption Value =
Absorbed MWh
× avoided curtailment / constraint-management value proxy
```

### Site Connection Capacity as MVP proxy

For MVP, `site_connection_capacity_mw` is used as a conservative proxy for local network-compatible demand.

This may be:

- contracted import capacity;
- planning-stated connection capacity;
- a documented site-level MW limit;
- another auditable public proxy.

This does not fully represent local transmission or distribution thermal limits, which may not be publicly available at sufficient resolution. Where detailed circuit ratings are unavailable, the model treats connection capacity as the upper bound on absorbable AI load.

---

## 12. Curtailment value proxy

No monetary renewable-absorption result should be published until the value proxy is pinned.

The project requires:

```text
configs/curtailment_value_proxy.yml
```

Skeleton:

```yaml
curtailment_value_proxy:
  source_name: null
  publication_year: null
  geography: null
  boundary_or_zone: null
  value_gbp_per_mwh: null
  value_type: null
  notes: "Must be pinned before monetary results are published."
```

The source must specify:

- publication source;
- publication year;
- geography or boundary;
- whether the value is system-wide, zonal or boundary-specific;
- whether it represents constraint cost, bid/offer cost, curtailment compensation or another proxy;
- units, usually £/MWh;
- limitations.

Candidate sources include NESO constraint-management publications, Electricity Ten Year Statement material, balancing/constraint market data, and derived BM/BOA/BOALF event values where the method is transparent.

---

## 13. Role of tenant-safe VPP support

The project does **not** assume domestic VPPs can power data centres.

They cannot, at least not at hyperscale.

A tenant-safe domestic VPP is a support layer, not a baseload substitute.

From the current Tenant-Safe VPP work:

```text
50,000-home NGA/LTO fleet:
normal winter firm capacity: ~62 MW
cold-spell firm capacity: ~5 MW
```

Against a 150 MW training hub:

```text
normal winter: ~40% of peak load
cold-spell: ~3%
```

Against a 500 MW hyperscale campus:

```text
normal winter: ~12%
cold-spell: ~1%
```

So the VPP contribution is most useful for:

- peak smoothing;
- event-time support;
- reducing residual import;
- supporting local constraints;
- improving connection acceptability;
- absorbing surplus renewables where charging headroom exists.

It is not credible as a primary power source for hyperscale AI load.

That honesty is part of the model.

---

## 14. Data contract

The candidate site register is the foundation of the project. No notebook should be built before the source contract is defined.

The source contract lives in:

```text
configs/data_sources.yml
```

Initial skeleton:

```yaml
constraint_zones:
  description: "Scottish transmission constraint zones and boundary classifications"
  candidate_sources:
    - "NESO constraint group / boundary publications"
    - "SSEN/SPT transmission boundary maps"
    - "TNUoS zone boundaries"
  required_fields:
    - zone_id
    - zone_name
    - boundary
    - constraint_direction
    - source_vintage
  status: "to_verify"

curtailment:
  description: "Half-hourly or zonal constraint / curtailment proxy"
  candidate_sources:
    - "NESO constraint management data"
    - "Balancing Mechanism accepted actions"
    - "constraint cost publications"
  required_fields:
    - timestamp
    - zone_or_boundary
    - curtailed_mwh_proxy
    - cost_proxy_gbp_per_mwh
  status: "to_verify"

renewable_projects:
  description: "Renewable project locations and capacities"
  candidate_sources:
    - "REPD"
  required_fields:
    - project_name
    - technology
    - capacity_mw
    - latitude
    - longitude
    - status
  status: "to_verify"

fibre_access:
  description: "Fibre / digital infrastructure proxy"
  candidate_sources:
    - "Ofcom Connected Nations"
  required_fields:
    - geography
    - fibre_availability_proxy
    - source_vintage
  status: "to_verify"

connection_queue:
  description: "Demand connection queue / grid connection pressure"
  candidate_sources:
    - "NESO connections reform results"
    - "Ofgem demand connections reform"
    - "local planning documents"
  required_fields:
    - site_or_zone
    - connection_capacity_mw
    - queue_status
    - expected_connection_date
  status: "to_verify"

planning:
  description: "Named site planning and development applications"
  candidate_sources:
    - "North Lanarkshire planning portal"
    - "relevant local authority planning portals"
  required_fields:
    - planning_reference
    - site_name
    - developer
    - capacity_mw
    - land_area
    - planning_status
  status: "to_verify"
```

---

## 15. MVP scope

The first version should be narrow, executable and public-data based.

## Stage 1 — publishable MVP

**Title:**

```text
Scotland AI Split-Zones:
A Constraint-Direction Siting Framework for Grid-Responsive AI Compute
```

Includes:

1. Scottish candidate site register.
2. Site typology: import-constrained, export-constrained, balanced, VPP-rich.
3. Workload flexibility assumptions file.
4. Workload response curves.
5. Residual grid-burden model for import-dependent sites.
6. Renewable-absorption model for export-constrained sites, including sensitivity analysis across varying IT notice periods (4h to 24h).
7. Simple training-versus-inference siting scenarios.
8. One clear site-scorecard chart.

Excludes for v1:

- full AI workload orchestration;
- geographic migration of live training jobs;
- detailed VPP dispatch simulation;
- vendor-specific software assumptions;
- full architecture comparison;
- monetary avoided-curtailment results unless the proxy is pinned.

## Stage 2 — extension

Adds:

- tenant-safe VPP support layer;
- workload scheduling sensitivities;
- architecture comparison;
- event-time constraint response;
- policy options for flexible data-centre connections;
- monetised renewable-absorption value where source-backed.

---

## 16. Architecture comparison credibility rule

When the architecture comparison is eventually added, avoid circular reasoning.

The credibility rule:

```text
If two architectures receive different assumptions, the reason must be structural,
not optimistic.
```

Examples:

- A training hub may receive higher schedulable-load potential because training is structurally more schedulable.
- An inference cluster may receive lower flexibility because real-time inference is latency-sensitive.
- A renewable-zone site may receive higher absorption potential because it is physically near constrained renewable generation.
- VPP support must be applied consistently wherever the same VPP resource is available.

The project should not "prove" the preferred architecture by giving it all the favourable inputs.

---

## 17. Policy questions

The project is about strategic demand connection design, not just data centres.

Questions for policy:

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
---

## 18. Repository structure

```text
scotland-ai-split-zones/
├── README.md
├── PROJECT.md
├── TECH_STACK.md
├── pyproject.toml
├── configs/
│   ├── data_sources.yml
│   ├── candidate_sites.yml
│   ├── constraint_direction.yml
│   ├── workload_flexibility_assumptions.yml
│   ├── vpp_support_assumptions.yml
│   └── curtailment_value_proxy.yml
├── data/
│   ├── raw/
│   ├── external/
│   ├── intermediate/
│   └── processed/
├── notebooks/
│   ├── 01_site_register_and_typology.ipynb
│   ├── 02_workload_response_curves.ipynb
│   ├── 03_residual_grid_burden_model.ipynb
│   ├── 04_renewable_absorption_model.ipynb
│   └── 05_site_scorecard.ipynb
├── src/
│   └── ai_split_zones/
│       ├── sites.py
│       ├── workloads.py
│       ├── constraints.py
│       ├── grid_burden.py
│       ├── renewable_absorption.py
│       ├── vpp_support.py
│       └── plots.py
└── figures/
```

---

## 19. Notebook plan

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

---

## 20. Tech stack

- Python 3.11
- `uv` for environment and dependency management
- Polars for tabular processing
- DuckDB for local analytical querying
- NumPy for vectorised modelling
- SciPy for distributions / sensitivity work where required
- Matplotlib for static figures
- PyYAML / Pydantic for config validation
- Jupyter notebooks as the explanatory interface
- Reusable logic promoted into `src/`

---

## 21. Setup

```bash
git clone (https://github.com/AndyMoran/scotland-ai-split-zones/)
cd scotland-ai-split-zones
uv sync
```

Run notebooks:

```bash
uv run jupyter lab
```

Run tests:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check .
```

---

## 22. Definition of Done

The MVP is complete when:

- `configs/data_sources.yml` is populated and source vintages are recorded.
- Candidate Scottish AI sites are classified by constraint direction.
- Workload assumptions are config-driven and validated.
- Duration Compatibility Factor is implemented.
- Import-constrained residual grid burden is calculated.
- Export-constrained renewable absorption is calculated using `site_connection_capacity_mw`.
- No monetary curtailment result is published without a pinned value proxy.
- Site scorecard is reproducible from clean execution.
- All core assumptions are visible in config files.
- README and PROJECT.md state what the model does **not** prove.

---

## 23. Known limitations

This MVP will not fully model:

- detailed transmission circuit thermal limits;
- private connection agreement details;
- full AI workload orchestration;
- geographic migration of active training jobs;
- detailed water infrastructure;
- detailed heat-reuse engineering;
- tenant-level VPP dispatch;
- commercial connection negotiations;
- confidential developer assumptions.
- MVP uses a conservative 50% curtailment availability proxy based on UK-wide NESO data; Stage 2 will incorporate granular, Scottish-specific constraint flow data.
- MVP evaluates workload flexibility as a standalone grid service. The interaction between slow IT checkpointing and co-located battery storage is explicitly deferred to Stage 3.

The MVP is a public-data framework. It is designed to make the siting logic transparent, not to replace detailed connection studies.

---

## 24. References and source anchors

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

---

## 25. Working LinkedIn summary

AI data centres should not all be treated as fixed grid burdens.

In the wrong place, AI load can worsen peak demand, water stress, land-use conflict and grid-connection pressure.

But in the right place — especially renewable-surplus, export-constrained Scottish zones — flexible AI training load could do something valuable:

absorb power that might otherwise be curtailed.

This project asks:

> Where is AI compute a burden, where is it a grid service, and how should Scotland distinguish between the two?

The key distinction is training versus inference.

Training is power-intensive but potentially schedulable.

Inference is latency-sensitive and may belong closer to users, fibre, universities, hospitals, public services and enterprise demand.

The point is not pretending domestic batteries can power hyperscale AI.

They cannot.

The useful question is more precise:

> Can flexible compute load, renewable co-location and verified VPP support reduce residual grid burden, absorb curtailed renewables and improve the credibility of strategic demand connections?

---

## Licence

- Code: MIT License
- Documentation: CC BY 4.0

