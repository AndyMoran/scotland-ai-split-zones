"""
benchmark.py

Reality-check baseline for Stage 4.

The point of this module is narrow but load-bearing: it holds the actual,
OBSERVED, blended revenue that real GB batteries earn today — across
wholesale, Balancing Mechanism, frequency response, and reserve, all
stacked together as best as a real operator can manage it.

This is deliberately NOT a sum of "best case average" product prices.
That sum-of-parts approach is what produced the £105-175k/MW/year figure
in the original Stage 4 brief, and it doesn't survive contact with actual
market data (see NOTES below). This module exists to stop that number
from silently coming back.

Data source note
-----------------
Modo Energy publishes monthly GB BESS revenue benchmarks. As of writing
there is no free public API for this — it's a research product, not an
open dataset like BMRS or NESO's CKAN portal. So this module:

  1. Hardcodes the published monthly figures we already have, with dates
     and sources, as a defensible reality-check range.
  2. Leaves a clearly-marked extension point (`fetch_latest_benchmark`)
     for whoever has a Modo Energy subscription to wire in a live pull.
  3. Falls back to the hardcoded range if no live source is configured,
     and says so loudly rather than silently using stale numbers.

This is the same discipline as the NESO Constraint Breakdown reconciliation
spike — don't commit an ingestion path until you know what you're actually
pulling and where its boundaries are.
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class BenchmarkPoint:
    period_label: str
    annual_run_rate_gbp_per_mw: float
    source: str
    source_date: date
    duration_class_hours: Optional[float] = None  # None = not duration-specific
    notes: str = ""


# Published monthly/period GB BESS blended revenue figures.
# These are ACTUAL observed revenue (all services combined), not theoretical
# product-by-product averages. Update this list as new published figures
# become available — do not delete old points, they're useful for the
# sensitivity/volatility picture.
KNOWN_BENCHMARKS: list[BenchmarkPoint] = [
    BenchmarkPoint(
        period_label="Feb 2026",
        annual_run_rate_gbp_per_mw=41_000,
        source="Modo Energy — ME BESS GB monthly revenue release",
        source_date=date(2026, 3, 5),
        notes="Down 23% from Jan 2026. Lowest monthly figure since Feb 2024. "
              "Wholesale spreads fell; BM was the only service to grow.",
    ),
    BenchmarkPoint(
        period_label="Jan 2026",
        annual_run_rate_gbp_per_mw=52_000,
        source="Modo Energy — ME BESS GB monthly revenue release",
        source_date=date(2026, 2, 4),
        notes="Up 9% from Dec 2025, still 44% lower than Jan 2025.",
    ),
    BenchmarkPoint(
        period_label="Dec 2025",
        annual_run_rate_gbp_per_mw=48_000,
        source="Modo Energy — ME BESS GB monthly revenue release",
        source_date=date(2026, 2, 4),
        notes="18-month low, referenced in the Jan 2026 release.",
    ),
    BenchmarkPoint(
        period_label="Sep 2025",
        annual_run_rate_gbp_per_mw=70_000,
        source="Modo Energy — ME BESS GB monthly revenue release",
        source_date=date(2025, 10, 1),
        notes="15% increase from Aug 2025.",
    ),
    BenchmarkPoint(
        period_label="Mar 2026",
        annual_run_rate_gbp_per_mw=70_000,
        source="Modo Energy — ME BESS GB monthly revenue release",
        source_date=date(2026, 4, 2),
        notes="Up 69% on Feb 2026. Record BM revenue; day-ahead spreads "
              "surged to £89/MWh from £40/MWh.",
    ),
    BenchmarkPoint(
        period_label="12mo to Apr 2026 (2hr duration)",
        annual_run_rate_gbp_per_mw=73_145,
        source="Modo Energy — 'How does a BESS make money?'",
        source_date=date(2026, 5, 19),
        duration_class_hours=2.0,
        notes="Wholesale + BM together = ~60% of stack (£43,829/MW/year). "
              "This is the closest published match to a 50MW/100MWh (2hr) "
              "system and should be the primary reality-check figure.",
    ),
]


def get_reality_check_range() -> dict:
    """
    Returns the range of observed blended revenue to sanity-check any
    modelled figure against. Use this as the ceiling test: if your
    modelled 'conventional stack' (arbitrage + DC + CM, no AI layer)
    comes out meaningfully above this range, something in the model
    is double-counting.
    """
    values = [b.annual_run_rate_gbp_per_mw for b in KNOWN_BENCHMARKS]
    two_hr_matches = [
        b for b in KNOWN_BENCHMARKS if b.duration_class_hours == 2.0
    ]
    return {
        "min_gbp_per_mw": min(values),
        "max_gbp_per_mw": max(values),
        "most_recent_12mo_2hr_match_gbp_per_mw": (
            two_hr_matches[-1].annual_run_rate_gbp_per_mw
            if two_hr_matches else None
        ),
        "n_data_points": len(values),
        "sources": sorted({b.source for b in KNOWN_BENCHMARKS}),
        "caveat": (
            "These are ALL-SERVICE blended actuals, not per-product figures. "
            "Do not decompose and re-sum these into 'arbitrage + FR + CM' "
            "without independent per-product data (see daahead.py, "
            "dc_auction.py, capacity_market.py) — and even then, expect the "
            "decomposed sum to be an upper bound, not the expected value, "
            "because of cannibalisation between arbitrage cycling and FR "
            "headroom requirements."
        ),
    }


def fetch_latest_benchmark(api_key: Optional[str] = None) -> BenchmarkPoint:
    """
    Extension point for a live pull from Modo Energy (subscription product)
    or an equivalent source. Not implemented here because Stage 4 should
    not depend on a paid API by default — the hardcoded KNOWN_BENCHMARKS
    list above is the working reality check until/unless this is wired up.
    """
    raise NotImplementedError(
        "No live benchmark source configured. Use get_reality_check_range() "
        "against KNOWN_BENCHMARKS, or wire in a subscription source here "
        "and set its result explicitly — don't silently fall back to a "
        "stale hardcoded number without flagging it in the report."
    )


def get_baseline_for_battery(
    battery_mw: float,
    duration_hours: float,
    use_conservative: bool = True,
) -> dict:
    """
    Returns a defensible baseline annual revenue figure (£/MW/year and
    total £/year) for a battery of the given size, based on observed
    market data rather than summed product assumptions.

    use_conservative=True picks the lower end of the recent range
    (reflecting the Feb 2026 £41k trough and the FR-saturation trend),
    which is the right default for an investable/defensible number.
    use_conservative=False uses the 12-month rolling average instead.
    """
    rc = get_reality_check_range()

    if duration_hours == 2.0 and rc["most_recent_12mo_2hr_match_gbp_per_mw"]:
        rolling_avg = rc["most_recent_12mo_2hr_match_gbp_per_mw"]
    else:
        rolling_avg = (rc["min_gbp_per_mw"] + rc["max_gbp_per_mw"]) / 2

    per_mw = rc["min_gbp_per_mw"] if use_conservative else rolling_avg

    return {
        "per_mw_gbp_per_year": per_mw,
        "total_gbp_per_year": per_mw * battery_mw,
        "basis": (
            "conservative (recent trough)" if use_conservative
            else "12-month rolling average, duration-matched where possible"
        ),
        "reality_check_range": rc,
    }


if __name__ == "__main__":
    # Quick sanity print — not a test suite, just a gut check when run directly.
    baseline = get_baseline_for_battery(battery_mw=50, duration_hours=2.0)
    print(f"Baseline basis: {baseline['basis']}")
    print(f"Per MW: £{baseline['per_mw_gbp_per_year']:,.0f}/MW/year")
    print(f"Total (50 MW): £{baseline['total_gbp_per_year']:,.0f}/year")
    print()
    print("Compare against original Stage 4 sum-of-parts estimate:")
    print("  Original: £105,000-175,000/MW/year (£5.25M-8.75M/year @ 50MW)")
    print(f"  Reality check range: £{baseline['reality_check_range']['min_gbp_per_mw']:,.0f}"
          f"-{baseline['reality_check_range']['max_gbp_per_mw']:,.0f}/MW/year")
