# Stage 6: Two Archetypes, One Grid — Inference Siting in the Central Belt

**Part of the Scotland AI Split-Zones programme.** Stages 1–5 built and validated a model of a 100MW AI training site in export-constrained Northern Scotland. Stage 6 asks the question that thesis leaves open: what does the *other* kind of AI data centre — inference, not training; import-pressured, not export-constrained — actually face when it connects to the grid?

The short answer: a different network-charge regime, a different regulatory threshold structure, and a genuinely different relationship between compute inflexibility and grid value than the training-site literature assumes. This document sets out what Stage 6 found, how confident each finding is, and what it means for Ofgem's live *Curate* connections reform consultation.

---

## Two Archetypes, Not a Census

This is worth stating plainly before anything else: Stage 6, like Stage 5 before it, models **one representative site**, not a survey of Scottish data centres. Stage 5's 100MW/132kV training site and Stage 6's 5MW/HV inference site are **paired archetypes** — chosen because they sit at structurally opposite points on two axes that matter (workload type, connection voltage, constraint direction), not because they're statistically typical of the full range of proposed developments.

That's a deliberate methodological choice, not a limitation to apologise for. The Central Belt alone has at least 11 proposed hyperscale data centres ranging from 200MW to 550MW — none of which Stage 6 claims to represent. The value of an archetype study isn't coverage; it's showing *why* two sites this different can't be treated as the same regulatory problem, which a broader-but-shallower survey would struggle to demonstrate as cleanly. Where this document draws conclusions that would need revisiting at other scales — and there are some — it says so explicitly rather than letting the archetype quietly stand in for the general case.

## Why the Battery Still Matters for an "Inflexible" Load

Stage 1 classified inference as the less flexible of the two workload types — true, and worth being precise about *what kind* of flexibility that claim covers. An inference workload can't be paused or rescheduled the way a training run can; requests have to be served when they arrive. But that's flexibility at the **compute layer**. A site's **grid import profile** is a different thing entirely, and it can still be shaped by a co-located battery regardless of whether the workload underneath it is flexible.

This distinction turns out to matter more than expected. Because inference load doesn't have the idle troughs a schedulable training workload can have, its daily demand curve barely dips — even overnight, Stage 6's modelled site never drops below 80% of peak capacity. That's exactly the property that ruled inference out of Stage 3–4's constraint-avoidance mechanism, and exactly what makes battery-driven peak-shaving *more* reliable here than it was for the training site. Continuous, inflexible demand isn't an obstacle to network-firming value — it's what makes the mechanism dependable.

## Finding One: Network Charges Run in the Opposite Direction

Stage 5's training site sat at 132kV/EHV — a hyperscale transmission connection that pays minimal local distribution charges. Stage 6's inference site sits at HV, much closer to the distribution network it actually uses, and pays accordingly.

The DUoS Red–Green differential — the value available to a battery shifting load out of peak pricing periods — is **£43.67/MWh** at HV, against Stage 5's **£1.58/MWh** at EHV. That's not a rounding difference; it's **27.6 times larger**, and it runs in the direction most people wouldn't guess: smaller, lower-voltage sites face materially higher network-charge exposure per MWh than the hyperscale sites usually assumed to be the harder case.

Realised against an evidence-based load profile — timed and shaped from measured generative-AI inference power data, not assumed — this comes to **£119,547 a year, gross**, for a battery sized at half the site's capacity. Net of round-trip losses, that figure barely moves, landing at £119,498 — but only because the battery charges during cheap off-peak periods. If that discipline slips even one tariff band, the picture changes fast: charging during Amber periods cuts net value to 92% of gross, and charging during Red periods turns the mechanism **loss-making**, not merely less profitable. The finding here isn't just a number — it's that the economics depend on operational discipline, not just battery hardware.

TNUoS tells a related but distinct story. Since 2023, the demand residual charge is banded purely by capacity, the same nationwide regardless of location. A 5MW site converts to roughly 5,263kVA, comfortably inside the top band — **£193,053 a year**. Stage 5 found a step-function mechanism at this same charge for the training site: dropping to a lower band via a formal capacity reduction can cut the bill sharply. For this inference site, that mechanism turns out not to be available. Every lower band's ceiling sits below the site's own minimum demand — its quietest overnight hour still draws 4.0MW, well above what even the next band down would allow. Where Stage 5's training site had genuine room to step down, this site's defining property — a narrow gap between its trough and its peak, the same property that makes its battery economics reliable in Finding One — leaves no lower band within reach. The full £193,053 is simply the cost of connecting a site whose demand never really varies.

