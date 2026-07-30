# PROJECT.md: Scotland AI Split-Zones — Project Specification

**Status:** Stages 1–5 Complete  
**Last updated:** July 2026  
**Purpose:** Define the project scope, methodology, findings, data contracts, and policy questions for the Scotland AI Split-Zones framework.

**Core Thesis:** *Traditional energy planning classifies data centres by geography and total MW demand. This project classifies AI workloads by constraint direction — and proves, empirically, that the gap between "theoretically flexible" and "actually deliverable" is where policy must focus.*

> For the complete, verified citation list, see `research_citations.md`.  
> For the adversarial review log (all data corrections and stress-tests), see `docs/adversarial_review_log.md`.

---

## 1. What This Project Is / Is Not

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

## 2. Workload Split

The project distinguishes AI workloads by their grid behaviour.

| Workload type | Grid behaviour | Likely siting logic | Baseline flexibility assumption |
|---|---|---|---|
| Large-model training | High power demand; long-running; potentially schedulable at job level | Renewable-rich/export-constrained zones | Schedulable at start/stop level, not freely interruptible |
| Real-time inference | Latency-sensitive; service-level driven | Lowlands, fibre routes, users, public services | Mostly inflexible |
| Batch inference | Queueable; partly shiftable | Could follow grid-aware scheduling | Shiftable within limited window |
| Edge AI | Smaller, localised, service-specific | Near operational need | Case-specific |

---

## 3. Site Typology

| Site type | Grid condition | Best AI workload | Main metric |
|---|---|---|---|
| Export-constrained renewable-surplus zone | Local generation exceeds export capability | Flexible training | Avoided curtailment / renewable absorption |
| Import-constrained Lowlands site | New demand may worsen local grid stress | Inference / smaller clusters | Residual grid burden |
| Balanced industrial zone | Some grid access, but strategic load still matters | Mixed compute | Net grid impact |
| VPP-rich community zone | Distributed flexibility available | Inference / support services | Event-time flexibility support |

---

## 4. Policy Questions

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

- Should Scotland be cautious about overbuilding AI training capacity that may become obsolete within 5–10 years, given the pace of algorithmic efficiency gains?
- Could diverting AI training to remote export-constrained sites undermine Scotland's AI services economy, which benefits from proximity to users, universities, and enterprise demand in the Central Belt?
- Are there better uses for curtailed renewable energy than AI training (e.g., green hydrogen production, industrial electrification, grid-scale storage) that deliver more durable economic or decarbonisation value per MWh?
- If flexible AI training proves economically unviable due to operator friction costs, should export-constrained zones instead pursue direct renewable-to-industry connections (e.g., data centres co-located with wind farms via private wire) rather than relying on Balancing Mechanism dispatch?

---

## 5. Project Status: Stages 1–5

All five stages are complete. Each stage built on the findings of the previous one, with adversarial review applied at every transition.

### Stage 1: Constraint Direction Thesis ✅ COMPLETE

**Core question:** Should AI workloads be classified by grid function rather than geography?

**Key deliverables:**
- Constraint-direction siting framework (import-constrained vs. export-constrained)
- Workload taxonomy (training, inference, batch, edge) with grid-behaviour mapping
- Duration Compatibility Factor formula
- Site typology and scorecard methodology
- Configuration-driven assumptions (`configs/workload_flexibility_assumptions.yml`)

**Key finding:** The grid-relevant unit is the workload, not the data centre. Flexible training belongs near renewable surplus; latency-sensitive inference belongs near users and fibre.

---

### Stage 2: Empirical Timescale Mismatch ✅ COMPLETE

**Core question:** Can AI training actually respond to Scottish grid constraint events in time?

**Key deliverables:**
- Empirical constraint event register from NESO data (SCOTEX, SSEN-S boundaries)
- Duration distributions (SCOTEX median: 2.0h, SSEN-S median: 1.5h)
- IT notice period decomposition (~0.93h total, hyperscaler lower bound)
- Verified Scottish constraint volume: ~1.76 TWh/year (corrected from initial ~3.0 TWh after catching synthetic data contamination)
- Constraint cost proxy: £164.89/MWh (GB-wide average)
- Theoretical upper bound: ~£291M/year (corrected from initial ~£500M)
- 4 Tufte-compliant visualizations

