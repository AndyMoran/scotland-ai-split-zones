"""
epex_prices.py

Half-hourly GB day-ahead wholesale price series, for modelling wholesale
peak-shaving value against a co-located AI load.

Data source note
-----------------
Real GB day-ahead prices are published via Elexon BMRS / Elexon Insights
Solution (data.elexon.co.uk) and EPEX SPOT's own day-ahead auction
results. Neither is reachable from this environment's network allowlist
(no api.elexon.co.uk / epexspot.com access here) — so this module:

  1. Defines the exact shape a real pull should take (`fetch_day_ahead_prices`),
     so it's a one-function swap once run somewhere with API access.
  2. Ships a REPRESENTATIVE half-hourly price shape for a single illustrative
     day, built from PUBLISHED descriptive statistics (not fabricated point
     data) — see PRICE_SHAPE_SOURCE below — so the mechanics of peak-shaving
     can be prototyped honestly before real data is wired in.
  3. Refuses to let that illustrative shape be mistaken for grounded data:
     every function that returns it tags the result with
     `status="ILLUSTRATIVE"`, and the stack module (network_stack.py)
     must check that tag before treating any output as reportable.

This mirrors the benchmark.py discipline from Stage 4: don't let a
placeholder quietly become load-bearing.
"""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Optional
import math

PRICE_SHAPE_SOURCE = (
    "Illustrative day built from published GB day-ahead descriptive "
    "statistics (Modo Energy Mar 2026 release: day-ahead spread reached "
    "£89/MWh during the gas-price spike month; typical spreads run "
    "£30-50/MWh). NOT a real BMRS/EPEX settlement series. Replace via "
    "fetch_day_ahead_prices() before this feeds any published figure."
)


@dataclass
class HalfHourlyPrice:
    period_start: datetime
    price_gbp_per_mwh: float
    status: str = "ILLUSTRATIVE"  # or "GROUNDED" once real data is wired in


def fetch_day_ahead_prices(
    target_date: date,
    zone: str = "GB",
    api_key: Optional[str] = None,
) -> list[HalfHourlyPrice]:
    """
    Extension point for a real pull — Elexon BMRS Insights Solution
    (MID / day-ahead auction data) or EPEX SPOT GB auction results.

    Not implemented here: this environment can't reach either API.
    Wire this in wherever the pipeline actually runs, and make sure
    every returned HalfHourlyPrice gets status="GROUNDED" with the
    source explicitly recorded, not just left at the dataclass default.
    """
    raise NotImplementedError(
        "No live wholesale price source reachable from this environment. "
        "Use get_illustrative_day() for prototyping, or wire in a real "
        "BMRS/EPEX pull elsewhere and mark results status='GROUNDED'."
    )


def get_illustrative_day(target_date: date, base_spread_gbp_per_mwh: float = 40.0) -> list[HalfHourlyPrice]:
    """
    Returns 48 half-hourly prices for a single illustrative day, shaped
    like a typical GB demand curve (overnight trough, morning ramp,
    evening peak) and scaled to a published typical spread. This is for
    PROTOTYPING MECHANICS ONLY — see PRICE_SHAPE_SOURCE.

    base_spread_gbp_per_mwh: peak-to-trough spread to scale the shape to.
    Default 40.0 reflects the "typical" (non-spike) spread; pass 89.0 to
    reproduce the March 2026 gas-price-spike scenario for stress-testing.
    """
    prices = []
    trough = 35.0  # illustrative overnight low, £/MWh
    for hh in range(48):
        hour = hh / 2.0
        # Simple double-hump shape: morning ramp + evening peak, both
        # scaled by base_spread_gbp_per_mwh. Illustrative only.
        morning = math.exp(-((hour - 8.0) ** 2) / 6.0)
        evening = math.exp(-((hour - 18.0) ** 2) / 4.0) * 1.3  # evening > morning
        shape = max(morning, evening)
        price = trough + shape * base_spread_gbp_per_mwh
        period_start = datetime.combine(target_date, datetime.min.time()) + timedelta(minutes=30 * hh)
        prices.append(HalfHourlyPrice(
            period_start=period_start,
            price_gbp_per_mwh=round(price, 2),
            status="ILLUSTRATIVE",
        ))
    return prices


def get_peak_troughs(prices: list[HalfHourlyPrice], n: int = 6) -> list[HalfHourlyPrice]:
    """Returns the n highest-price half-hour periods, for peak-shaving targeting."""
    return sorted(prices, key=lambda p: p.price_gbp_per_mwh, reverse=True)[:n]


def assert_all_grounded(prices: list[HalfHourlyPrice]) -> None:
    """
    Call this before letting any price series feed a figure that will be
    reported externally. Raises if any illustrative data is present.
    """
    illustrative = [p for p in prices if p.status != "GROUNDED"]
    if illustrative:
        raise ValueError(
            f"{len(illustrative)}/{len(prices)} price points are "
            f"ILLUSTRATIVE, not GROUNDED. Do not report figures derived "
            f"from this series without replacing with a real BMRS/EPEX pull."
        )


if __name__ == "__main__":
    day = get_illustrative_day(date(2026, 7, 15))
    print(f"Illustrative day: {len(day)} half-hourly periods")
    print(f"Status: {day[0].status} — {PRICE_SHAPE_SOURCE}\n")

    top6 = get_peak_troughs(day, n=6)
    print("Top 6 half-hourly price periods (peak-shaving targets):")
    for p in top6:
        print(f"  {p.period_start.strftime('%H:%M')}  £{p.price_gbp_per_mwh:.2f}/MWh  [{p.status}]")

    print("\nConfirming the guard rail raises on illustrative data:")
    try:
        assert_all_grounded(day)
    except ValueError as e:
        print(f"  Raised as expected: {e}")
