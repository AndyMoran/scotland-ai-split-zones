"""
tnuos_central_belt.py

Stage 6 — TNUoS residual band-step economics for a Central Belt inference site.

Source: NESO Final TNUoS Tariffs for 2026/27, Table 10 (Non-Locational demand
residual charges), effective 1 April 2026.
https://www.neso.energy/document/376336/download

Band thresholds (RIIO-ET3, locked 2026/27-2030/31, unchanged between Draft
and Final): NESO, Draft Forecast of TNUoS Tariffs for 2026/27 Webinar.
https://www.neso.energy/document/375476/download

Confirms and refines Stage 5's finding: post-2023 TCR, the demand residual is
genuinely non-locational — "all sites within the same band pay the same demand
residual tariff regardless of which demand zone they are in" (NESO, Final
Tariffs document, Demand Residual Tariffs section). The mechanism that
mattered for Stage 5's 100MW/EHV training site — moving to a lower capacity
BAND, not avoiding a ZONE — applies identically here, just at a different
band tier.
"""

from dataclasses import dataclass


@dataclass
class TnuosResidualBand:
    band_name: str
    gbp_per_site_per_day: float
    lower_threshold_kva: float
    upper_threshold_kva: float
    source: str = "NESO Final TNUoS Tariffs 2026/27, Table 10"
    evidence_status: str = "GROUNDED"


# NESO Final TNUoS Tariffs 2026/27, Table 10 — HV bands, with RIIO-ET3
# thresholds (locked for 2026/27-2030/31) from NESO's Draft Forecast webinar.
HV_BANDS = [
    TnuosResidualBand("HV1", 31.839048, 0, 500),
    TnuosResidualBand("HV2", 117.152788, 500, 1100),
    TnuosResidualBand("HV3", 185.418505, 1100, 2000),
    TnuosResidualBand("HV4", 528.912335, 2000, float("inf")),
]


def annual_cost_gbp(band: TnuosResidualBand) -> float:
    return band.gbp_per_site_per_day * 365


def assign_band(capacity_mw: float, power_factor: float = 0.95) -> TnuosResidualBand:
    """
    Assigns a site to its TNUoS HV residual band based on agreed capacity
    (MIC), converted from MW to kVA. This replaces the earlier OMITTED
    ledger item — the assignment is unambiguous for a 5MW site (~2.6x the
    HV4 lower threshold of 2,000kVA), so no band-boundary judgement call
    is needed here. (Corrected: an earlier version of this comment said
    "~10x", which mistakenly compared the site's kVA to the HV1 band's
    upper bound (500kVA) rather than HV4's actual lower bound (2,000kVA).
    The band assignment itself was never wrong — only this multiplier was.)
    """
    capacity_kva = capacity_mw * 1000 / power_factor
    for band in HV_BANDS:
        if band.lower_threshold_kva < capacity_kva <= band.upper_threshold_kva:
            return band
    raise ValueError(f"{capacity_kva:.0f} kVA does not fall within any defined HV band.")


def band_step_saving(current_band: TnuosResidualBand, lower_band: TnuosResidualBand) -> dict:
    """
    Mirrors Stage 5's tnuos_asc_band_step_saving logic: the saving from
    crossing from a higher band to a lower one via a sustained, formal
    capacity reduction. Same step-function behaviour — no saving without
    actually crossing a threshold; this is a contractual/capacity decision,
    not a dispatch decision.
    """
    saving = annual_cost_gbp(current_band) - annual_cost_gbp(lower_band)
    return {
        "from_band": current_band.band_name,
        "to_band": lower_band.band_name,
        "annual_saving_gbp": round(saving, 2),
        "behaviour": "step_function",
        "note": (
            "Requires a formal, sustained capacity reduction (agreed with the "
            "DNO), not opportunistic peak-shaving. Same mechanism as Stage 5's "
            "ASC Band Step, applied to the HV band tier rather than EHV."
        ),
    }


# ─────────────────────────────────────────────────────────────────────────
# ASSUMPTIONS LEDGER (Stage 6, TNUoS component)
# ─────────────────────────────────────────────────────────────────────────
ASSUMPTIONS_LEDGER = [
    ("HV band rates", "HV1 £31.84 - HV4 £528.91 per site/day",
     "GROUNDED — NESO Final TNUoS Tariffs 2026/27, Table 10"),
    ("HV band thresholds", "HV1 <=500kVA, HV2 <=1,100kVA, HV3 <=2,000kVA, HV4 >2,000kVA",
     "GROUNDED — NESO Draft Forecast of TNUoS Tariffs 2026/27 Webinar; RIIO-ET3 "
     "thresholds are locked for 2026/27-2030/31 and unchanged between Draft and Final"),
    ("5MW site band assignment", "HV4 (~5,263 kVA at 0.95 PF, ~2.6x the HV4 lower threshold of 2,000kVA)",
     "GROUNDED — unambiguous, not a boundary judgement call. (Corrected from an earlier "
     "'~10x' claim, which compared against the wrong threshold — HV1's 500kVA upper "
     "bound, not HV4's 2,000kVA lower bound.)"),
    ("Non-locational confirmation", "Same band = same charge regardless of demand zone",
     "GROUNDED — direct quote from NESO's own methodology text"),
    ("Power factor assumption", "0.95, typical for commercial/colo load",
     "PROVISIONAL — real site PF would need confirming, though the band "
     "assignment is robust to reasonable PF variation given the site sits "
     "well clear of the threshold at any plausible PF"),
    ("Locational (Triad/HH) component", "Not yet sourced — Table 11, demand zone-specific",
     "OMITTED — NESO's own text confirms this is a smaller additional "
     "component on top of the residual; residual is 'the majority' of the "
     "TNUoS demand charge, per NESO's own wording."),
]


if __name__ == "__main__":
    print("Stage 6 — TNUoS HV Residual Bands, 2026/27 (NESO Final Tariffs)")
    print("=" * 65)
    for band in HV_BANDS:
        print(f"  {band.band_name}: £{band.gbp_per_site_per_day:.2f}/day "
              f"-> £{annual_cost_gbp(band):,.0f}/year")

    print("\nAsanti Livingston (5MW) band assignment:")
    assigned = assign_band(5.0)
    print(f"  Assigned band: {assigned.band_name}")
    print(f"  Annual TNUoS residual: £{annual_cost_gbp(assigned):,.0f}/year")

    print("\nBand-step saving potential (HV4 -> HV3, most achievable single step):")
    result = band_step_saving(HV_BANDS[3], HV_BANDS[2])
    for k, v in result.items():
        print(f"  {k}: {v}")

    print("\nBand-step saving potential (HV4 -> HV1, maximum theoretical):")
    result = band_step_saving(HV_BANDS[3], HV_BANDS[0])
    for k, v in result.items():
        print(f"  {k}: {v}")

    print("\nAssumptions Ledger:")
    for assumption, detail, status in ASSUMPTIONS_LEDGER:
        print(f"\n  {assumption}:")
        print(f"    {detail}")
        print(f"    Status: {status}")