**Key finding:** Median events are temporally compatible with AI training (~1hr checkpointing). However, short-duration (P10) events are physically incompatible — 27% of constraint events end before an AI hub can respond. "Compatibility is not capture."

**Critical correction:** Initial analysis included synthetic Day-Ahead forecast data masquerading as historical outturn. A strict `year.is_in([2023, 2024])` filter was applied, correcting the volume from ~3.0 TWh to ~1.76 TWh and the theoretical ceiling from ~£500M to ~£291M. Full details in `docs/adversarial_review_log.md` §1.

---

### Stage 3: Battery Sizing & Economic Limits ✅ COMPLETE

**Core question:** Can a co-located battery bridge the timescale mismatch, and does it pay for itself?

**Key deliverables:**
- Empirical event-clustering analysis (inter-event gaps, chain depth, rolling window density)
- 2-hour battery spec validated against worst-case historical sequence (26.5-hour marathon event, Dec 30-31 2024)
- Hybrid AI + battery response simulation (50 MW / 100 MWh paired with 100 MW AI hub)
- Marginal value breakdown: £0.12M/year (P10 events) + £0.67M/year (handoff coverage) = £0.79M/year upper bound
- Round-trip efficiency (85% AC-AC) applied
- Constant-magnitude upper-bound assumption explicitly stated
- 31.5-year simple payback on constraint value alone
- 2 Tufte-compliant visualizations

**Key finding:** The battery's primary economic role is not catching short events — it's smoothing the 1-hour handoff transition for longer events. However, even combined, constraint avoidance alone yields a 31.5-year payback on a £25M investment. Multi-revenue merchant stacking is an absolute necessity.

**Defence against adversarial review:** The 2-hour spec was challenged on the basis that P10 events don't stack back-to-back. Empirical clustering analysis proved: 0% of 2-hour windows contain 3+ events; the battery survives 3+ consecutive events 100% of the time under zero-recharge assumptions. The 2-hour spec is validated not just for reliability, but to retain ~35 MWh of usable headroom for merchant revenue stacking between events.

---

### Stage 4: Grounded Merchant Stacking ✅ COMPLETE

**Core question:** What does a co-located battery actually earn in today's GB market, and does AI constraint avoidance improve the business case?

**Key deliverables:**
- Modo Energy blended benchmarks integrated (£41k–£73k/MW/year observed actuals)
- Sum-of-parts double-counting explicitly prevented (original £105-175k/MW estimate rejected)
- Constraint layer guardrail (`scripts/constraint_layer.py`) — raises `ValueError` if mechanism is not explicitly declared
- Three mechanisms evaluated: BM overlap (£0 incremental), bilateral contract (£15.8k/MW/yr), system passthrough (£0 incremental)
- Realistic payback calculated: 8.6 years (rolling average, investable) to 18.7 years (conservative trough, marginal-to-uninvestable)
- Headline split into "investable" vs "marginal" categories (not blended)
- Augmentation CAPEX flagged as OMITTED (not DELIBERATE)
- 5-category Assumptions Ledger (GROUNDED / PROVISIONAL / DELIBERATE / FORWARD-LOOKING / OMITTED)
- 3 Tufte-compliant visualizations

**Key finding:** The conventional merchant stack alone gives a defensible 8.6–18.7 year payback. AI constraint avoidance could improve this to 6.8–11.7 years, but ONLY if GB develops a bilateral flexibility contract mechanism that Ofgem is currently just recommending be explored. The gap between "physically possible" and "currently contracted" is itself the finding.

**Defence against adversarial review:** The original Stage 4 brief proposed summing four standalone revenue figures (arbitrage + FR + CM + constraint avoidance) to produce £105-175k/MW/year. Adversarial review identified this as ~2× the actual observed market ceiling, due to cannibalisation between products. The model was rebuilt around observed blended benchmarks. The bilateral contract scenario was explicitly flagged as FORWARD-LOOKING (no GB precedent exists as of July 2026).

---

### Stage 5: Behind-the-Meter Cost Avoidance ✅ COMPLETE

