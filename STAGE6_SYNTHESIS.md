# Stage 6: Central Belt Inference Siting — Behind-the-Meter Economics and Commitment Fee Proportionality

**Status:** In progress — core modules grounded, submission text not yet drafted
**Consultation target:** Ofgem, *Proposed data centre connection reforms* (published 29 July 2026, deadline 16 September 2026)
**Companion stage:** Extends Stage 1's constraint-direction thesis and Stages 4-5's behind-the-meter methodology from the export-constrained training site to a Central Belt inference site facing local distribution demand-headroom pressure (see "Constraint Direction" note below for what this does and doesn't claim).

---

## The Core Thesis

Stage 4-5 modelled a 100MW AI training site at 132kV/EHV in export-constrained Northern Scotland. This stage models the structural opposite: a 5MW inference site at HV in the Central Belt — see the note below on what "import-constrained" means here and doesn't. The two sites are not a large version and a small version of the same asset — they sit in different network charge regimes, face different constraint directions, and warrant different regulatory treatment. Ofgem's proposed connections reforms apply a single fee-and-milestone framework across all data centre scales; this stage tests whether that framework holds up against a real site of this class.

## Constraint Direction: What "Import-Constrained" Means Here, and What It Doesn't

Flagged by external review, and it caught something real: "import-constrained" was inherited framing from Stage 1, used throughout Stage 6 without being checked against current evidence. It needed checking, and checking it surfaced a genuine complication worth stating precisely rather than smoothing over.

**The complication:** Scotland is a *net exporter* of electricity — 21TWh in 2024, the majority flowing south to England. Industry commentary (Addleshaw Goddard, 2025) describes Scotland's dominant grid problem as *transmission* congestion moving remote renewable generation to demand centres, not a national shortage of import capacity. Read carelessly, "the Central Belt is import-constrained" could sound like it contradicts this. It doesn't, but the reason why needs to be stated, not assumed.

**The distinction that resolves it:** national export/import balance and local distribution headroom are different things, at different network levels. Scotland exporting power overall doesn't mean every distribution substation in the Central Belt has spare capacity to connect new large loads — those are separate questions, answered by different data (national transmission flows vs local GSP/primary substation headroom). The claim this stage actually needs is the local one: does the Central Belt have enough *local distribution* headroom for new demand connections, independent of the national picture.

**What's genuinely evidenced for the local claim:** real, concentrated demand pressure. At least 11 hyperscale data centre projects (200-550MW each) are proposed across Central Scotland and neighbouring council areas — Edinburgh (x2), North Lanarkshire (x2), Fife, West Lothian, East Dunbartonshire, South Lanarkshire, and others — with aggregate proposed capacity estimated above 4.8GW, a material concentration of proposed new demand in the region (Action to Protect Rural Scotland / DCD reporting, June 2026). The source article itself frames this as "more than double Scotland's overall energy usage" — worth flagging that comparison as a unit mismatch (GW is power capacity; "energy usage" is normally TWh/year) rather than repeating it uncritically; the scale point stands without needing that comparison. That's genuine, documented demand clustering in exactly the area Stage 6 models. SP Distribution's own 2021 Network Capacity Headroom Report shows planned reinforcement work specifically in the Livingston/Bathgate corridor (Kirknewton substation upgrade, unbanking the Livingston East–Bathgate GSP interconnector) — evidence of pre-existing local capacity pressure in the immediate area of the Asanti Livingston anchor, though this predates the current data centre demand surge by several years and can't be read as confirming *current* headroom status.

**What's not confirmed, and shouldn't be assumed:** current, quantified, substation-specific headroom figures for the Livingston/Bathgate or Chapelhall areas specifically. SP Distribution publishes this data through an interactive online tool (heat maps, embedded capacity register), not as a static document this stage has been able to pull structured data from. The 2021 NCHR is a methodology document, not current numbers — treating it as confirming today's headroom status would repeat exactly the kind of dated-data error this project has caught in its own earlier stages.

**Revised framing for this stage:** "import-constrained" should be read as *local distribution demand-headroom pressure from clustered new connections*, not a claim about Scotland's national import/export balance — the two are genuinely different mechanisms, and only the first is well-evidenced here. Any submission text drawing on this should state that distinction explicitly rather than use "import-constrained" as an unqualified label a technical reader could reasonably push back on.

## What This Stage Does Not Do

Consistent with the project's scope discipline: this stage does not model workload-level flexibility for inference (inference load is "mostly inflexible" per Stage 1's own workload taxonomy — see Mechanism Note below). It does not model a specific named facility's actual finances; Asanti Livingston is used as a **real, verified capacity anchor**, not as a claim about that company's own economics. It does not yet include the TNUoS locational (Triad/HH) component, which NESO's own documentation confirms is a smaller addition on top of the residual charge modelled here.

