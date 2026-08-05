"""
inference_load_central_belt.py

Stage 6 — Inference site load profile, built to close the gap flagged in
STAGE6_SYNTHESIS.md: the DUoS differential (£43.67/MWh) was real, but had no
realised annual £/year figure because no load profile existed to convert it.

This profile is deliberately NOT a scaled-down copy of Stage 5's training
profile. Stage 5's "70% baseline + spikes to 100%" shape represented
scheduled training-job starts — a mechanism that doesn't exist for inference.
Inference load tracks user demand continuously; the physically correct shape
is a diurnal curve, not discrete spikes.

Evidence base for the shape (status: SYNTHETIC, evidence-INFORMED — see
PROFILE_EVIDENCE below). This is not real telemetry from a real facility;
no such data is publicly available at this granularity. It is a physically
motivated curve built from published measurements of comparable systems,
which is a meaningfully stronger basis than an arbitrary function, but must
not be reported as if it were the site's own metered data.
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta
import math

PROFILE_EVIDENCE = """
Two separate, real measurements inform this profile, and it's important they
are not conflated:

1. TIMING of the diurnal peak — measured, not assumed:
   A 2026 measurement study of real generative-AI inference data centre power
   ("Measurement of Generative AI Workload Power Profiles for Whole-Facility
   Data Center Infrastructure Planning") found requests "ramping up after 9 AM
   and decreasing after 10 PM," with job submission "increasing after 8 AM,
   with peaks after 4 PM." This profile uses that timing directly: ramp from
   ~08:00, peak window ~16:00-19:00, decline from ~22:00.

2. MAGNITUDE of diurnal power variation — measured, not assumed, and
   deliberately NOT taken from request-volume figures:
   Request/query volume for inference services can vary by an order of
   magnitude peak-to-trough (vendor sources cite ~10x). ACTUAL POWER DRAW
   varies far less, because idle GPU/server power floors and non-power-
   proportional infrastructure (storage, baseline cooling) damp the
   relationship between request volume and site power. Measured CPU
   utilisation diurnal variation: Meta ~20%, Google ~15% (cited in Bhardwaj
   et al., "Shaved Ice," arXiv:2503.10235). This profile uses 25% peak-to-
   trough power variation — within, and toward the upper end of, that
   measured range, i.e. a deliberately conservative (higher-value) choice
   for the purposes of this stage, since a larger swing gives the battery
   more genuine peak to shave rather than less.

Do not use request-volume variability figures (e.g. "10x") to justify power
variation in this or any downstream module. That would conflate two
different measured quantities and materially overstate the shavable peak.
"""


@dataclass
class LoadPoint:
    period_start: datetime
    load_mw: float
    status: str = "SYNTHETIC_EVIDENCE_INFORMED"


def generate_inference_load_profile(
    target_date: date,
    site_capacity_mw: float = 5.0,
    peak_to_trough_variation: float = 0.25,
    peak_hour: float = 17.5,  # mid-point of the measured 16:00-19:00 peak window
) -> list:
    """
    Generates a 48-period half-hourly diurnal load profile for the inference
    site. Continuous curve, not discrete spikes — this is the physical
    distinction from Stage 5's training profile.

    trough_mw is set so that peak load reaches site_capacity_mw (the site
    runs at full contracted capacity during its daily peak window, which is
    the standard basis on which a site's MIC/capacity is set in the first
    place).
    """
    trough_mw = site_capacity_mw / (1 + peak_to_trough_variation)
    swing_mw = site_capacity_mw - trough_mw

    points = []
    for hh in range(48):
        hour = hh / 2.0
        # Smooth diurnal curve: low overnight, ramp from ~08:00, broad peak
        # centred on 17:30 (mid-point of the measured 16:00-19:00 peak
        # window), decline from ~22:00. A single broad Gaussian centred on
        # the peak hour, floored at the trough, is the simplest credible
        # shape that matches the measured ramp/peak/decline timing without
        # inventing sharper structure the evidence doesn't support.
        shape = math.exp(-((hour - peak_hour) ** 2) / 18.0)
        load = trough_mw + swing_mw * shape
        period_start = datetime.combine(target_date, datetime.min.time()) + timedelta(minutes=30 * hh)
        points.append(LoadPoint(period_start=period_start, load_mw=round(load, 3)))

    return points


def check_battery_coverage(
    profile: list,
    battery_mw: float,
    red_band_start_hour: float = 16.5,
    red_band_end_hour: float = 19.5,
) -> dict:
    """
    Validates the mechanism the DUoS calculation depends on: does site load
    stay at or above the battery's rated MW throughout the DUoS Red band
    (16:30-19:30, per SP Distribution's Annex 1 time bands) for every period
    in the profile? If not, the battery cannot discharge at full rated MW
    for the full Red window on every day represented by this profile, and
    the "shave at full battery MW for all Red periods" assumption from
    duos_central_belt.py does not hold without qualification.
    """
    red_band_points = [
        p for p in profile
        if red_band_start_hour <= (p.period_start.hour + p.period_start.minute / 60) < red_band_end_hour
    ]
    shortfalls = [p for p in red_band_points if p.load_mw < battery_mw]

    return {
        "n_red_band_periods": len(red_band_points),
        "n_shortfall_periods": len(shortfalls),
        "min_load_in_red_band_mw": min(p.load_mw for p in red_band_points),
        "battery_mw": battery_mw,
        "coverage_confirmed": len(shortfalls) == 0,
    }


def realised_annual_duos_value(
    battery_mw: float,
    duos_differential_gbp_mwh: float,
    red_band_hours_per_day: float = 3.0,  # 16:30-19:30, per SP Distribution Annex 1
    days_per_year: int = 365,
) -> dict:
    """
    Converts the DUoS differential (grounded in duos_central_belt.py) into a
    realised annual £ figure, GIVEN that battery coverage has been confirmed
    for the full Red band. This is the number that was missing from
    STAGE6_SYNTHESIS.md's Finding 1.

    This is a GROSS figure: it assumes charging and discharging happen at
    zero loss, and does not distinguish where in the day the battery
    recharges. See net_annual_duos_value() for the loss-adjusted figure —
    the gap between the two turns out to be small in the intended
    operating case, but not negligible if charging discipline slips.
    """
    annual_shaved_mwh = battery_mw * red_band_hours_per_day * days_per_year
    annual_value_gbp = annual_shaved_mwh * duos_differential_gbp_mwh
    return {
        "battery_mw": battery_mw,
        "annual_shaved_mwh": round(annual_shaved_mwh, 1),
        "duos_differential_gbp_mwh": duos_differential_gbp_mwh,
        "annual_value_gbp": round(annual_value_gbp, 0),
        "status": "GROSS — no losses, no charging-period assumption",
    }


def required_energy_capacity_mwh(battery_mw: float, red_band_hours_per_day: float = 3.0) -> dict:
    """
    States the battery's ENERGY (MWh) requirement explicitly, separate from
    its power (MW) rating. A "2.5MW battery" says nothing about whether it
    can sustain 3 hours of discharge — that depends on installed MWh, not
    MW. Flagged by external review; the earlier version of this module
    specified MW only.
    """
    usable_mwh_minimum = battery_mw * red_band_hours_per_day
    return {
        "battery_mw": battery_mw,
        "red_band_hours": red_band_hours_per_day,
        "usable_mwh_minimum": usable_mwh_minimum,
        "note": (
            f"Minimum USABLE energy capacity to sustain {red_band_hours_per_day}h "
            f"of discharge at {battery_mw}MW is {usable_mwh_minimum}MWh, assuming "
            f"100% depth of discharge (no SOC reserve). Installed NAMEPLATE "
            f"capacity would need to be higher than this to allow for SOC "
            f"reserve/DoD limits and degradation over asset life — by how much "
            f"is not quantified here; doing so requires a specific battery "
            f"chemistry and degradation curve, which this stage does not model."
        ),
    }


def net_annual_duos_value(
    battery_mw: float,
    red_rate_gbp_mwh: float,
    charge_rate_gbp_mwh: float,
    round_trip_efficiency: float = 0.85,
    red_band_hours_per_day: float = 3.0,
    days_per_year: int = 365,
) -> dict:
    """
    Loss-adjusted DUoS value: discharge revenue at the Red rate, minus the
    cost of the charging energy actually required to deliver that
    discharge once round-trip efficiency is accounted for.

    round_trip_efficiency=0.85 reuses Stage 3's established AC-AC RTE
    figure for this project, for consistency rather than introducing a
    new unjustified number.

    charge_rate_gbp_mwh is a parameter, not hardcoded to Green, because
    the whole point of this function is to show how much the result
    depends on WHEN charging actually happens — see the worked comparison
    in this file's __main__ block.
    """
    discharge_mwh_daily = battery_mw * red_band_hours_per_day
    charge_mwh_daily = discharge_mwh_daily / round_trip_efficiency

    discharge_value_daily = discharge_mwh_daily * red_rate_gbp_mwh
    charge_cost_daily = charge_mwh_daily * charge_rate_gbp_mwh
    net_daily = discharge_value_daily - charge_cost_daily

    return {
        "discharge_mwh_daily": round(discharge_mwh_daily, 2),
        "charge_mwh_daily_required": round(charge_mwh_daily, 2),
        "round_trip_efficiency": round_trip_efficiency,
        "charge_rate_gbp_mwh": charge_rate_gbp_mwh,
        "net_daily_gbp": round(net_daily, 2),
        "net_annual_gbp": round(net_daily * days_per_year, 0),
    }


# ─────────────────────────────────────────────────────────────────────────
# ASSUMPTIONS LEDGER (Stage 6, load profile component)
# ─────────────────────────────────────────────────────────────────────────
ASSUMPTIONS_LEDGER = [
    ("Diurnal peak timing (16:00-19:00)", "Ramp from 08:00, peak 16:00-19:00, decline from 22:00",
     "GROUNDED (timing) — measured generative-AI inference data centre study, "
     "'requests ramping up after 9 AM and decreasing after 10 PM,' peaks after 4PM"),
    ("Diurnal power magnitude (25% peak-to-trough)", "Within measured range 15-34%",
     "GROUNDED (range) / PROVISIONAL (specific 25% choice within that range) — "
     "Meta ~20%, Google ~15% (CPU utilisation), Shaved Ice paper's own workload 34% "
     "(all cited in arXiv:2503.10235). Deliberately NOT using request-volume "
     "variability (~10x, different quantity, would overstate the shavable peak)."),
    ("Battery size (2.5MW, 50% of site capacity)", "Same ratio as Stage 4/5's 50MW/100MW site",
     "PROVISIONAL — consistency choice for comparability with Stage 4/5, not "
     "independently justified for a pure peak-shaving (non-merchant-stacking) "
     "use case, which may support a different, possibly smaller, sizing"),
    ("Battery energy capacity (MWh, not just MW)", "Minimum 7.5MWh usable (2.5MW x 3h)",
     "GROUNDED (minimum) / OMITTED (installed nameplate headroom) — flagged by "
     "external review; MW alone does not establish the battery can sustain the "
     "full Red-band discharge. Nameplate capacity above 7.5MWh, to allow for "
     "SOC reserve and degradation, is not quantified — needs a specific "
     "chemistry/degradation model this stage doesn't build."),
    ("Round-trip efficiency (85%)", "Reused from Stage 3's established AC-AC figure",
     "GROUNDED — not a new assumption; deliberately kept consistent with the "
     "rest of the project rather than introducing an unjustified new RTE value"),
    ("Net vs gross DUoS value", "£119,547/yr gross; ~£119,498/yr net if charging stays in Green",
     "GROUNDED — computed, not asserted. Net value is ~100% of gross only "
     "because Green-period charging is cheap enough that RTE losses barely "
     "register in £ terms. This is charging-discipline-dependent, not a free "
     "pass — see the Amber/Red sensitivity in this file's __main__ output."),
    ("Curve shape (single Gaussian)", "Simplest credible shape matching measured timing",
     "DELIBERATE — Sledgehammer Test: no evidence supports a more complex "
     "shape (e.g. bimodal, weekday/weekend split) at this stage"),
]


if __name__ == "__main__":
    target = date(2026, 8, 5)  # arbitrary Wednesday, non-Triad-season
    site_mw = 5.0
    battery_mw = site_mw * 0.5  # 2.5MW, mirroring Stage 4/5's 50% ratio

    profile = generate_inference_load_profile(target, site_capacity_mw=site_mw)

    print("Stage 6 — Inference Load Profile")
    print("=" * 65)
    print(f"Site capacity: {site_mw} MW | Battery: {battery_mw} MW\n")

    print("Sample points (every 4 hours):")
    for p in profile[::8]:
        print(f"  {p.period_start.strftime('%H:%M')}  {p.load_mw:.2f} MW  [{p.status}]")

    print("\nBattery coverage check (Red band 16:30-19:30):")
    coverage = check_battery_coverage(profile, battery_mw)
    for k, v in coverage.items():
        print(f"  {k}: {v}")

    print("\nRealised annual DUoS value (only valid because coverage confirmed above):")
    duos_diff = 43.67  # from duos_central_belt.py, SP Distribution HV differential
    value = realised_annual_duos_value(battery_mw, duos_diff)
    for k, v in value.items():
        print(f"  {k}: {v}")

    print("\nBattery energy (MWh) sizing — separate from the MW power rating:")
    sizing = required_energy_capacity_mwh(battery_mw)
    for k, v in sizing.items():
        print(f"  {k}: {v}")

    print("\nNet vs gross DUoS value — sensitivity to WHEN the battery recharges:")
    red_rate = 43.77
    for label, charge_rate in [("Green (£0.10/MWh)", 0.10),
                                ("Amber (£3.22/MWh)", 3.22),
                                ("Red (£43.77/MWh — should never happen operationally)", 43.77)]:
        net = net_annual_duos_value(battery_mw, red_rate, charge_rate)
        pct_of_gross = net["net_annual_gbp"] / value["annual_value_gbp"] * 100
        print(f"  Charging in {label}: net £{net['net_annual_gbp']:,.0f}/year "
              f"({pct_of_gross:.1f}% of gross)")
    print("  -> Charging discipline (staying in Green) is what makes gross ≈ net.")
    print("     This is an operating requirement, not a free assumption.")

    print("\nAssumptions Ledger:")
    for assumption, detail, status in ASSUMPTIONS_LEDGER:
        print(f"\n  {assumption}:")
        print(f"    {detail}")
        print(f"    Status: {status}")