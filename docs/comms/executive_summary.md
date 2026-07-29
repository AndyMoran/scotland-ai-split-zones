# Executive Summary: A Constraint-Direction Siting Framework for AI Data Centres in Scotland

To: Scottish Government, Local Planning Authorities, and Energy System Regulators

From: Andy Graham Moran (Independent Researcher -  Heaviside Analytics)

Subject: Strategic Siting of AI Infrastructure via Constraint-Direction Computing

## The Bottom Line
Current UK and Scottish policy treats "AI data centres" as a single category of fixed grid burden. This is a strategic error. AI compute is not a monolith. By classifying AI workloads by Constraint Direction—rather than just total MW demand—Scotland can turn flexible AI training into a grid asset that absorbs wasted renewable energy, while protecting local grids from inflexible inference loads.

## 1. The Problem: Treating AI as a Monolith

The UK Government’s AI Growth Zone programme and the Scottish Government’s AI Strategy both identify electricity connections as the primary blocker for AI infrastructure. However, current planning frameworks evaluate data centres based on geography and total peak demand, ignoring the distinct physics of the workloads inside them.

This leads to two structural risks:

1.	Overloading Import-Constrained Grids: Siting massive, inflexible AI campuses in the Central Lowlands adds severe stress to local grids, risking stranded public assets (socialised grid upgrade costs) if future algorithmic efficiency drastically reduces power demand.
2.	Wasting Export-Constrained Renewables: Failing to site flexible AI in the North misses a massive opportunity to use compute as "renewable absorption demand," consuming wind power that would otherwise be curtailed due to full transmission lines.
  
## 2. The Solution: Constraint-Direction Siting

We propose a bifurcated siting framework that matches the physical characteristics of the AI workload to the specific constraint profile of the local grid.

### Workload A: Flexible AI Training (e.g., Large Language Models)
·	Characteristics: Power-hungry, runs for weeks, but can be paused and restarted with sufficient notice.
·	Optimal Siting: Export-constrained, renewable-rich zones (e.g., Peterhead, Caithness, SSEN-N).
·	Grid Function: Acts as a strategic demand sink. It absorbs trapped renewable power, reducing curtailment costs for consumers without requiring expensive new transmission lines.

### Workload B: Latency-Sensitive Inference (e.g., Real-time AI services)
·	Characteristics: Requires instant, uninterrupted response; cannot be paused.
·	Optimal Siting: Import-constrained zones near users, fibre networks, universities, and public services (e.g., The Central Lowlands, Lanarkshire AI Growth Zone).
·	Grid Function: Requires firm capacity. Must be designed to minimise residual grid burden through local storage, private-wire renewables, or tenant-safe Virtual Power Plant (VPP) support.

## 3. The Evidence: Stage 2 Empirical Findings
We tested the "timescale mismatch" hypothesis—the industry assumption that AI cannot pause and restart fast enough to help the grid—against real 2023-24 National Energy System Operator (NESO) constraint data for Scotland.

**Finding 1:** The Timescale Mismatch is Resolved
Median Scottish export constraint events last 1.5 to 2.0 hours. Modern hyperscaler IT infrastructure (using asynchronous checkpointing and automated orchestration) can pause and restart in approximately 1 hour. Therefore, modern AI training is temporally compatible with grid constraint events.

**Finding 2:** The Scale of the Opportunity
Using a cost-proportion allocation of NESO’s outturn thermal constraint data (strictly filtered for 2023-2024 historical periods), we estimate Scotland’s annual constraint volume at ~1.76 TWh/year. This represents a **theoretical upper bound of ~£290M per year** in avoided constraint costs if flexible AI were perfectly dispatched to absorb these events.

**Finding 3:** Compatibility is NOT Capture
The £500M figure is a theoretical ceiling, not guaranteed revenue. Real-world capture is materially lower due to:
·	Physical Incompatibility: Short-duration grid events (under 1 hour) remain physically incompatible with large-scale AI response.
·	AI-Operator Friction Costs: Pausing a training run incurs real costs for the operator (e.g., idle GPU amortization, checkpoint overhead). Flexibility only makes economic sense if grid compensation exceeds these friction costs.

**Finding 4:** Symmetric Stranded-Asset Risk Hard-allocating 500 MW of firm grid capacity in the Lowlands for AI carries severe stranded-asset risk for ratepayers. Conversely, Jevons paradox suggests that as AI compute becomes cheaper and more efficient, total demand may actually increase, potentially leaving infrastructure undersized rather than stranded. This uncertainty strongly favours flexible, non-firm connection agreements over hard-allocated capacity.

## 4. Policy Recommendations
To implement Constraint-Direction Siting, we recommend three immediate policy interventions:

1.	**Bifurcate Planning Conditions:** Planning authorities should explicitly distinguish between "Training" and "Inference" workloads in AI Growth Zone approvals. Training sites in export-constrained zones should be required to demonstrate modern orchestration and checkpointing capabilities.

2.	**Mandate Non-Firm Connections for Training:** Flexible AI training hubs in renewable-surplus zones should be granted accelerated connections via non-firm or flexible agreements. This protects ratepayers from stranded network asset risk while allowing sites to absorb curtailed renewables.

3.	**Broaden Public Benefit Tests:** Acknowledge that this framework addresses grid constraint direction only. Comprehensive site approvals must still rigorously assess water stress, community acceptance, and local planning impacts, which are not modelled by this framework.

**Conclusion:** AI data centres do not have to be a burden on the Scottish grid. By aligning the physics of the workload with the physics of the grid, Scotland can lead the world in grid-responsive AI infrastructure.


Public Good
Open Source:
·	MIT License
·	Documentation: CC BY 4.0
·	https://github.com/AndyMoran/scotland-ai-split-zones
·	https://www.linkedin.com/in/andy-graham-moran/
·	andrewgmoran@gmail.com

