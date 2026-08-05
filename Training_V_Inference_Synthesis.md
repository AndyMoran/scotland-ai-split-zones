# Training vs Inference: A Synthesis of the Two Grid Archetypes

**Companion to `PROJECT.md`.** Stages 1–5 built and validated a 100MW AI training site in export-constrained Northern Scotland. Stage 6 built a 5MW inference site facing local distribution demand-headroom pressure in the Central Belt. This document puts the two side by side and asks what the comparison actually shows — not just what each stage found on its own.

---

## Ground Truth Status — Read This Before Citing Anything Below

This document draws on two bodies of work with genuinely different verification status, and blending them without saying so would misrepresent both.

**Stage 6 figures are fresh-verified in this session.** Every number below traces to one of four executable modules (`duos_central_belt.py`, `tnuos_central_belt.py`, `capex_central_belt.py`, `inference_load_central_belt.py`), re-run end to end via the Stage 6 notebook, with assertions on every headline figure. Several real errors were caught and corrected in the process of producing them — the kVA arithmetic, the site-anchor mismatches, the TNUoS band-step feasibility. What's presented here reflects the corrected state, not the original.

**Stage 5 figures were cross-checked against the actual Stage 5 notebook export** (`09_stage5_behind_the_meter_synthesis.md`) after this document's first draft, and the check found a real error, not just confirmation. The headline numbers — £1.58/MWh DUoS differential, £1.8M/yr TNUoS ASC Band Step, £600/yr locational residual, £25M capex, the 96% share, the payback figures — all confirmed exactly against source. But the wholesale peak-shaving mechanism description in the first draft was wrong: it claimed the mechanism was "capped by load/price overlap," which Stage 5's own conclusion explicitly rejects (the actual constraints are battery duration, price volatility, and peak-day count — see the mechanism section below). That wrong framing had also propagated into the top-level `README.md`; both are now fixed. One nuance worth carrying forward rather than smoothing over: **Stage 5's own internal ledger marks the £1.8M TNUoS ASC Band Step — the mechanism supplying 96% of the whole finding — as PROVISIONAL, not GROUNDED.** This document cites that figure with the same status Stage 5 itself assigned it, not with more confidence than the source claims for itself.

**Stage 4's net cash-flow figures were subsequently checked against the actual Stage 4 notebook export** (`08_stage4_merchant_stacking_synthesis.md`) — a clean pass, no errors found this time, worth reporting as plainly as the Stage 5 error was. The figures Stage 5 inherited (£1,338,500 and £2,897,532 net cash flow) reproduce Stage 4's stated 18.7yr/8.6yr paybacks exactly, and reverse-engineering them through Stage 4's stated OPEX/degradation/availability assumptions lands almost exactly on Modo Energy's stated £41k–73k/MW/yr benchmark range. The bilateral-contract scenario and Stage 3's £0.79M/yr ceiling also cross-check consistently. **What this confirms is internal consistency — that Stage 4's own numbers follow from Stage 4's own stated inputs — not external verification of Modo Energy's published rates themselves**, since Modo's own data isn't in either uploaded file. That's a narrower, more specific remaining gap than "Stage 4 unverified" would suggest.

Every table below is marked per-row with which status applies.

---

## The Two Archetypes at a Glance