**Core question:** How much value does a co-located battery generate by shaving the AI site's own peak consumption and avoiding network charges?

**Key deliverables:**
- SSEN SHEPD 132kV/EHV DUoS tariffs sourced and integrated (Red: £1.58/MWh, Green: £0.00/MWh)
- DUoS structural limitation at hyperscale voltages documented (~30× less than HV/33kV sites)
- TNUoS ASC Band Step modelled as step-function (£1.8M/year, contingent on formal capacity reduction)
- TNUoS Locational Residual modelled as partial residual (£600/year, post-2023 TCR)
- Wholesale peak-shaving modelled with explicit load/price overlap caveat (£12k/year in illustrative scenario)
- Behavioural separation enforced (continuous vs. step-function vs. partial residual — never blended)
- Synthetic/illustrative data explicitly flagged throughout
- 4 Tufte-compliant visualizations

**Key finding:** For a 100MW AI site at 132kV, DUoS avoidance is structurally limited (£1.58/MWh differential). The real behind-the-meter value driver is the TNUoS ASC Band Step (£1.8M/year), but this requires a formal, sustained capacity reduction — not just opportunistic dispatch. Wholesale peak-shaving is capped by load/price overlap, not battery size.

**Defence against adversarial review:** Initial placeholder DUoS rates (£18/£3 per MWh) were replaced with sourced SSEN SHEPD tariffs (£1.58/£0.00 per MWh), revealing that the real differential is ~10× smaller than assumed. This was flagged as a finding, not hidden. The TNUoS ASC Band Step was explicitly separated from continuous savings to prevent a reader from assuming uniform reliability across all three mechanisms.

---

### Cross-Stage Adversarial Review Summary

| Stage | Key Catch | Impact |
|-------|-----------|--------|
| 2 | Synthetic forecast data contamination | Volume corrected: 3.0 → 1.76 TWh; ceiling: £500M → £291M |
| 3 | P10 event clustering challenge | 2-hour spec empirically validated |
| 4 | Sum-of-parts double-counting | Revenue baseline corrected: £105-175k → £41-73k/MW |
| 4 | Augmentation CAPEX omission | Flagged as OMITTED, not DELIBERATE |
| 4 | Two £0 mechanisms conflated | Split into BM overlap vs. system passthrough |
| 5 | Placeholder DUoS rates | Replaced with sourced SSEN SHEPD tariffs (10× correction) |
| 5 | Load/price overlap assumption | Explicitly modelled and flagged as structural ceiling |

Full details: `docs/adversarial_review_log.md`

---

## 6. Definition of Done

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
- [x] Defensible constraint volume proxy calculated (1.76 TWh for Scotland via cost-proportion method, corrected)
- [x] Empirical constraint cost proxy pinned (£164.89/MWh average)
- [x] Theoretical maximum addressable market identified (£291M/year, corrected)
- [x] AI-side friction costs and symmetric stranded-asset risks explicitly documented
- [x] Tufte-compliant visualizations produced (4 figures)
- [x] README updated with empirical findings and strict caveats

### Stage 3: Battery Sizing & Economic Limits ✅ COMPLETE
- [x] Empirical event-clustering analysis (inter-event gaps, chain depth, rolling window density)
- [x] 2-hour battery spec validated against worst-case historical sequence (26.5h marathon, Dec 2024)
- [x] Hybrid AI + battery response simulation (50 MW / 100 MWh + 100 MW AI hub)
- [x] Marginal value breakdown (£0.12M P10 + £0.67M handoff = £0.79M/yr upper bound)
- [x] Round-trip efficiency (85% AC-AC) applied
- [x] Constant-magnitude upper-bound assumption explicitly stated
- [x] 31.5-year simple payback on constraint value alone documented
- [x] Merchant stacking necessity established
- [x] Tufte-compliant visualizations produced (2 figures)

