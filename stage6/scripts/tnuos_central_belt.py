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

    IMPORTANT: this function computes the saving IF the step is achievable.
    It does not check whether it actually is — that requires
    feasible_band_step() below, which checks the target band's ceiling
    against the site's own minimum load. Computing a saving from the tariff
    table alone, without that check, is exactly the mistake an earlier
    version of this analysis made — flagged in conversation, not caught by
    review, worth being honest about that.
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


def feasible_band_step(current_band: TnuosResidualBand, site_min_load_mw: float,
                        power_factor: float = 0.95) -> dict:
    """
    Checks whether ANY lower band is actually reachable, given the site's
    own minimum load — not just whether the tariff table shows a saving.
    A site can't reduce its agreed capacity below what it actually draws;
    a band-step saving that requires cutting capacity under the site's own
    floor demand isn't a saving, it's an outage.

    This is the check that was missing from the original band_step_saving()
    usage: computing "£181,432/year available" from the tariff table alone,
    without checking against a real load profile, overstated what this
    specific site can actually capture.
    """
    lower_bands = [b for b in HV_BANDS if b.upper_threshold_kva < current_band.upper_threshold_kva]
    results = []
    for band in lower_bands:
        ceiling_mw = band.upper_threshold_kva * power_factor / 1000
        reachable = site_min_load_mw <= ceiling_mw
        results.append({
            "band": band.band_name,
            "ceiling_mw": round(ceiling_mw, 2),
            "reachable": reachable,
            "shortfall_mw": round(site_min_load_mw - ceiling_mw, 2) if not reachable else 0.0,
        })
    any_reachable = any(r["reachable"] for r in results)
    return {
        "current_band": current_band.band_name,
        "site_min_load_mw": site_min_load_mw,
        "band_checks": results,
        "any_band_step_feasible": any_reachable,
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
    ("Saving capture route", "Via the site's electricity supply contract (pass-through), not a direct NESO relationship",
     "PARTIALLY GROUNDED — a second review caught that this was overstated as "
     "GROUNDED when one link in the chain wasn't sourced. Confirmed: TNUoS "
     "applies to Suppliers and directly-connected transmission demand, not "
     "distribution-connected demand sites directly (NESO's own scope "
     "statement). NOT confirmed: whether the DNO-agreed MIC specifically is "
     "the 'capacity' figure NESO uses to reassign a site's demand residual "
     "band, versus metered demand or another reported figure — inferred from "
     "adjacent facts, not sourced directly. Also not confirmed: contract-"
     "specific pass-through timing."),
    ("Band-step saving feasibility for this specific site", "NOT feasible — no lower band is reachable",
     "GROUNDED — checked directly via feasible_band_step(), not assumed. The "
     "site's own minimum load (4.0MW overnight) exceeds even HV3's ceiling "
     "(~1.90MW at 0.95 PF) by more than 2MW. HV1 and HV2 are further out of "
     "reach again. HV4 isn't a starting point with room to improve for this "
     "site — it's the only band this site's real load profile can ever "
     "occupy. An earlier version of this analysis computed £125,375/yr and "
     "£181,432/yr 'potential savings' straight from the tariff table without "
     "checking this — a real error, caught in conversation, not by review."),
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

    print("\nBand-step saving — computed from the tariff table alone (this is NOT")
    print("the same as feasible; see the check below):")
    result = band_step_saving(HV_BANDS[3], HV_BANDS[2])
    for k, v in result.items():
        print(f"  {k}: {v}")

    print("\nIs this saving actually achievable, given the site's real load profile?")
    feasibility = feasible_band_step(assigned, site_min_load_mw=4.0)
    for check in feasibility["band_checks"]:
        status = "REACHABLE" if check["reachable"] else f"NOT REACHABLE (short by {check['shortfall_mw']}MW)"
        print(f"  {check['band']}: ceiling {check['ceiling_mw']}MW -> {status}")
    print(f"  Any band-step feasible for this site: {feasibility['any_band_step_feasible']}")
    print("  Conclusion: the tariff-table saving above is real for a DIFFERENT")
    print("  site with more headroom between its minimum load and a lower band's")
    print("  ceiling. For THIS site, it isn't available at all.")

    print("\nAssumptions Ledger:")
    for assumption, detail, status in ASSUMPTIONS_LEDGER:
        print(f"\n  {assumption}:")
        print(f"    {detail}")
        print(f"    Status: {status}")