## Finding Two: Is the Commitment Fee Proportionate?

Ofgem's proposed data centre commitment fee — 2.5–7.5% of capital cost, applied to projects at or above 40MW — is designed to filter speculative connection requests from genuine ones. Tested against a real, verified 40MW site (DataVita DV1's confirmed expansion target) and Ofgem's own published capital-cost data for similarly-sized projects in the connections queue, the fee comes out at **1.75–7.09% of capex** — inside, or very close to, Ofgem's own stated target.

That's a genuinely useful result for a consultation response, even though it isn't a dramatic one. It means Stage 6 can tell Ofgem their own instrument checks out against their own evidence, rather than manufacturing a grievance the numbers don't support. Notably, this conclusion holds regardless of a definitional ambiguity in the underlying data — whether "40MW" refers to a site's IT capacity or its grid connection capacity, which can differ by 15–20% for a typical facility — because the fee and the capex benchmark both scale linearly with site size, so the ratio between them is unaffected by which reading is used.

## Finding Three: Where This Actually Fits in Ofgem's Reform Programme

This is the strategic centre of Stage 6, and it's a more useful contribution than either of the numerical findings above.

Ofgem's *Curate* consultation asks four things of a data centre project — a compute offtaker, evidence of long-lead procurement, financial capability, technical design certification — and every one of them answers the same question: **will this project actually get built?** None of them ask whether it's a *good use of the grid capacity it's requesting*. That's a different question, and Stage 6's evidence — the constraint-direction thesis, the network-firming mechanism, the voltage-tier economics — speaks directly to it.

Ofgem hasn't ignored this. A separate, earlier-stage workstream — **Connect Operate**, supported by a newly-formed Flex Technical Taskforce — is explicitly tasked with exactly this question, and has already arrived independently at part of Stage 1's own thesis: that a data centre's flexibility depends on its workload type, and that siting solutions need to account for location-specific network conditions. The Curate consultation and the Connect Operate workstream are asking genuinely different questions, on different timelines, about the same population of projects.

That creates a coordination gap worth naming directly: Curate closes for responses well before Connect Operate's evidence base is developed. Evidence like Stage 6's — real, quantified, site-specific — risks having nowhere to land in the interim. The right ask isn't a new Curate milestone; Curate's viability-only scope is coherent as designed, and arguing against it would be picking the wrong fight. The better ask is a lightweight route for grid-value evidence to reach Connect Operate and the Flex Technical Taskforce without waiting for a formal consultation vehicle that doesn't exist yet.

## Reproducing This Work

Every figure in this document is computed, not typed — running the notebook below from a clean checkout should reproduce all five charts and pass every embedded check.

- **Modules:** `scripts/duos_central_belt.py`, `scripts/tnuos_central_belt.py`, `scripts/capex_central_belt.py`, `scripts/inference_load_central_belt.py` — each independently runnable, each printing its own sourcing and assumptions.
- **Notebook:** `notebooks/10_stage6_central_belt_synthesis.ipynb` — narrated, executable, produces all five figures inline.
- **Figures:** `figures/10_1` through `10_5` — the standalone chart exports.
- **Full working record:** `STAGE6_SYNTHESIS.md` — every finding above, with complete sourcing, the correction history where findings were revised, and a line-by-line Assumptions Ledger. Read this alongside the notebook for anything you intend to rely on, cite, or challenge.

## Scope and What Would Strengthen This Further

Consistent with the archetype framing above, a few things would need attention before generalising beyond the two sites modelled here:

- **The inference site's own scale is an assumption, not a confirmed fact.** Whether its "5.0MW" figure represents IT load or grid import capacity isn't settled in the available source data; if it's IT load, the site's true grid draw — and this document's DUoS figure — could be meaningfully larger.
- **The Central Belt's local network conditions** are evidenced through documented demand clustering (11+ proposed large sites) rather than current, substation-specific capacity data, which sits behind an interactive tool this stage hasn't queried directly.
- **The TNUoS saving's exact capture mechanism** — the specific link between a distribution capacity reduction and system-operator band reassignment — would benefit from direct confirmation with network operator documentation before being treated as certain.

None of these affect the two headline conclusions that matter most for the consultation: that network charges and regulatory thresholds behave differently for smaller, differently-sited data centres than the reform package's uniform framework assumes, and that Ofgem's own programme structure already has a home for this evidence — it just doesn't yet have a route to get there in time.