### Stage 4: Grounded Merchant Stacking ✅ COMPLETE
- [x] Modo Energy blended benchmarks integrated (£41k–£73k/MW/year)
- [x] Sum-of-parts double-counting explicitly prevented
- [x] Constraint layer guardrail (ValueError on UNCERTAIN mechanism)
- [x] Three mechanisms evaluated (BM overlap, bilateral contract, system passthrough)
- [x] Realistic payback calculated (8.6–18.7 years baseline-only)
- [x] Headline split into "investable" vs "marginal-to-uninvestable"
- [x] Augmentation CAPEX flagged as OMITTED (not DELIBERATE)
- [x] 5-category Assumptions Ledger implemented
- [x] Bilateral contract flagged as FORWARD-LOOKING (no GB precedent)
- [x] Tufte-compliant visualizations produced (3 figures)

### Stage 5: Behind-the-Meter Cost Avoidance ✅ COMPLETE
- [x] SSEN SHEPD 132kV/EHV DUoS tariffs sourced and integrated (£1.58/MWh differential)
- [x] DUoS structural limitation at hyperscale voltages documented
- [x] TNUoS ASC Band Step modelled as step-function (£1.8M/yr, contingent)
- [x] TNUoS Locational Residual modelled as partial residual (£600/yr)
- [x] Wholesale peak-shaving modelled with explicit overlap caveat
- [x] Behavioural separation enforced (continuous vs step-function vs partial)
- [x] Synthetic/illustrative data explicitly flagged throughout
- [x] Combined Stage 4 + Stage 5 value stack visualized
- [x] Tufte-compliant visualizations produced (4 figures)

---

## 7. Notebook Plan

### Notebook 01 — `01_site_register_and_typology.ipynb` (Stage 1)
- Build candidate site register; classify by constraint direction; assign workload suitability.

### Notebook 02 — `02_workload_response_curves.ipynb` (Stage 1)
- Generate flexible-load response curves; compare schedulable fractions and notice periods.

### Notebook 03 — `03_residual_grid_burden_model.ipynb` (Stage 1)
- Evaluate import-dependent sites; calculate residual grid burden under workload/VPP/storage assumptions.

### Notebook 04 — `04_renewable_absorption_model.ipynb` (Stage 1)
- Evaluate export-constrained sites; estimate absorbable curtailed renewable energy.

### Notebook 05 — `05_site_scorecard.ipynb` (Stage 1)
- Combine all metrics into public-facing site scorecard.

### Notebook 06 — `06_hybrid_ai_battery_response.ipynb` (Stage 3)
- Simulate hybrid AI + battery response against real NESO constraint events.
- Calculate marginal value breakdown (P10 events + handoff coverage).
- Validate 2-hour battery spec against event clustering.

### Notebook 07 — `07_stage3_economic_verdict.ipynb` (Stage 3)
- Compare battery CAPEX against marginal constraint value.
- Calculate simple payback on constraint avoidance alone.
- Produce strategic verdict on merchant stacking necessity.

### Notebook 08 — `08_stage4_merchant_stacking_synthesis.ipynb` (Stage 4)
- Load Modo Energy blended benchmarks as reality-check baseline.
- Run three-mechanism sensitivity analysis.
- Calculate payback for all scenarios (investable vs marginal).
- Produce revenue waterfall and mechanism overlap diagrams.
- Output full Assumptions Ledger.

### Notebook 09 — `09_stage5_behind_the_meter_synthesis.ipynb` (Stage 5)
- Generate synthetic AI load profile and illustrative price shape.
- Visualise load/price overlap problem.
- Calculate DUoS, TNUoS ASC, TNUoS Locational, and wholesale peak-shaving values.
- Produce DUoS voltage sensitivity chart.
- Combine Stage 4 + Stage 5 into full value stack visualization.

---

## 8. References

The complete, verified citation list is maintained in `research_citations.md` at the repository root.

All empirical data is sourced from public, auditable datasets. No proprietary or confidential data is used. Synthetic/illustrative data is explicitly flagged throughout the codebase.

**Pre-publication verification:** Before any external submission, run the checklist in `research_citations.md` §12 to confirm all PROVISIONAL assumptions are sourced and all ILLUSTRATIVE data is flagged.

---

## 9. Plain English Translation Guide

