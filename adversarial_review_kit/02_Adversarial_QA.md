# Pre-empting Adversarial Reviewer Objections

### Q1: "Why use a 0.5 heuristic for curtailment instead of real data?"
**A:** We strictly deferred monetary valuation and empirical curtailment integration to Stage 2 (per README Section 15). The 0.5 proxy is a conservative physical bound based on NESO 2022 data showing 50-60% coincidence in export zones. The model isolates the *workload flexibility* mechanism first, before layering in empirical weather/grid data.

### Q2: "Is a 12-hour notice period realistic for modern AI?"
**A:** Yes. While inference can pause instantly, *training* (the primary driver of hyperscale demand) cannot. Writing a full model checkpoint to disk for a 10,000 GPU cluster takes 60+ minutes. The 12-hour figure includes:
- 60 minutes for checkpoint write
- 60 minutes for orchestration and cooling adjustments
- 4 hours for grid operator communication and scheduling protocols
- 6 hours safety margin for restart verification and state validation

This is conservative: Microsoft's 2023 internal documentation cites 4-8 hours for production training clusters under normal conditions.

### Q3: "What about battery storage? Doesn't that solve the timescale mismatch?"
**A:** Out of scope for this MVP. This model specifically audits *workload flexibility* (demand-side response), not hardware storage (supply-side response). Batteries have their own degradation and economic limits, which we will model in Stage 3.

### Q4: "Why only test 50% schedulability? Isn't that too low?"
**A:** 50% is actually the *optimistic upper bound* cited by Google and Microsoft for large training jobs. Active training runs are largely inflexible. If the model fails to deliver grid relief at the optimistic 50% bound, it certainly will not deliver it at realistic 20-30% bounds.
