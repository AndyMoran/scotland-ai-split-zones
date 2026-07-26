# Core Thesis: The Timescale Mismatch Trap

## The Testable Hypothesis
**Claim:** A static "50% flexibility" claim for AI workloads is physically meaningless for intraday grid events if the IT checkpointing timescale exceeds the event duration. This creates a "timescale mismatch" that reduces delivered flexibility by 83% (from 270 MW to 45 MW) under realistic conditions.

**Falsification Test:** To disprove this, a reviewer must demonstrate a scenario where a 500 MW AI campus with a 12-hour IT notice requirement successfully delivers 270 MW of flexibility during a 2-hour grid constraint event.

## The Evidence Chain
Every assumption in the model is traceable and auditable.

| Component | Model Assumption | Evidence Source | Reviewer Falsification Test |
| :--- | :--- | :--- | :--- |
| **IT Checkpointing Time** | 12 hours notice required | Microsoft Azure (2023): 60+ mins for 10k GPU cluster checkpointing + safety margins. | *Find a major hyperscaler with <4h checkpointing for large models.* |
| **Curtailment Proxy** | 50% availability factor | NESO (2022): ~50% of constraint events coincide with high wind generation. | *Show NESO data where curtailment availability is <30% in Scottish export zones.* |
| **Grid Event Durations** | 2 to 4 hours | National Grid ESO (2023): 68% of constraint events last <4 hours. | *Find evidence that >50% of events last >6 hours in Scotland.* |
| **Workload Flexibility** | 50% schedulable fraction | Google (2022): 50% is the upper bound for large training jobs at start/stop. | *Prove 50% schedulability is easily achievable mid-run for active clusters.* |

## Clarification on "Unmitigated Burden"
The model distinguishes between:
- **Inflexible baseline load**: 50% of the 500 MW campus (250 MW) that is never schedulable, regardless of timescale
- **Failed flexibility claim**: The portion of the schedulable load (250 MW) that cannot be delivered due to timescale mismatch (205 MW loss in the worst-case scenario)

The "unmitigated burden" refers specifically to the *failed flexibility claim*, not the entire load. The inflexible baseline is a separate issue that planning authorities should address through different mechanisms (e.g., demand-side management, efficiency standards).

**Limitation:** Event duration statistics are UK-wide (National Grid ESO 2023). 
Scottish constraint events in wind-rich export zones may have different duration 
profiles. Stage 2 will incorporate NESO's Scottish-specific Day-Ahead Constraint 
Flow data to refine this assumption.