| Audience | Technical Term | Plain English Translation |
|----------|---------------|--------------------------|
| **Grid Engineers / Academics** | Constraint-Direction Computing | "Classifying compute workloads by whether they add to import pressure or absorb export curtailment." |
| **Government Ministers / Policymakers** | Export-Constrained Renewable Absorption | "Putting flexible AI training where the wind is blowing but the wires are full, turning wasted energy into an economic asset." |
| **Government Ministers / Policymakers** | Import-Constrained Residual Grid Burden | "Ensuring new AI data centres in the Lowlands don't overload local grids or drive up bills for existing residents and businesses." |
| **Journalists / General Public** | Duration Compatibility Factor | "Making sure the AI can actually pause and restart fast enough to match how long the grid constraint lasts." |
| **Journalists / General Public** | AI-Operator Friction Costs | "The real-world cost to an AI company of pausing their servers, which means we can't just assume they will do it for free." |
| **Community Groups** | Scope Boundary (Water/Fibre excluded) | "This tool looks specifically at the electricity grid. We know that water use, local traffic, and community impact are equally important and must be assessed separately." |
| **Energy Economists / Investors** | Sum-of-parts double-counting | "Adding up the 'best case' revenue from each market service separately, as if a battery could earn all of them at full capacity simultaneously. In reality, they compete for the same MWh." |
| **Energy Economists / Investors** | Constraint layer mechanism guardrail | "A software guardrail that physically prevents the model from running unless you explicitly declare HOW the battery captures constraint value." |
| **Policymakers / Planners** | TNUoS ASC Band Step | "A one-time permanent saving on your grid connection bill, but only if you can prove to the network operator that you've permanently reduced your peak demand — not just shaved it occasionally." |
| **Policymakers / Planners** | DUoS structural limitation at EHV | "Big sites connecting at high voltage (132kV) already pay very low distribution charges, so there's very little left to save by shifting consumption. The savings are structurally limited by physics, not by battery size." |
| **Policymakers / Planners** | Bilateral contract mechanism (forward-looking) | "A direct commercial deal between the battery owner and the AI operator, paid outside normal market channels. Doesn't exist in GB yet — Ofgem is only just recommending it be explored." |
| **Journalists / General Public** | Load/price overlap problem | "The battery can only save money by avoiding expensive electricity if the AI's peak consumption happens to coincide with peak prices. If they don't overlap, the battery has nothing to shave against." |
| **Journalists / General Public** | Investable vs. marginal payback | "An 8.6-year payback means investors will fund it. An 18.7-year payback means the battery might need replacing before it's paid for itself." |
| **Developers / DNOs** | Behavioural separation (continuous vs step-function) | "DUoS savings happen every half-hour you shift load. TNUoS ASC savings happen once, when you cross a threshold. Blending them into one number misleads readers into thinking all the savings are equally reliable." |

**The Golden Rule for Public Comms:**
Always lead with the **problem** (wasted wind power in the North, grid stress in the Lowlands), then introduce the **mechanism** (flexible AI training vs. inflexible inference), and only use the **technical term** as a shorthand label *after* the concept is understood.

---

## 10. Modelling Discipline

This project enforces strict modelling discipline to prevent common analytical errors:

- **No Sum-of-Parts Fantasy:** Baseline revenues use observed, blended market actuals, not theoretical maximums of stacked products.
- **Behavioural Separation:** Behind-the-meter savings are explicitly separated into *continuous* (DUoS), *step-function* (TNUoS ASC Band Step), and *partial residual* mechanisms. They are never blended into a single misleading total.
- **Explicit Omissions:** Known costs (e.g., augmentation CAPEX) and synthetic inputs (e.g., illustrative price shapes) are explicitly flagged in the Assumptions Ledger of every synthesis script.
- **Mechanism Before Model:** Every model result is attached to a physical or economic mechanism. A model that cannot explain the sign of the effect is not ready for policy use.
- **Physics Before Economics:** Physical feasibility and system need are established before economic conclusions are drawn.
- **Zero Look-Ahead Bias:** No variable uses information unavailable at the decision timestamp.

This project follows a rigorous, adversarial-review-driven research methodology. The full methodology is available on request.

---

## Licence

- **Code:** MIT License
- **Documentation & Data:** CC BY 4.0

*This framework is provided as an open-source public good to elevate the standard of evidence in AI infrastructure planning.*