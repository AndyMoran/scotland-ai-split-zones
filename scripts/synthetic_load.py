"""
synthetic_load.py

A synthetic 100MW AI data centre load profile, for testing WHEN a
battery's peak-shaving capability overlaps with wholesale/network peaks.

Status: this is legitimately synthetic by design, not a placeholder for
missing real data (unlike epex_prices.py's illustrative day). No public
half-hourly load trace exists for a specific hyperscale AI site, so a
synthetic profile is the correct tool here — but it still needs to be
clearly labelled as a modelling convenience, not a claim about any real
facility's actual behaviour.
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Optional
import random


@dataclass
class LoadPoint:
    period_start: datetime
    load_mw: float
    status: str = "SYNTHETIC"


def generate_ai_load_profile(
    target_date: date,
    baseline_mw: float = 70.0,
    peak_mw: float = 100.0,
    n_training_spikes: int = 2,
    spike_duration_hh: int = 4,
    seed: Optional[int] = 42,
) -> list[LoadPoint]:
    """
    Generates a 48-period half-hourly load profile: a high baseline
    (inference/idle-not-idle — AI hardware rarely goes fully idle) with
    periodic training-run spikes to near-peak capacity.

    baseline_mw: continuous background load (default 70% of 100MW capacity —
                 reflects that AI hardware draws significant power even
                 between training runs).
    peak_mw: load during a training spike.
    n_training_spikes: number of spike windows in the 24hr period.
    spike_duration_hh: length of each spike in half-hour periods
                        (default 4 = 2 hours).

    This is a MODELLING CONVENIENCE, not a claim about real hyperscaler
    behaviour. If real site data becomes available, replace this entirely
    rather than calibrating against it — a synthetic profile shouldn't be
    quietly upgraded to "grounded" just because it looks plausible.
    """
    rng = random.Random(seed)
    points = []

    # Pick spike start periods, spaced out, avoiding overlap
    available_starts = list(range(0, 48 - spike_duration_hh))
    spike_starts = []
    for _ in range(n_training_spikes):
        if not available_starts:
            break
        start = rng.choice(available_starts)
        spike_starts.append(start)
        available_starts = [
            s for s in available_starts
            if abs(s - start) > spike_duration_hh
        ]

    spike_periods = set()
    for start in spike_starts:
        spike_periods.update(range(start, start + spike_duration_hh))

    for hh in range(48):
        load = peak_mw if hh in spike_periods else baseline_mw
        period_start = datetime.combine(target_date, datetime.min.time()) + timedelta(minutes=30 * hh)
        points.append(LoadPoint(period_start=period_start, load_mw=load))

    return points


def get_peak_load_periods(load: list[LoadPoint], n: int = 6) -> list[LoadPoint]:
    """Returns the n highest-load half-hour periods."""
    return sorted(load, key=lambda p: p.load_mw, reverse=True)[:n]


def overlap_with_price_peaks(
    load: list[LoadPoint],
    price_peaks: set,  # set of datetime period_starts identified as price peaks
) -> dict:
    """
    Checks how much of the AI load's high-consumption periods coincide
    with wholesale price peaks — this overlap (or lack of it) is the
    actual mechanism that determines whether peak-shaving has anything
    to bite on. If load spikes and price peaks rarely coincide, battery
    peak-shaving value is structurally limited regardless of battery size.
    """
    load_peak_periods = {p.period_start for p in get_peak_load_periods(load, n=len(price_peaks))}
    overlap = load_peak_periods & price_peaks
    return {
        "n_load_peaks": len(load_peak_periods),
        "n_price_peaks": len(price_peaks),
        "n_overlapping": len(overlap),
        "overlap_fraction": len(overlap) / len(price_peaks) if price_peaks else 0.0,
    }


if __name__ == "__main__":
    day = date(2026, 7, 15)
    profile = generate_ai_load_profile(day)

    print(f"Synthetic AI load profile: {len(profile)} half-hourly periods")
    print(f"Baseline: 70 MW, Peak (training spike): 100 MW\n")

    top6 = get_peak_load_periods(profile, n=6)
    print("Top 6 highest-load periods:")
    for p in top6:
        print(f"  {p.period_start.strftime('%H:%M')}  {p.load_mw:.0f} MW  [{p.status}]")

    # Quick overlap check against the illustrative price peaks from epex_prices.py
    import epex_prices
    prices = epex_prices.get_illustrative_day(day)
    price_peak_times = {p.period_start for p in epex_prices.get_peak_troughs(prices, n=6)}
    overlap = overlap_with_price_peaks(profile, price_peak_times)
    print(f"\nOverlap with illustrative price peaks: "
          f"{overlap['n_overlapping']}/{overlap['n_price_peaks']} "
          f"({overlap['overlap_fraction']*100:.0f}%)")
    print("(This overlap fraction — not battery size — is the real ceiling "
          "on wholesale peak-shaving value. Low overlap = limited value "
          "regardless of how big the battery is.)")
