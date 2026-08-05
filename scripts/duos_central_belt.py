"""
duos_central_belt.py

Stage 6 — Behind-the-Meter Economics for Central Belt Inference Siting

Sources SP Distribution's real DUoS tariffs (not SHEPD — Central Belt sits in
SP Energy Networks' territory, not SSEN's) for a representative inference-scale
site, and computes the RAG-avoidance differential the same way Stage 5 did for
the Northern Scotland training site.

Source: SP Distribution Use of System Charging Statement, Notice of Charges,
effective 1 April 2026, Annex 1 (LV and HV Designated Properties).
https://www.scottishpower.com/documents/d/guest/lc14-statement-2026_spd_v01

Voltage tier note (this is a modelling assumption, not a sourced fact):
Stage 5's training site was 100MW at 132kV/EHV — full hyperscale transmission
connection. This project's own PROJECT.md (Section 2) describes inference as
"smaller footprint" than training. A representative Central Belt inference
site — retrofitted into brownfield/office-block sites per the Stage 1 thesis —
is assumed here to connect at HV, not EHV. This assumption should be revisited
once a specific representative site (MW scale, connection type) is chosen;
see ASSUMPTIONS_LEDGER at the bottom of this file.
"""

from dataclasses import dataclass
from enum import Enum


class ChargeBehaviour(Enum):
    CONTINUOUS = "continuous"        # same behavioural category as Stage 5's DUoS line


@dataclass
class DuosTariff:
    tariff_name: str
    red_black_p_kwh: float
    amber_yellow_p_kwh: float
    green_p_kwh: float
    fixed_p_mpan_day: float
    capacity_p_kva_day: float
    source: str
    evidence_status: str = "GROUNDED"


# SP Distribution Annex 1, HV Site Specific No Residual (M00/N00),
# effective 1 April 2026. This is the "No Residual" band — a real site would
# be allocated to a residual charging Band (0-4) based on its consumption
# profile; No Residual is used here as the conservative floor, consistent
# with how Stage 5 used a single representative SHEPD tariff rather than
# resolving exact banding. Flagged PROVISIONAL for that reason.
SPD_HV_SITE_SPECIFIC = DuosTariff(
    tariff_name="SP Distribution HV Site Specific (No Residual)",
    red_black_p_kwh=4.377,
    amber_yellow_p_kwh=0.322,
    green_p_kwh=0.010,
    fixed_p_mpan_day=159.79,
    capacity_p_kva_day=8.99,
    source="SP Distribution Charging Statement, Annex 1, effective 1 Apr 2026",
    evidence_status="GROUNDED (rate) / PROVISIONAL (residual band assumed 'No Residual')",
)


def p_kwh_to_gbp_mwh(p_kwh: float) -> float:
    """p/kWh -> £/MWh is a straight x10 conversion (1 MWh = 1000 kWh, 100p = £1)."""
    return p_kwh * 10


def get_duos_differential_gbp_mwh(tariff: DuosTariff) -> dict:
    """
    Returns the Red-Green DUoS differential in £/MWh — the value a battery
    captures per MWh shifted out of Red periods, mirroring Stage 5's
    duos_red_rate / duos_green_rate structure exactly.
    """
    red = p_kwh_to_gbp_mwh(tariff.red_black_p_kwh)
    green = p_kwh_to_gbp_mwh(tariff.green_p_kwh)
    return {
        "red_gbp_mwh": round(red, 2),
        "green_gbp_mwh": round(green, 2),
        "differential_gbp_mwh": round(red - green, 2),
        "source": tariff.source,
        "evidence_status": tariff.evidence_status,
    }


def compare_to_stage5_training_site() -> dict:
    """
    Traceability check: reproduces Stage 5's SHEPD 132kV/EHV figure alongside
    this stage's SP Distribution HV figure, so the voltage-tier comparison is
    auditable from one function call rather than two separate scripts.
    """
    shepd_diff = 1.58  # Stage 5, sourced SSEN SHEPD 132kV/EHV, Red £1.58/MWh - Green £0.00/MWh
    spd = get_duos_differential_gbp_mwh(SPD_HV_SITE_SPECIFIC)
    ratio = spd["differential_gbp_mwh"] / shepd_diff

    return {
        "stage5_shepd_132kv_ehv_differential_gbp_mwh": shepd_diff,
        "stage6_spd_hv_differential_gbp_mwh": spd["differential_gbp_mwh"],
        "ratio": round(ratio, 1),
        "interpretation": (
            f"The Central Belt HV inference-scale differential is {ratio:.1f}x "
            f"larger than the hyperscale 132kV/EHV training-site differential. "
            f"This mirrors Stage 5's voltage-sensitivity finding from the other "
            f"direction: DUoS value scales down with voltage, not up with load."
        ),
    }


# ─────────────────────────────────────────────────────────────────────────
# ASSUMPTIONS LEDGER (Stage 6, DUoS component)
# ─────────────────────────────────────────────────────────────────────────
ASSUMPTIONS_LEDGER = [
    ("SP Distribution HV rates", "Red £43.77/MWh, Green £0.10/MWh",
     "GROUNDED — sourced from SP Distribution Charging Statement, Annex 1, eff. 1 Apr 2026"),
    ("Voltage tier (HV, not EHV)", "Representative inference site assumed HV-connected",
     "PROVISIONAL — no specific site chosen yet; revisit once MW scale is set"),
    ("Residual charging band", "'No Residual' band used as conservative floor",
     "PROVISIONAL — real site would be banded 0-4 by consumption profile"),
    ("Site MW scale", "Not yet set — Stage 5 used 100MW; inference is 'smaller footprint' per PROJECT.md §2",
     "OMITTED — required before annual £/year figures can be computed"),
]


if __name__ == "__main__":
    print("Stage 6 — SP Distribution DUoS, Central Belt Inference Site")
    print("=" * 65)
    result = get_duos_differential_gbp_mwh(SPD_HV_SITE_SPECIFIC)
    for k, v in result.items():
        print(f"  {k}: {v}")

    print("\nTraceability check against Stage 5:")
    comparison = compare_to_stage5_training_site()
    for k, v in comparison.items():
        print(f"  {k}: {v}")

    print("\nAssumptions Ledger:")
    for assumption, detail, status in ASSUMPTIONS_LEDGER:
        print(f"\n  {assumption}:")
        print(f"    {detail}")
        print(f"    Status: {status}")