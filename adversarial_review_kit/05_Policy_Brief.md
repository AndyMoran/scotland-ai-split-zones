# POLICY BRIEF: Auditing AI "Flexibility" in Scottish Planning Applications

**To:** Scottish Government (Net Zero & Energy Directorate), Local Planning Authorities, NESO  
**From:** [Your Name/Organization], Scotland AI Split-Zones Framework  
**Subject:** Preventing "Math-Washing" in Hyperscale Data Centre Grid Connection Claims  

## 1. The Problem: The "Flexibility" Illusion
As Scotland develops its AI Growth Zones, hyperscale data centre applicants increasingly claim their workloads are "50% flexible" to secure grid connections without triggering expensive transmission reinforcements. However, our physical modelling reveals a critical trap: **a static percentage claim is physically meaningless without defining the IT timescale.** 

Large AI training jobs cannot be paused instantly. They require hours to safely write "checkpoints" to disk. If a grid constraint event lasts 2 hours, but the AI system requires 12 hours of notice to pause, that "50% flexibility" is a fiction. The grid still bears the full, unmitigated burden.

## 2. The Evidence: Timescale Mismatch & Siting Bifurcation
Using an auditable, config-driven physical model, we tested a representative 500 MW AI campus under realistic grid conditions:

*   **The Timescale Trap:** We tested the worst-case combination within the plausible range: a 2-hour grid event (shorter than 68% of UK constraint events) paired with a 12-hour IT notice requirement (consistent with Microsoft Azure's 2023 production cluster documentation). The campus's schedulable workload (250 MW) collapses to just 42 MW—a loss of **208 MW of *potentially flexible* load** due to timescale mismatch. This represents an **83% reduction in the campus's flexible capacity**, or equivalently, a **42% reduction in the campus's total load contribution**. The remaining 250 MW of the 500 MW campus was never flexible to begin with (inflexible baseline). *(See Chart 1)*

*   **The Siting Bifurcation:** Placing this load in the Lowlands (import-constrained) creates massive new peak demand requiring transmission reinforcement. Placing the same load in the Highlands (export-constrained, e.g., near Whitelee) turns it into a grid asset, absorbing wasted renewable power without new wires. *(See Chart 2)*

### Siting Bifurcation: Physical Mechanism

| Factor | Export-Constrained Zone (e.g., Highlands) | Import-Constrained Zone (e.g., Lowlands) |
|--------|------------------------------------------|------------------------------------------|
| **Grid Constraint Type** | Cannot export enough renewable generation | Cannot import enough power to meet demand |
| **Curtailment Frequency** | High (wind generation exceeds transmission capacity) | Low (demand exceeds local generation) |
| **AI Load Effect** | Absorbs curtailed renewable power, reducing waste | Adds to peak demand, increasing import requirement |
| **Transmission Impact** | Uses existing underutilised capacity | Requires new reinforcement to handle additional import |
| **Net Grid Outcome** | Grid asset (reduces curtailment costs) | Grid burden (increases constraint costs) |

*Note: Quantitative curtailment volumes and transmission capacity figures for specific Scottish zones will be incorporated in Stage 2 using NESO constraint flow data.*

**Conclusion:** The same 500 MW AI workload has diametrically opposite grid impacts depending on location. In export-constrained zones with trapped renewables, AI becomes a grid asset. In import-constrained zones, it becomes a grid burden requiring expensive reinforcement.

## 3. Actionable Recommendations for Planning Authorities
To protect Scotland's Net Zero targets and prevent stranded grid assets, we recommend planning authorities adopt the following criteria for hyperscale AI developments:

1.  **Mandate IT Timescale Disclosure:** Do not accept flat "% flexibility" claims. Require applicants to explicitly state the *minimum notice period* (in hours) their specific IT orchestration requires to safely pause and resume workloads.
2.  **Condition Flexibility on Event Duration:** Link Section 75 (planning obligation) flexibility commitments to specific grid event durations. If an applicant claims 50% flexibility, their IT systems must physically demonstrate the ability to respond to sub-4-hour intraday balancing events.
3.  **Prioritise Export-Constrained Zones:** Actively steer AI compute development toward renewable-surplus, export-constrained areas (e.g., the Highlands and Islands), where flexible load can demonstrably absorb curtailed wind power, aligning with NPF4's Just Transition principles.

## 4. Conclusion
AI compute is not inherently a grid liability, but its flexibility is a function of time, not just arithmetic. By auditing the physical reality of IT checkpointing timescales, Scottish planners can ensure AI Growth Zones become genuine grid assets, not costly bottlenecks.

cat >> adversarial_review_kit/05_Policy_Brief.md << 'EOF'

## 5. Scope and Limitations
This analysis focuses on **workload flexibility as a standalone grid service**. We acknowledge that co-located battery storage could partially mitigate the timescale mismatch by bridging the gap between fast grid events and slow IT checkpointing. However, storage introduces its own economic constraints (capital cost, degradation, round-trip efficiency losses) and does not eliminate the fundamental physics of the timescale mismatch—it merely shifts the cost. Modelling the interaction between workload flexibility and co-located storage is planned for Stage 3 of this framework.

Similarly, this MVP uses a conservative 50% curtailment availability proxy based on UK-wide NESO data. Stage 2 will incorporate Scottish-specific constraint event data to refine the absorption estimates for Highland and Lowland zones.
EOF


*The underlying open-source model, "Scotland AI Split-Zones", is available for immediate audit and integration into local authority pre-application workflows at: https://github.com/AndyMoran/scotland-ai-split-zones*