| | Stage 5: Training | Stage 6: Inference | Status |
|---|---|---|---|
| Site scale | 100MW | 5MW | Both GROUNDED |
| Connection voltage | 132kV / EHV | HV | Both GROUNDED |
| Region | Northern Scotland | Central Belt | Both GROUNDED |
| Constraint mechanism | Export-constrained (renewable curtailment) | Local distribution demand-headroom pressure (not a national import claim — see Stage 6's own correction on this) | Both GROUNDED |
| Battery | 50MW / 100MWh | 2.5MW / 7.5MWh minimum usable | Both GROUNDED |
| Workload flexibility | Schedulable (can pause/resume) | Continuous, cannot be paused | Both GROUNDED |
| DUoS Red\u2013Green differential | £1.58/MWh | £43.67/MWh (27.6\u00d7 larger) | Stage 5: GROUNDED, cross-checked against source. Stage 6: GROUNDED, this session |
| TNUoS mechanism | ASC Band Step: £1.8M/yr (**PROVISIONAL** in Stage 5's own ledger), ~96% of total BTM value | Band-step checked directly against real load profile: **not feasible at any point** \u2014 confirmed via `feasible_band_step()` | Stage 5: cross-checked, status is Stage 5's own PROVISIONAL, not upgraded here. Stage 6: GROUNDED, this session |
| Dominant realised value driver | TNUoS (96%, on a PROVISIONAL figure) | DUoS (100% \u2014 the only mechanism that pays out at all) | Stage 5: cross-checked. Stage 6: GROUNDED, this session |
| Commitment fee proportionality | Not applicable \u2014 Curate didn't exist when Stage 5 was done | 1.75\u20137.09%, spans Ofgem's own 2.5\u20137.5% target (DataVita DV1 anchor) | Stage 6 only. GROUNDED, this session |
| Combined payback | Stage 4 baseline (no BTM): 18.7yr conservative / 8.6yr rolling. + Continuous BTM only: 17.7yr / 8.4yr. + Full BTM incl. ASC step: 7.8yr / 5.2yr | Not computed \u2014 see Economics section below | Stage 5: GROUNDED, cross-checked against source. Stage 4 baseline inputs: internally consistent, checked against Stage 4's own source \u2014 not independently verified against Modo Energy's underlying published rates. Stage 6: genuine gap, not a number to force |

---

## The Core Synthesis Finding: The Two Mechanisms Swap Which One Matters

This is the single sharpest result in the whole comparison, and it's worth stating precisely because the arithmetic is clean enough to check directly: **for the training site, TNUoS supplies 96% of realised behind-the-meter value and DUoS is close to a rounding error. For the inference site, it's the exact mirror — DUoS supplies 100% of realised value, because the TNUoS mechanism isn't available at all.** One caveat worth keeping attached to this finding wherever it's quoted: the £1.8M TNUoS figure driving Stage 5's 96% is marked PROVISIONAL in Stage 5's own methodology, not GROUNDED — the *mirror-image pattern* is robust either way (Stage 6's 0%/100% split is independently confirmed this session), but the specific *96%* figure inherits Stage 5's own stated uncertainty.

This isn't two unrelated facts about two different sites. It's one underlying pattern — connection voltage tier — driving both results in opposite directions simultaneously:

- **DUoS scales down with voltage, not with site size.** A hyperscale site connects close to the transmission network and barely touches local distribution infrastructure, so it pays almost nothing for it. A smaller, HV-connected site sits much closer to the distribution network it actually uses, and pays the fuller rate. This is why Stage 6's differential is 27.6\u00d7 larger despite the site being 20\u00d7 smaller.
- **TNUoS band-step availability depends on how much headroom exists between a site's minimum load and the next band down — not on site size directly, but on load *shape*.** The training site's schedulable workload gives it genuine idle periods, creating room to step down a capacity band. The inference site's continuous, unpausable demand means its minimum load barely differs from its peak — confirmed this session at 4.0MW trough against a 5.0MW peak — leaving no band-step reachable at all.

Put plainly: **bigger, transmission-connected sites should expect network-charge value from TNUoS management, not DUoS arbitrage. Smaller, distribution-connected sites should expect the opposite.** That's a generalisable siting principle, not a fact about these two specific sites — though it's only been checked rigorously for these two.

---

## Mechanism-by-Mechanism: What Transfers, What Doesn't, and Why

Four distinct mechanisms have come up across both stages. They don't all transfer between workload types for the same reason, and conflating them would be a real analytical error:

1. **AI constraint avoidance (Stage 3\u20134, training only).** Requires the *workload itself* to pause and resume around grid conditions. This is genuinely training-specific — Stage 6 confirmed inference cannot use this mechanism, because inference load cannot be paused by definition.
2. **DUoS peak-shaving (both stages, opposite magnitude).** Requires a *battery* to shift the site's import profile, not the workload. Transfers to inference cleanly — arguably more reliably, since continuous demand means the battery always has somewhere to discharge into.
3. **TNUoS ASC Band Step (both stages, opposite availability).** Also battery/capacity-driven rather than workload-driven in principle — but requires enough gap between minimum and peak load to actually step down a band. Training's schedulability creates that gap; inference's continuity closes it.
4. **Wholesale peak-shaving (Stage 5 only, not yet built for Stage 6).** Not capped by load/price overlap — that's a real finding from Stage 5 (training spikes and price peaks show 0% overlap) but an irrelevant one, per Stage 5's own conclusion: the training site's 70MW baseline load always exceeds the 50MW battery's capacity, so the battery can discharge into background demand during any price peak without needing a training spike to be running. The actual constraints are battery duration, price volatility magnitude, and the number of shaveable peak days per year. Not yet modelled for the inference site — a genuine gap in this comparison, not a finding either way.

The generalisable point: **"does this mechanism require the workload to be flexible, or just the site's import profile to be shapeable by a battery"** is the actual dividing line — not "training vs inference" as a blunt category. Mechanism 1 needs the former; mechanisms 2 and 3 need only the latter, which is why they transfer (or don't) for reasons that have nothing to do with workload flexibility itself, only with load *shape*.

---

## What Doesn't Have a Direct Comparison

Being honest about asymmetry matters as much as the comparison itself:

- **Commitment fee proportionality (Stage 6 only).** Ofgem's Curate consultation postdates Stage 5 entirely — there's no Stage 5 equivalent to compare against, not because Stage 5 found something different, but because the question didn't exist yet.
- **The Curate/Connect Operate regulatory-architecture finding (Stage 6 only).** Same reason — this emerged from Stage 6's direct engagement with a live 2026 consultation.
- **Wholesale peak-shaving for the inference site.** Modelled for Stage 5, not yet built for Stage 6. Absence of a finding here, not a negative finding.

---

## Economics: Why There's No Combined Payback Figure for Stage 6

Stage 5 has one: 8.6\u201318.7 years depending on whether the ASC Band Step materialises. Stage 6 doesn't have an equivalent, and manufacturing one would be worse than leaving the gap visible.

The reason is structural, not an oversight: Stage 6's capex work (`capex_central_belt.py`) was built specifically to test commitment-fee proportionality against DataVita DV1, a 40MW site — a different anchor from the 5MW/2.5MW-battery site the DUoS and TNUoS findings use. There is no capex figure in this project, for the 5MW site specifically, to divide the annual DUoS value into. Computing a payback would mean pairing a real revenue figure (£119,547/yr, gross) with a capex figure borrowed from a different, larger site — exactly the kind of category error this project's own discipline exists to catch. **This is flagged as a genuine gap for future work, not filled in with an estimate.**

---

## What This Feeds Into

This document is the shared foundation for two different outputs, not a draft of either:

- **A LinkedIn post** would likely lead with the "mechanisms swap which one matters" finding — it's the most quotable, most visually chartable result, and doesn't require regulatory context to land.
- **The Ofgem consultation response** would draw on the mechanism-by-mechanism breakdown and the "voltage tier, not workload type" reframing — this is a sharper, more general version of Stage 1's original constraint-direction thesis, now backed by two independently-modelled sites rather than asserted conceptually.

Neither is drafted here. Both should wait until the Stage 5 figures in this document have had the spot-check flagged above.

---

*Full detail: `PROJECT.md` and `docs/adversarial_review_log.md` for Stage 5; `stage6/STAGE6_SYNTHESIS.md` and `stage6/README.md` for Stage 6.*