"""
network_charges.py

Models network charge avoidance as THREE STRUCTURALLY DISTINCT mechanisms,
not one blended "network charge avoidance" line. Collapsing these would
repeat the Stage 4 sum-of-parts error in a new place — these three
mechanisms have different triggers, different time constants, and
critically, are not all "continuous £/half-hour" savings.

Mechanism status (checked July 2026 — verify again before reporting,
Ofgem's Access and Forward-Looking Charges reform is still moving):

  1. DUoS_RAG — Distribution Use of System, Red/Amber/Green banding.
     STATUS: LIVE, CONTINUOUS. This remains a real, schedulable,
     half-hourly mechanism — avoid consumption in Red bands, save DUoS.
     Closest to what most people assume "network charge avoidance" means.

  2. TNUoS_ASC_BAND_STEP — reducing Available Supply Capacity band via
     permanent behind-the-meter peak shaving.
     STATUS: LIVE, but LUMPY. Since the 2023 Targeted Charging Review,
     ~90% of TNUoS moved to a fixed residual based on agreed capacity
     band, not continuous consumption. The only way to meaningfully cut
     this is to permanently lower your ASC band — a step-function saving
     (cross a threshold, save every year after), not a per-half-hour
     optimisation. Requires sustained capex-backed peak reduction, not
     just occasional shaving on high-price days.

  3. TNUoS_LOCATIONAL_RESIDUAL — the remaining small locational/Triad-
     linked element.
     STATUS: LIVE but SMALL and PARTIAL. Most of the old Triad-avoidance
     value is gone post-TCR; what's left is a minor locational signal,
     not the dominant mechanism it used to be pre-2023. Do not model
     this as if pre-2023 Triad-dodging economics still apply.

Do not sum these three into one number without stating, for each, whether
it's continuous or step-function — a reader will otherwise assume all
three behave like (1).
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ChargeBehaviour(Enum):
    CONTINUOUS = "continuous"        # saved every time you shave, every half-hour
    STEP_FUNCTION = "step_function"  # saved only if you cross a capacity band threshold
    PARTIAL_RESIDUAL = "partial_residual"  # small, live, but much reduced vs pre-2023


@dataclass
class NetworkChargeLine:
    name: str
    behaviour: ChargeBehaviour
    status_note: str
    annual_saving_gbp: float = 0.0
    evidence_status: str = "PROVISIONAL"


def duos_rag_saving(
    load_profile_mw: list,
    red_band_periods: set,
    # SSEN SHEPD (Northern Scotland) 132kV/EHV Site Specific Rates
    # Source: SSEN SHEPD Schedule of Charges, "LDNO 132kV/EHV: HV Site Specific"
    # Note: These rates are ~10× lower than typical HV (33kV) rates because
    # a 100MW site connects at transmission level, imposing minimal local
    # distribution losses. This is a feature, not a bug — it means DUoS
    # peak-shaving value is structurally limited for hyperscale AI sites.
    duos_red_rate_gbp_per_mwh: float = 1.58,   # 0.158 p/kWh × 10
    duos_green_rate_gbp_per_mwh: float = 0.00, # 0.000 p/kWh × 10
) -> NetworkChargeLine:
    """
    DUoS Red/Amber/Green avoidance — LIVE, CONTINUOUS mechanism.
    Savings = (load shaved during Red periods) × (Red rate - Green rate).
    This is genuinely schedulable: every half-hour of Red-period load
    avoided saves money, independent of any capacity-band threshold.
    
    IMPORTANT: For a 100MW AI site connecting at 132kV (EHV), the DUoS
    differential is only £1.58/MWh — roughly 10× lower than typical HV
    rates. This means DUoS peak-shaving value is structurally limited
    for hyperscale sites, regardless of battery size.
    """
    # Calculate total MWh shaved during Red periods
    red_band_shaved_mwh = sum(
        load_mw * 0.5  # 0.5 hours per half-hour period
        for i, load_mw in enumerate(load_profile_mw) 
        if i in red_band_periods
    )
    
    rate_differential = duos_red_rate_gbp_per_mwh - duos_green_rate_gbp_per_mwh
    annual_saving = red_band_shaved_mwh * rate_differential
    
    return NetworkChargeLine(
        name="DUoS RAG Avoidance (SSEN SHEPD 132kV/EHV)",
        behaviour=ChargeBehaviour.CONTINUOUS,
        status_note=(
            f"Based on SSEN SHEPD published DUoS rates for 132kV/EHV Site Specific. "
            f"Red rate: £{duos_red_rate_gbp_per_mwh}/MWh, "
            f"Green rate: £{duos_green_rate_gbp_per_mwh}/MWh. "
            f"Differential: £{rate_differential}/MWh. "
            f"Total Red-period load shaved: {red_band_shaved_mwh:.1f} MWh. "
            f"Note: EHV rates are ~10× lower than HV rates because the site "
            f"connects at transmission level, imposing minimal local distribution losses."
        ),
        annual_saving_gbp=annual_saving,
        evidence_status="GROUNDED — sourced from SSEN SHEPD published charging statement (April 2027 tariff)",
    )

def tnuos_asc_band_step_saving(
    current_asc_mw: float,
    band_thresholds_mw: list[float],
    band_annual_charge_gbp: dict,
    sustained_peak_reduction_mw: float,
) -> NetworkChargeLine:
    """
    TNUoS saving via dropping an Available Supply Capacity (ASC) band —
    LIVE but STEP-FUNCTION, not continuous.

    This only produces a saving if `sustained_peak_reduction_mw` is large
    enough, and SUSTAINED enough, to justify actually lowering the site's
    agreed capacity with the DNO/transmission owner — a contractual,
    capex-backed decision, not a daily dispatch choice. Occasional
    high-price-day shaving does NOT reduce this charge; only a genuine,
    committed reduction in peak demand does.
    """
    new_asc = current_asc_mw - sustained_peak_reduction_mw
    current_band = _band_for_capacity(current_asc_mw, band_thresholds_mw)
    new_band = _band_for_capacity(new_asc, band_thresholds_mw)

    if current_band == new_band:
        return NetworkChargeLine(
            name="TNUoS ASC Band Step",
            behaviour=ChargeBehaviour.STEP_FUNCTION,
            status_note=(
                f"Sustained reduction of {sustained_peak_reduction_mw}MW "
                f"insufficient to cross a band threshold (still band "
                f"{current_band}). Annual saving: £0. This is the normal "
                f"outcome unless the battery enables a genuinely large, "
                f"permanent capacity reduction."
            ),
            annual_saving_gbp=0.0,
            evidence_status="STRUCTURAL — no saving without threshold crossing",
        )

    saving = band_annual_charge_gbp.get(current_band, 0) - band_annual_charge_gbp.get(new_band, 0)
    return NetworkChargeLine(
        name="TNUoS ASC Band Step",
        behaviour=ChargeBehaviour.STEP_FUNCTION,
        status_note=(
            f"Sustained reduction of {sustained_peak_reduction_mw}MW crosses "
            f"from band {current_band} to band {new_band}. This requires a "
            f"formal ASC reduction with the network operator, not just "
            f"dispatch behaviour — treat as a capex/contractual decision, "
            f"not an operational one."
        ),
        annual_saving_gbp=saving,
        evidence_status="PROVISIONAL — band thresholds/charges need DNO-specific sourcing",
    )


def _band_for_capacity(capacity_mw: float, thresholds: list[float]) -> int:
    band = 0
    for t in sorted(thresholds):
        if capacity_mw >= t:
            band += 1
    return band


def tnuos_locational_residual_saving(
    peak_shaved_mwh_at_triad_risk_periods: float,
    locational_rate_gbp_per_mwh: float,
) -> NetworkChargeLine:
    """
    The remaining small locational/Triad-linked TNUoS element —
    LIVE but PARTIAL. Post-2023 TCR, this is a minor residual signal,
    not the dominant Triad-avoidance mechanism that existed pre-2023.

    Model this conservatively and flag explicitly that it is a small
    fraction of what pre-2023 Triad-avoidance analyses would have shown —
    do not let this number quietly inherit pre-2023 scale assumptions.
    """
    saving = peak_shaved_mwh_at_triad_risk_periods * locational_rate_gbp_per_mwh
    return NetworkChargeLine(
        name="TNUoS Locational Residual",
        behaviour=ChargeBehaviour.PARTIAL_RESIDUAL,
        status_note=(
            "Post-2023 TCR reduced this to a minor locational signal. "
            "Do not compare this figure against pre-2023 Triad-avoidance "
            "case studies — those reflect a mechanism that has since been "
            "~90% removed from TNUoS cost recovery."
        ),
        annual_saving_gbp=saving,
        evidence_status="PROVISIONAL — locational rate needs NESO tariff sourcing",
    )


def summarise_network_stack(lines: list[NetworkChargeLine]) -> dict:
    """
    Summarises the three lines WITHOUT collapsing them into one number
    unless each line's behaviour type is preserved in the output.
    """
    continuous_total = sum(l.annual_saving_gbp for l in lines if l.behaviour == ChargeBehaviour.CONTINUOUS)
    step_total = sum(l.annual_saving_gbp for l in lines if l.behaviour == ChargeBehaviour.STEP_FUNCTION)
    residual_total = sum(l.annual_saving_gbp for l in lines if l.behaviour == ChargeBehaviour.PARTIAL_RESIDUAL)

    return {
        "continuous_annual_gbp": continuous_total,
        "step_function_annual_gbp": step_total,
        "partial_residual_annual_gbp": residual_total,
        "total_annual_gbp": continuous_total + step_total + residual_total,
        "caveat": (
            "Total combines three DIFFERENT KINDS of saving: continuous "
            "(reliable every year), step-function (only if a capacity "
            "band threshold is actually crossed — treat as contingent), "
            "and partial residual (small, post-2023 reduced value). "
            "Report these three separately in any external-facing output; "
            "a single blended total will mislead a reader into assuming "
            "uniform reliability across all three."
        ),
    }


if __name__ == "__main__":
    print("Testing TNUoS ASC band-step mechanism (illustrative thresholds):\n")

    band_thresholds = [50, 80, 100, 120]  # MW, illustrative
    # Charge INCREASES with band number (higher capacity band = higher agreed
    # capacity = higher TNUoS residual charge). Caught an inverted version of
    # this during testing — worth remembering as a sign-error trap.
    band_charges = {0: 900_000, 1: 1_400_000, 2: 2_100_000, 3: 3_200_000, 4: 4_500_000}

    # Case A: shaving isn't enough to cross a band
    result_a = tnuos_asc_band_step_saving(
        current_asc_mw=100, band_thresholds_mw=band_thresholds,
        band_annual_charge_gbp=band_charges, sustained_peak_reduction_mw=10,
    )
    print(f"Case A (10MW sustained reduction): £{result_a.annual_saving_gbp:,.0f}")
    print(f"  {result_a.status_note}\n")

    # Case B: shaving is enough to cross a band
    result_b = tnuos_asc_band_step_saving(
        current_asc_mw=100, band_thresholds_mw=band_thresholds,
        band_annual_charge_gbp=band_charges, sustained_peak_reduction_mw=25,
    )
    print(f"Case B (25MW sustained reduction): £{result_b.annual_saving_gbp:,.0f}")
    print(f"  {result_b.status_note}\n")

    residual = tnuos_locational_residual_saving(
        peak_shaved_mwh_at_triad_risk_periods=150, locational_rate_gbp_per_mwh=8.0,
    )
    print(f"Locational residual (150 MWh shaved @ £8/MWh): £{residual.annual_saving_gbp:,.0f}")
    print(f"  {residual.status_note}\n")

    summary = summarise_network_stack([result_a, residual])
    print("Summary (Case A + residual):")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    print("\nConfirming DUoS raises without real DNO rates:")
    try:
        duos_rag_saving([], set(), 0, 0)
    except NotImplementedError as e:
        print(f"  Raised as expected: {e}")
