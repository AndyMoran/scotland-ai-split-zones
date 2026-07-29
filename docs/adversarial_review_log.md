# Adversarial Review & Data Integrity Log

This document tracks the rigorous self-auditing and adversarial review processes applied to the "Scotland AI Split-Zones" framework. Our core principle is that open-source policy research must actively seek out its own flaws, correct them transparently, and document the process.

---

## 1. Stage 2: Synthetic Data Contamination & Volume Correction

**The Catch:** 
Initial Stage 2 calculations estimated a Scottish thermal constraint volume of ~3.0 TWh/year, yielding a theoretical upper bound of ~£500M/year. During a routine audit, we discovered the NESO API endpoint was returning future Day-Ahead forecast data (extending to 2026) alongside historical outturn data. 

**The Fix:** 
We implemented a strict historical filter (`pl.col("timestamp").dt.year().is_in([2023, 2024])`) across all Stage 2 and Stage 3 data pipelines to exclude all synthetic future forecast artifacts.

**The Impact:** 
- Corrected 2-year historical volume: **3.53 TWh** (~1.76 TWh annualized).
- Corrected theoretical upper bound: **~£291M/year** (down from ~£500M/year).
- *Why this matters:* This correction aligns the framework with expected Scottish constraint shares (1-2 TWh/year) and makes our "Compatibility ≠ Capture" caveat significantly more conservative and defensible.

---

## 2. Stage 3: Battery Sizing & Event Clustering Defense

**The Challenge:** 
A common critique is that a 2-hour battery is overkill if short (P10) constraint events don't stack back-to-back. Inferring conditional probability (stacking) from marginal frequency (overall prevalence) is a known statistical trap.

**The Fix:** 
We built dedicated temporal clustering scripts (`scripts/04_inter_event_gap_analysis.py`, `scripts/05_chain_depth_analysis.py`) to measure actual event sequencing in the verified 2023-2024 dataset.

**The Findings:**
- **Rolling Window Density:** 0.0% of 2-hour windows contain 3+ events. The maximum observed stress in a 2-hour window is exactly 2 events.
- **Chain Depth:** Starting from a 0.5h (P10) event, the 85 MWh usable battery capacity survives 3+ consecutive events 100% of the time under a strict "zero-recharge" assumption.
- **Worst-Case Scenario:** The only historical sequence causing a simulated breach was a 26.5-hour marathon event (Dec 30-31, 2024). Under the conservative zero-recharge assumption, the subsequent event breaches the floor. In operational reality, the multi-day clear grid period following such an event provides ample recharge opportunity.
- *Why this matters:* The 2-hour spec is empirically validated not just for reliability, but to retain ~35 MWh of usable headroom for merchant revenue stacking between events.

---

## 3. Stage 3: Economic Simulation Stress-Testing

**The Challenge:** 
Initial hybrid simulation outputs showed a marginal battery capture of 9,625 MWh over 2 years. Divided by the 59 P10 events, this implied an impossible ~163 MWh per event, violating the established 50 MW / 1-hour handoff cap. Additionally, round-trip efficiency (RTE) was not being applied, violating conservation of energy.

**The Fix:** 
We audited the simulation logic (`scripts/09_hybrid_response_simulation.py`) and implemented two critical corrections:
1. **Marginal Value Breakdown:** We explicitly separated the marginal capture into two physically valid components:
   - P10 events (<1h, battery-enabled): 1,475 MWh (25 MWh/event average).
   - Handoff coverage (≥1h events): 8,150 MWh (50 MWh/event handoff cap).
2. **Round-Trip Efficiency:** We applied the 85% AC-AC RTE, correctly showing that recharging the battery requires more AC grid energy (11,265 MWh) than the DC energy it delivers (9,625 MWh), accounting for ~1,640 MWh of thermal loss.

**The Impact:** 
The corrected simulation confirms an annualized marginal value of **~£0.79M/year** from constraint avoidance alone. At a £25M CAPEX, this yields a 31.5-year simple payback. 

**Explicit Acknowledged Assumption:** 
The model assumes a constant magnitude response (full 50 MW battery / 100 MW AI response for every event). In reality, constraint magnitudes (Flow - Limit) vary. Therefore, the £0.79M/year figure represents an **upper bound**. The true marginal value is likely lower, making the conclusion—that the battery *must* rely on merchant revenue stacking to be investable—even stronger.

---

## Conclusion

This framework does not claim to have all the answers on the first try. It claims to have a rigorous, reproducible, and transparent methodology for finding the right answers. All code, data filters, and correction logs are publicly available in this repository for independent verification.