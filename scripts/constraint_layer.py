"""
constraint_layer.py

This module has one job: stop the Stage 3 constraint-value figure
(£0.79M/year, £15.8k/MW/year) from being ported into Stage 4 as a
free-standing revenue line without anyone having to say HOW the battery
actually captures it.

Stage 3 answered a physical/system-value question: is AI data-centre
flexibility meaningful for constraint relief in the Scottish grid?
That is not the same question as: does a co-located BATTERY earn this
money, and if so, through which market mechanism, and does that
mechanism already overlap with revenue counted elsewhere in the stack?

Three plausible mechanisms, three different overlap answers:

  1. BM_CONSTRAINT_ACTION
     The battery itself bids into the Balancing Mechanism specifically
     to relieve constraint (charging/discharging in response to a
     constraint-driven Bid/Offer). This is REAL, but it runs through
     the same BM channel that's already inside the benchmark.py
     baseline (Balancing Mechanism revenue is part of that £41-73k/MW
     blended figure). Counting it again here is double-counting.

  2. BILATERAL_CONTRACT
     The battery (or its owner) has a direct commercial arrangement
     with the AI data centre operator — e.g. a flexibility/curtailment
     avoidance contract, paid outside of BM/wholesale mechanisms
     entirely. This COULD be genuinely additive, because it's a
     separate cash flow from a separate counterparty, not routed
     through a market the baseline already captures.

  3. SYSTEM_VALUE_PASSTHROUGH
     The Stage 3 figure was never a battery revenue number at all —
     it's a system/DNO/data-centre-side saving that doesn't touch the
     battery's P&L unless a contract in mechanism 2 exists. If this is
     the honest answer, the increment for Stage 4 is £0, and that's a
     legitimate finding, not a gap to explain away.

The default is UNCERTAIN and the module raises rather than guessing.
That's deliberate — this is the same discipline as catching the
overclaimed burden figure and circular logic in the Stage 3 document
bundle review. A wrong default here would resurrect exactly that kind
of error, just one stage further downstream.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Mechanism(Enum):
    BM_CONSTRAINT_ACTION = "bm_constraint_action"
    BILATERAL_CONTRACT = "bilateral_contract"
    SYSTEM_VALUE_PASSTHROUGH = "system_value_passthrough"
    UNCERTAIN = "uncertain"


MECHANISM_DESCRIPTIONS = {
    Mechanism.BM_CONSTRAINT_ACTION: (
        "Battery bids into the Balancing Mechanism specifically for "
        "constraint relief actions."
    ),
    Mechanism.BILATERAL_CONTRACT: (
        "Direct commercial contract between battery owner and AI data "
        "centre operator, paid outside BM/wholesale."
    ),
    Mechanism.SYSTEM_VALUE_PASSTHROUGH: (
        "Stage 3 figure is a system-level saving, not a battery cash flow, "
        "unless a bilateral contract (see above) is separately in place."
    ),
    Mechanism.UNCERTAIN: "Not yet established.",
}


@dataclass
class ConstraintIncrementResult:
    mechanism: Mechanism
    incremental_value_gbp_per_mw: float
    overlaps_baseline: bool
    reasoning: str


# ---------------------------------------------------------------------------
# THIS IS THE ONE LINE IN THE WHOLE PIPELINE THAT MUST BE SET DELIBERATELY.
# Do not change the default. Change this only once you've established,
# with evidence, which mechanism actually applies.
# ---------------------------------------------------------------------------
MECHANISM: Mechanism = Mechanism.UNCERTAIN


def evaluate_increment(
    stage3_value_gbp_per_mw: float = 15_800,
    mechanism: Optional[Mechanism] = None,
) -> ConstraintIncrementResult:
    """
    Evaluates whether the Stage 3 constraint value is a legitimate
    incremental revenue line for Stage 4, and whether it overlaps with
    the benchmark.py baseline.

    Raises ValueError if mechanism is UNCERTAIN (the default) — this
    function will not let the model run with an unexamined assumption.
    """
    m = mechanism if mechanism is not None else MECHANISM

    if m == Mechanism.UNCERTAIN:
        raise ValueError(
            "MECHANISM is UNCERTAIN. Stage 3 was a system-value calculation, "
            "not a battery-revenue mechanism. Before running the stack, "
            "establish (with evidence — a contract structure, a BM dispatch "
            "pattern, or a DNO/NESO settlement mechanism) which of the three "
            "Mechanism options actually applies, and pass it explicitly. "
            "Do not set a default here just to make the script run."
        )

    if m == Mechanism.BM_CONSTRAINT_ACTION:
        return ConstraintIncrementResult(
            mechanism=m,
            incremental_value_gbp_per_mw=0.0,
            overlaps_baseline=True,
            reasoning=(
                "Constraint-relief BM bids are already inside the blended "
                "Balancing Mechanism revenue captured in benchmark.py's "
                "baseline (BM was ~part of the £41-73k/MW/year blended "
                "figure, and was in fact the ONLY service to grow in Feb "
                "2026). Adding the Stage 3 figure on top here would "
                "double-count. Incremental value set to £0 — the value is "
                "already counted."
            ),
        )

    if m == Mechanism.BILATERAL_CONTRACT:
        return ConstraintIncrementResult(
            mechanism=m,
            incremental_value_gbp_per_mw=stage3_value_gbp_per_mw,
            overlaps_baseline=False,
            reasoning=(
                "A direct bilateral flexibility contract with the AI data "
                "centre operator is a separate cash flow from a separate "
                "counterparty, not routed through BM/wholesale/FR/CM. "
                "Treat as genuinely additive — BUT this still requires "
                "evidence such a contract structure exists or is realistic "
                "(pricing precedent, counterparty willingness), not just "
                "that it's theoretically possible."
            ),
        )

    if m == Mechanism.SYSTEM_VALUE_PASSTHROUGH:
        return ConstraintIncrementResult(
            mechanism=m,
            incremental_value_gbp_per_mw=0.0,
            overlaps_baseline=False,
            reasoning=(
                "Stage 3's £0.79M/year is a system/grid-level saving, not a "
                "cash flow that reaches the battery's P&L. Correct "
                "incremental revenue for THIS battery is £0. This is a "
                "legitimate finding — it means the AI constraint story is "
                "still true and useful, but it's a policy/system argument, "
                "not a line item on this battery's investment case. Don't "
                "force it into the stack to make the payback number better."
            ),
        )

    raise ValueError(f"Unhandled mechanism: {m}")


if __name__ == "__main__":
    # Deliberately demonstrates the guard rail — this will raise, on purpose,
    # until MECHANISM is set. Run each branch explicitly to see the three
    # possible outcomes.
    print("Testing all three mechanisms explicitly (bypassing the default):\n")

    for mech in [
        Mechanism.BM_CONSTRAINT_ACTION,
        Mechanism.BILATERAL_CONTRACT,
        Mechanism.SYSTEM_VALUE_PASSTHROUGH,
    ]:
        result = evaluate_increment(mechanism=mech)
        print(f"--- {mech.value} ---")
        print(f"  Incremental value: £{result.incremental_value_gbp_per_mw:,.0f}/MW/year")
        print(f"  Overlaps baseline: {result.overlaps_baseline}")
        print(f"  Reasoning: {result.reasoning}\n")

    print("Now testing the default (should raise):")
    try:
        evaluate_increment()
    except ValueError as e:
        print(f"  Raised as expected: {e}")