---

## MW Basis: A Definitional Note

Flagged by external review, and worth being precise about rather than treating "MW" as one uncontested number throughout this document.

**Convention used in this stage:** "MW" means grid import capacity / agreed capacity (MIC), not IT load, unless stated otherwise. This is a deliberate choice, not a default: DUoS, TNUoS, and MIC-based mechanisms all attach to what a site draws from the network, not to its compute capacity. IT load and grid import capacity are different quantities, related by PUE (Power Usage Effectiveness) — a site with X MW of IT load typically needs more than X MW of grid connection to also cover cooling and facility overhead.

**Ofgem's own two thresholds appear to use different bases from each other** — worth naming plainly rather than assuming consistency. The milestone framework's 10MW threshold is explicitly labelled *"a threshold of a rated IT load of 10 MW"* (consultation para 7.4). The commitment fee's 40MW threshold is never given an equivalently explicit label, but the surrounding language — *"a data centre with a requested connection of 100 MW"* (para 4.1), *"contracted capacities ranging from 1 MW to over 1500 MW"* (para 5.4) — reads as grid connection capacity. If that reading is right, the two thresholds this stage discusses are measured on different bases, and any comparison across them needs to say so explicitly rather than treat "MW" as a single consistent unit.

**This is worth elevating into an explicit consultation ask, not just a modelling caveat.** IT load and grid import capacity can differ materially because of PUE, cooling design, and resilience margins — DataVita DV1's own figures below show a ~7.2MW gap between the two readings at a single site. A framework that measures different thresholds on different bases creates avoidable ambiguity, and potentially a boundary-gaming incentive (sizing a declared capacity just under whichever threshold uses the more favourable basis). The ask: Ofgem should either define both thresholds on the same capacity basis, or publish an explicit IT-load-to-grid-import conversion rule for threshold purposes. This is a proportionate drafting-clarity ask, not an objection to the reform itself — it doesn't require opposing anything Ofgem has proposed, just asking them to close a gap in how they've specified it.

**DataVita DV1 — threshold scope confirmed, capacity basis estimated.** An industry report (New Project Media, January 2026) states the expansion explicitly: *"the developer had received planning permission... to further expand the facility's IT capacity to 40 MW."* That's IT load. DV1's own stated PUE is 1.18, giving an estimated grid import capacity of ≈40 × 1.18 ≈ **47.2MW**. This strengthens Finding 3, not weakens it: DV1 clears the 40MW fee threshold whether the threshold is read as IT load (40MW ≥ 40MW) or grid capacity (≈47.2MW ≥ 40MW). It was never a marginal boundary case under either reading — though whether the stated 40MW figure is itself final, and whether the project would trigger a Transmission Entry Assessment, remain open questions tracked in the Assumptions Ledger, not settled by this finding.

**Asanti Livingston — genuinely unresolved, not assumed away.** No source states whether the "5.0MW" figure used throughout Findings 1 and 2 is IT load or grid capacity. What's known: the facility's PUE is reported as 1.67 (DCD) or 1.4 (Asanti's own site) — a minor inconsistency in the underlying source data, worth noting on its own. If "5.0MW" is IT load rather than grid capacity, true grid import could be **7.0-8.35MW** using those two PUE figures, not 5.0MW. This stage treats "5.0MW" as grid import capacity throughout — the quantity the DUoS/TNUoS/battery mechanics actually operate on — as an explicit modelling choice, not a confirmed fact about the site. The practical consequences differ by finding:

- **Finding 2 (TNUoS band assignment) is robust to this either way.** Even at the low end of the 5.0MW reading, the site clears HV4's 2,000kVA threshold by a wide margin; if the true figure is closer to 7-8.35MW, the conclusion only strengthens.
- **Finding 1 (the £119,547/year DUoS figure) is not robust to this.** That figure, and the battery sizing behind it, scale directly with the site capacity assumption. If true grid import is 7-8.35MW rather than 5.0MW, the site-appropriate battery and DUoS value would both be larger — this stage's headline figure should be read as conditional on the 5.0MW-as-grid-capacity assumption, not as a fact independent of it.

---

## Mechanism Note: Why a Battery Still Belongs in an "Inflexible Workload" Site

Stage 3-4's AI constraint-avoidance mechanism required the **workload itself** to pause and resume — that is training-specific, and does not transfer to inference. But Stage 5's DUoS, TNUoS ASC Band Step, and wholesale peak-shaving mechanisms are **battery-driven, not workload-driven**: they require predictable peak demand and battery capacity to shave it, not an IT load that can stop and start. An inference site's compute is inflexible in *when it runs*, but its power draw still has a daily shape a battery can smooth regardless of workload behaviour.

**Operating assumption for this stage:** a co-located peak-shaving battery carries over from Stage 5's mechanism set; the bilateral AI-constraint-avoidance mechanism from Stage 3-4 does not. This is itself a finding, not just a scoping note — it demonstrates that the constraint-direction framework distinguishes mechanisms by *what physically enables them*, not by asset class alone.

---

## Finding 1: DUoS Value Runs the Opposite Direction from Stage 5 — and the Realised Annual Figure Now Closes

**£43.67/MWh** is the DUoS Red-Green differential for a representative HV-connected Central Belt inference site, against SP Distribution's real Annex 1 tariffs (Red £43.77/MWh, Green £0.10/MWh, HV Site Specific No Residual band, effective 1 April 2026). This is **27.6 times larger** than Stage 5's £1.58/MWh differential for the 100MW/132kV/EHV training site.

**Mechanism:** DUoS scales down with voltage, not down with load. Hyperscale EHV sites impose minimal local distribution losses and pay correspondingly little for them; HV-connected sites sit closer to the distribution network they use and pay the fuller rate for it. This is physics, not a modelling artefact — the same structural relationship Stage 5 identified from the other end of the voltage scale.

**Realised annual value: £119,547/year gross**, for a 2.5MW battery (50% of the 5MW site's capacity, mirroring Stage 4/5's ratio) discharging across the DUoS Red band (16:30-19:30, three hours daily per SP Distribution's Annex 1 time bands). "Gross" is the operative word — flagged by external review, and worth being precise about rather than letting a reader assume this is a net commercial return. This required a load profile — deliberately built as a diurnal curve, not a scaled-down copy of Stage 5's training-spike shape, since inference has no scheduled job starts to spike around. The curve's timing (ramp from ~08:00, peak 16:00-19:00, decline from ~22:00) and magnitude (25% peak-to-trough power variation) are both anchored to published measurements, not invented — see `inference_load_central_belt.py::PROFILE_EVIDENCE` for the full sourcing, including the explicit decision not to use request-volume variability figures (~10x), which measure a different quantity than power draw and would have overstated the shavable peak.

**Battery sizing needs MWh, not just MW.** A "2.5MW battery" says nothing about whether it can sustain three hours of discharge — that depends on installed energy capacity, not power rating. Minimum usable capacity: 2.5MW × 3h = **7.5MWh**, before losses and before any SOC reserve or degradation margin. Installed nameplate capacity would need headroom above that; this stage doesn't quantify how much, since that requires a specific battery chemistry and degradation curve it doesn't model.

**Net value, computed rather than asserted:** at 85% round-trip efficiency (reusing Stage 3's established figure for this project, not a new assumption), delivering 7.5MWh of discharge requires 8.82MWh of charging input. If that charging happens during Green periods (£0.10/MWh — cheap enough that the loss barely registers), net value is **£119,498/year — 99.96% of gross**. But this is charging-discipline-dependent, not a free pass: if charging slips into Amber (£3.22/MWh), net drops to **£109,450/year (91.6% of gross)**; if it slips into Red, the mechanism goes **negative** (round-trip losses bought back at the same rate they're sold at guarantee a loss). Gross ≈ net only because the operational discipline of charging in Green is maintained — that's a real operating requirement for anyone deploying this, not an incidental detail.

**What if the site is actually larger than 5.0MW — the Asanti MW-basis sensitivity, made concrete.** The MW Basis note above states qualitatively that grid import could be 7.0-8.35MW if "5.0MW" is IT load, not grid capacity. Scaled through the same model (battery at 50% of site capacity, same Red-band discharge): indicative gross DUoS value would be **≈£167,000-£200,000/year**, not £119,547 — a genuinely different scale of finding, not a rounding difference. This doesn't change the mechanism, only its size; it's included here so the £119,547 figure isn't read as site-independent when it demonstrably isn't.

**A genuine finding, not just a filled-in gap:** the battery coverage check confirms site load never drops below 4.0MW even at its overnight trough (80% of site capacity) — comfortably above the 2.5MW battery rating throughout the Red band, with no shortfall periods. This is a *more* robust mechanism than Stage 4/5 needed to establish for the training site, precisely because inference load doesn't have the idle troughs a schedulable training workload can have. Continuous, inflexible demand — the property that ruled inference out of the Stage 3-4 constraint-avoidance mechanism — is exactly what makes the peak-shaving mechanism reliable here.

**Scope boundary:** this covers Red-band discharge and its associated Green-period recharge cost. It does not include battery degradation, availability losses, financing costs, or SOC reserve margins beyond the minimum stated above.

**Caveat:** the "No Residual" DUoS band was used as the conservative floor; a real site would be allocated to one of four residual charging bands (0-4) based on its consumption profile, which could move this figure in either direction. The 25% peak-to-trough magnitude sits within a measured range of 15-34% (Meta, Google, and the source study's own workload) — the specific choice within that range is a stated, not hidden, assumption.

## Finding 2: TNUoS — A 5MW Site Sits Unambiguously in the Top HV Band

A 5MW HV-connected site (≈5,263 kVA at 0.95 power factor) sits comfortably above the HV4 lower threshold (2,000 kVA) under NESO's RIIO-ET3 banding, locked for 2026/27-2030/31 — approximately **2.63 times** that threshold, not the "~10 times" stated in an earlier version of this document (that figure mistakenly compared the site's kVA against HV1's *upper* bound, 500kVA, rather than HV4's actual *lower* bound, 2,000kVA — an external review caught this). The band assignment itself was never in doubt; only that multiplier was wrong. This is not a marginal band-boundary judgement call. The site's TNUoS demand residual is **£528.91/site/day → £193,053/year** (NESO Final TNUoS Tariffs 2026/27, Table 10).

**Mechanism:** identical in kind to Stage 5's ASC Band Step — a step-function saving available only through a formal, sustained capacity reduction agreed with the DNO, not through opportunistic dispatch. NESO's own text confirms the charge is genuinely non-locational: "all sites within the same band pay the same demand residual tariff regardless of which demand zone they are in."

**Numbers, and a correction that matters more than the original claim did.** The tariff table alone shows a single-step saving (HV4→HV3) of £125,375/year, and a maximum theoretical saving (HV4→HV1) of £181,432/year. **Neither is actually available to this site**, and reporting them without checking that was a real error, not a hedge that needed adding — caught in conversation, not by either prior review. Every lower band's ceiling sits below this site's own minimum load: HV3 tops out at roughly 1.90MW (at 0.95 power factor), but the site's own overnight trough — its quietest possible moment, from the load profile behind Finding 1 — never drops below 4.0MW. HV2 and HV1 are further out of reach again. **HV4 isn't a starting point with room to improve for this site. It's the only band this site's real load profile can ever occupy.** The mechanism itself is real — it's the same step-function logic as Stage 5's £1.8M EHV finding — but mechanism and availability are different questions, and this finding conflated them. A site with more headroom between its floor demand and a lower band's ceiling could genuinely capture this; this specific archetype, defined by its narrow trough-to-peak range, structurally cannot. That narrow range is exactly what made Finding 1's DUoS mechanism *more* reliable — the same property cuts the other way here.

**Denominator:** these figures are per 5MW site. They do not scale linearly with capacity — the band thresholds are fixed points, so a site's position relative to a threshold matters more than its raw size.

**Capture route — who actually realises the saving, and how.** This wasn't specified in the first version of this finding, and it should have been; an external review caught the gap. NESO states plainly who TNUoS applies to: Generators, Suppliers, and directly-connected transmission demand — not distribution-connected demand sites themselves. A 5MW HV site connected via SP Distribution is a standard distribution-connected customer, not directly-connected transmission demand, so the site does not have a direct billing relationship with NESO for this charge. The mechanism runs in three steps, and a second review caught that one of them was overstated as confirmed when it wasn't: (1) the site formally reduces its agreed capacity (MIC) with SP Distribution — a real, documented process already covered in Stage 6's DUoS module (SP Distribution's charging statement, §2.36-2.47) — **confirmed**; (2) that capacity re-banding determines which TNUoS demand residual band the site sits in — **not actually confirmed**; NESO's own text establishes that bands are based on "capacity," but doesn't specify whether that means the DNO-agreed MIC specifically, versus metered demand or another reported figure, so this link is inferred from adjacent facts rather than sourced directly; (3) the saving reaches the site through its **commercial electricity supply contract**, not a direct NESO relationship — **plausible, not sourced**. Most UK business supply contracts treat TNUoS as a pass-through cost that moves with the underlying charge — including many contracts marketed as "fixed," where TNUoS specifically is still allowed to float — so the saving typically does reach the site, but the speed and certainty of that pass-through depends on the specific contract in place, not on the band-step mechanism itself. **Given the feasibility finding above, this entire capture-route mechanism is currently moot for this specific site — there's no saving to capture. It's preserved here because the mechanism is real for the archetype in general, and remains directly relevant to any site whose minimum load sits closer to a lower band's ceiling.**

**A practical constraint worth naming for the mechanism in general, even though it doesn't apply to this specific site:** a formal capacity reduction lowers the site's contractual headroom, not just its charges. For an inference site with uptime obligations, any MIC reduction needs to remain compatible with resilience and redundancy requirements — if the co-located battery is unavailable (maintenance, depleted state of charge), the site's actual import could exceed its newly-reduced contracted capacity unless other controls are in place. The band-step saving and the site's operational resilience margin are in tension, not independent — worth carrying forward for any future site where the step-down is actually reachable.

## Finding 3, Corrected: The Fee Is Reasonably Proportionate — The Original Finding Didn't Survive Its Own Errors

The first version of this finding was wrong in two compounding ways, both now fixed rather than patched.

**Error 1: the site anchor was out of scope.** Asanti Livingston (5MW) sits below the commitment fee's own 40MW threshold (consultation para 5.1, 5.4). The fee would never apply to it. Calculating a proportionality ratio for a site the instrument doesn't touch isn't a minor imprecision — it's analysing the wrong thing entirely.

**Error 2: the capex benchmark was the wrong source.** The original figure ($7-12M/MW) came from international brownfield-retrofit literature (Terrapin CG, QTS-style figures). Ofgem's own consultation document publishes real GB queue capex by project size, drawn from NESO's mandatory information request and a DNO voluntary request (Tables 3 and 4) — a strictly better source for this exact question than a general international benchmark.

**Corrected finding, using DataVita DV1 (40MW IT capacity, ≈47.2MW estimated grid capacity at its own stated PUE — see MW Basis note above; clears the fee threshold under either reading) against Ofgem's own Table 4 (DNO data), Medium 10-50MW band (n=8 projects):**

| Statistic | Capex/MW | Fee as % of capex |
|---|---|---|
| Median | £10,051,053 | 2.36% – 7.09% |
| Mean | £13,541,800 | 1.75% – 5.26% |

Both estimates fall within, or very close to, Ofgem's own stated 2.5-7.5% target range. **The original claim — that the fee overshoots its proportionality target for smaller, brownfield-class sites — does not survive correction.** Using the right site and Ofgem's own evidence, the fee looks reasonably well-calibrated for this asset class, not disproportionate.

**On whether 40MW itself is in scope — this is confirmed, not assumed.** The consultation states the threshold twice in identical language: *"The data centre commitment fee would be applied to projects that have a capacity equal to or above 40 MW"* (para 5.1), repeated at Question 12. "Equal to or above" is inclusive — a 40MW project is in scope, not a boundary case sitting just outside it. DataVita DV1's expansion target is a genuine, direct application of the fee, not a hypothetical.

**On whether the proportionality calculation should use 40MW (IT load) or ≈47.2MW (estimated grid capacity) as the denominator — checked directly rather than assumed either way.** It doesn't matter, and this is worth showing rather than asserting: both the commitment fee (a flat £/MW rate) and the capex benchmark (also a flat £/MW rate) scale linearly with site MW, so the site-size term cancels out of the ratio entirely. Computed directly: fee-to-capex percentage is **2.3629% at 40MW and 2.3629% at 47.2MW** — identical to four decimal places, not approximately similar. This holds because the model has no internal banding or non-linearity within the fee's scope — a genuinely different situation from, say, the TNUoS band-step mechanism, where crossing a threshold changes the outcome discontinuously. The finding is robust to the MW-basis question by construction, not by having picked the more favourable number.

**Why report a correction that undermines the original argument, rather than quietly dropping Finding 3?** Because the point of this project's discipline has never been "find problems with the consultation" — it's "find out what's actually true and report it, whichever direction that cuts." A wrong finding that happened to support a critical stance would be exactly as much of a failure as a wrong finding that happened to support the opposite. This one just turned out to run the other way once checked properly.

**Mechanism, restated correctly:** Ofgem's own methodology (para 4.12) derives its £9.5M/MW average using a median-based approach specifically to manage outlier risk in a small dataset. The Medium band's n=8 sample is itself small enough that its estimate carries real uncertainty — visible in the mean/median spread above (£13.5M vs £10.1M/MW) — but that uncertainty runs in both directions, not systematically toward "the fee is too high for this class of site."

**Scope boundary:** this correction addresses the fee-proportionality question specifically. It says nothing about whether 40MW is the right threshold, whether DataVita DV1 specifically would trigger a Transmission Entry Assessment (which would put it under NESO's process rather than the DNO dataset used here — unconfirmed), or whether other size bands would show a different picture. Table 4's Small band (0-10MW, n=7) shows a much higher mean (£27M/MW) than median (£9.5M/MW) — a genuinely volatile small sample that a future stage could examine, but that's a different site class from the one this finding now covers.

**Caveat:** n=8 is a small sample for the Medium band specifically. Ofgem's own document treats this as usable evidence (it's their own published table), but a single additional outlier project could shift the mean substantially. The median is more robust to this and is the figure this finding leans on.

---

## Finding 4: The Milestone Argument, Revised — Flexibility Wasn't Rejected, It Was Routed Elsewhere

The account in the first version of this finding was accurate as far as the Curate consultation goes, but incomplete in a way that matters. Ofgem's own *Connect Update: Demand Connections Reform* (16 June 2026) — published alongside the summary of Call for Input responses referenced in Curate chapter 6 — shows that "flexibility-based readiness criteria" wasn't judged unimportant. It was deliberately routed out of Curate and into a separate, still-forming workstream called **Connect Operate**, which is explicitly, actively seeking exactly the evidence Stage 6 has been building.

**The reframe, precisely:** Curate tests *is this project real* (compute offtaker, procurement, financial capability, technical design certification — four objective, documentary tests). Connect Operate is tasked with *is this project good for the grid* — flexibility, alternative connection agreements, siting-specific impact. These are genuinely different questions, and Ofgem has split them across two pillars of the same reform programme rather than folding one into the other. That's a more coherent design than "they rejected the idea," and it changes where Stage 6's evidence actually belongs.

**Connect Operate has already arrived, independently, at part of Stage 1's own thesis.** From the Connect Update itself:

> "Feedback from stakeholder engagement is that data centre's ability to operate flexibly is dependent on their use and business model. For example, an AI training data centre may be more capable of flexible operation than cloud data centres." (para 3.19)

That is the training-vs-inference half of the constraint-direction thesis, in Ofgem's own words, already shaping live policy — not something Stage 6 needs to introduce from scratch. And the next paragraph names the other half directly: the plan is to "identify solutions that may be appropriate for specific types of development, considering location specific network and site challenges" (para 3.21) — the site-typology half.

**There's a named, live body this could feed into.** The **Flex Technical Taskforce** — established via a recommendation from the AI Energy Council (a body jointly run by DSIT and DESNZ) — launches late June 2026, is explicitly tasked with understanding "the degree to which data centres may be able to operate flexibly," and reports back to the AI Energy Council in autumn 2026, directly informing Connect Operate policy. It is, as of this document, still forming. That's a better-timed, better-fitting target for Stage 6's evidence than a fifth Curate milestone ever was.

**What this means for the Curate submission itself, and for what comes after it.** The Curate response should not ask Ofgem to add a workload/siting-fit milestone to the M0.5.Dc–M6.Dc framework — that framework was deliberately scoped to viability only, and arguing against that scoping fights the wrong battle. The sharper, more accurate ask is a **coordination point**: flag that Curate and Connect Operate are testing different things about the same projects, on different timelines, and that grid-value evidence (like the kind Stage 6 produces) risks falling through the gap between a live consultation closing 16 September and a taskforce whose findings won't land until autumn. Separately — and this is now the more promising lead — Stage 6's evidence is well-suited to feed the Flex Technical Taskforce directly, or the Connect Operate consultation expected in autumn 2026, once that opens.

**Scope boundary:** this finding identifies where Stage 6's evidence fits in Ofgem's actual programme structure. It does not yet include a plan for how to reach the Flex Technical Taskforce (no public engagement route has been identified — worth checking whether one exists) or a draft of the coordination point for the Curate response itself. Both are still open, and neither should be guessed at without checking.

**What's now settled, that wasn't:** the earlier caveat about not knowing *why* flexibility criteria were declined is resolved — they weren't declined, they were relocated, and the document explaining that (this Connect Update) has now been read in full.

## Traceability Table

| Finding | Number | Source | Reproducible via |
|---|---|---|---|
| DUoS differential | £43.67/MWh | SP Distribution Charging Statement, Annex 1, eff. 1 Apr 2026 | `duos_central_belt.py::get_duos_differential_gbp_mwh()` |
| DUoS vs Stage 5 ratio | 27.6× | Cross-reference to Stage 5's £1.58/MWh | `duos_central_belt.py::compare_to_stage5_training_site()` |
| Diurnal load timing | Peak 16:00-19:00 | Measured generative-AI inference power study | `inference_load_central_belt.py::PROFILE_EVIDENCE` |
| Battery coverage | Confirmed, no shortfalls | Min load 4.0MW vs 2.5MW battery | `inference_load_central_belt.py::check_battery_coverage()` |
| Realised annual DUoS value (gross) | £119,547/yr | Derived from differential + confirmed coverage | `inference_load_central_belt.py::realised_annual_duos_value()` |
| Battery energy sizing | 7.5MWh minimum usable | 2.5MW x 3h, before losses/SOC reserve | `inference_load_central_belt.py::required_energy_capacity_mwh()` |
| Realised annual DUoS value (net, Green charging) | £119,498/yr (99.96% of gross) | 85% RTE (Stage 3's figure), Green-period recharge cost | `inference_load_central_belt.py::net_annual_duos_value()` |
| Net value sensitivity (Amber charging) | £109,450/yr (91.6% of gross) | Same function, charge_rate=Amber | `inference_load_central_belt.py::net_annual_duos_value()` |
| TNUoS band assignment | HV4 | NESO Draft Forecast TNUoS Tariffs 2026/27 Webinar (thresholds) | `tnuos_central_belt.py::assign_band(5.0)` |
| TNUoS annual residual | £193,053/yr | NESO Final TNUoS Tariffs 2026/27, Table 10 | `tnuos_central_belt.py::annual_cost_gbp()` |
| Band-step saving feasibility | NOT feasible — £0 available | Site's 4.0MW min load exceeds even HV3's ~1.90MW ceiling | `tnuos_central_belt.py::feasible_band_step()` |
| Site anchor (fee analysis) | DataVita DV1, 40MW | Real, verified, at the fee threshold | `capex_central_belt.py::FEE_THRESHOLD_MW` |
| Capex benchmark (corrected) | £10.05M-£13.54M/MW | Ofgem consultation, Table 4 (DNO RFI), Medium band | `capex_central_belt.py::OFGEM_DNO_CAPEX_BY_SIZE` |
| Fee-to-capex ratio (corrected) | 1.75%-7.09% | Within Ofgem's own 2.5-7.5% target — original overshoot finding did not survive correction | `capex_central_belt.py::proportionality_check()` |

Every figure in this document traces to one of four scripts (`duos_central_belt.py`, `tnuos_central_belt.py`, `capex_central_belt.py`, `inference_load_central_belt.py`), each independently runnable and each printing its own Assumptions Ledger. No number here was retyped from memory of an earlier calculation.

---

## No Double-Counting

DUoS, TNUoS, and capex/commitment-fee are three separate, non-overlapping mechanisms, exactly as Stage 5 established for the training site:

- **DUoS** is continuous — realised per half-hour of load shifted, every year, indefinitely.
- **TNUoS** is a step-function — realised once, contingent on a formal capacity reduction, then held annually thereafter.
- **Commitment fee proportionality** is a one-off comparison at the point of connection — it does not recur annually and is not additive to the other two.

These should never be summed into a single blended "value" figure. They answer three different policy questions, for three different audiences: DUoS and TNUoS speak to a developer's ongoing economics; the commitment fee speaks to Ofgem's calibration of a one-off queue-management instrument.

---

## Assumptions Ledger (Consolidated)

| Item | Status | Detail |
|---|---|---|
| "Import-constrained" Central Belt claim | PROVISIONAL (sharpened) | Refers to local distribution demand-headroom pressure from clustered new connections, not Scotland's national import/export balance (Scotland is a net exporter — 21TWh, 2024). Local claim evidenced by documented demand clustering (11+ proposed hyperscale sites, 4.8GW+); current substation-specific headroom data not confirmed. |
| SP Distribution DUoS rates | GROUNDED | Sourced, current, dated 1 Apr 2026 |
| Residual charging band (DUoS) | PROVISIONAL | "No Residual" used as floor; real band unconfirmed |
| Site voltage tier assumption | PROVISIONAL | HV assumed; no specific site chosen for this parameter |
| NESO TNUoS HV rates | GROUNDED | Table 10, Final Tariffs 2026/27 |
| NESO TNUoS band thresholds | GROUNDED | RIIO-ET3, locked 2026/27-2030/31 |
| 5MW → HV4 band assignment | GROUNDED | Unambiguous, ~2.6x the threshold (corrected from an earlier "~10x" that compared against the wrong threshold — same error existed in this consolidated table, missed in an earlier fix pass) |
| Power factor (0.95) | PROVISIONAL | Reasonable assumption; band assignment robust to it given margin |
| TNUoS locational (Triad) component | OMITTED | Smaller addition on top of residual; not yet sourced |
| TNUoS saving capture route | PARTIALLY GROUNDED | Two of three links confirmed, one isn't. GROUNDED: TNUoS is billed to Suppliers not distribution-connected sites directly (NESO's own scope statement); SP Distribution's MIC reduction process is real and documented (§2.36-2.47). NOT CONFIRMED: whether a DNO-agreed MIC reduction is specifically the figure NESO uses to reassign a site's TNUoS demand residual band, versus some other reported or metered capacity figure. That specific link needs NESO/DNO/supplier charging documentation to confirm, not inferred from adjacent facts |
| TNUoS band-step savings for this site | GROUNDED (that it's NOT available) | No lower band is reachable — site's 4.0MW minimum load exceeds even HV3's ~1.90MW ceiling by over 2MW. An earlier version reported £125,375-£181,432/yr as available, computed from the tariff table without checking feasibility against the real load profile — a real error, caught in conversation, corrected here |
| Site anchor for fee/capex analysis | GROUNDED | Corrected from Asanti Livingston (5MW, out of scope) to DataVita DV1 (40MW, at threshold) |
| Capex benchmark (Medium 10-50MW band) | GROUNDED | Ofgem's own Table 4 (DNO RFI); corrected from international literature |
| Capex benchmark sample size | PROVISIONAL | n=8 for Medium band; both mean and median reported given small-sample uncertainty |
| DataVita DV1 TEA status | PROVISIONAL | Whether DV1 would trigger Transmission Entry Assessment (NESO process) vs pure DNO process is unconfirmed |
| MW basis: DataVita DV1 (40MW) | GROUNDED | Confirmed as IT load (NPM reporting); ≈47.2MW grid capacity at DV1's own 1.18 PUE; clears fee threshold either way |
| MW basis: Asanti Livingston (5.0MW) | PROVISIONAL | Not OMITTED — an explicit modelling choice was made (grid import capacity, since DUoS/TNUoS/MIC/battery mechanics all operate on that quantity), just not one the source data confirms. True figure could be 7.0-8.35MW if actually IT load, per the facility's own reported PUE range (1.4-1.67) — see Finding 1 for the scaled sensitivity |
| Ofgem's fee vs milestone threshold basis | PARTIALLY GROUNDED / INFERRED | Milestone threshold explicitly "rated IT load" (para 7.4) — that half is GROUNDED. Fee threshold's basis is never explicitly labelled; "grid connection capacity" is inferred from surrounding language ("requested connection," "contracted capacities") — that half is INFERRED, not confirmed. The two DO appear to use different bases, but only one side of that claim is a direct quote |

---

## Limitations & Future Work

This stage does not yet include: the TNUoS locational component; a specific DUoS residual charging band determination (requires site-specific consumption data Ofgem/SP Distribution would not have pre-connection); a check of the corrected fee-proportionality finding against the other size bands in Ofgem's own Table 4 (Small 0-10MW shows a highly volatile mean/median spread — £27M vs £9.5M/MW on n=7 — worth examining separately rather than assumed to follow the Medium band's pattern); a resolution of whether Asanti Livingston's "5.0MW" is IT load or grid capacity, which would change Finding 1's headline DUoS figure if resolved toward the higher (7.0-8.35MW) reading; or current, substation-specific SP Distribution headroom data for the Livingston/Bathgate or Chapelhall areas, which would let the "local distribution demand-headroom pressure" claim move from PROVISIONAL to GROUNDED. That data exists via SP Distribution's interactive heat maps and embedded capacity register, not as a document this stage could pull structured figures from. The battery sizing ratio (50% of site capacity, mirroring Stage 4/5) is a consistency choice, not independently justified for a pure peak-shaving use case — a smaller battery might suffice given the Red band is only 3 hours/day, and testing that is worthwhile future work.

The Flex Technical Taskforce engagement route (Finding 4) has not been identified — whether there's a public way to submit evidence to it, versus it being a closed stakeholder body, is unconfirmed. Neither has the actual coordination-point text for the Curate submission been drafted. Both are live next steps, not resolved.

---

*Full methodology, module code, and Assumptions Ledgers: `stage6/duos_central_belt.py`, `stage6/tnuos_central_belt.py`, `stage6/capex_central_belt.py`, `stage6/inference_load_central_belt.py`.*