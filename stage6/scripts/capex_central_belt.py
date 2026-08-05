"""
capex_central_belt.py (CORRECTED)

Stage 6 — Capex sourcing and commitment-fee proportionality, corrected.

WHAT WAS WRONG WITH THE FIRST VERSION, STATED PLAINLY:
1. Site anchor was Asanti Livingston (5MW) — below BOTH the commitment fee's
   40MW threshold and the milestone framework's 10MW threshold. The fee
   doesn't apply to a 5MW site at all; the whole proportionality argument
   was solving a problem for a site that would never face the instrument
   being analysed.
2. Capex benchmark was international literature (Terrapin CG, QTS-style
   brownfield figures, $7-12M/MW) rather than Ofgem's own published GB
   queue data. Ofgem's consultation document (Tables 3 and 4) shows real
   UK capex-per-MW by project size band, sourced from NESO's mandatory
   information request and a DNO voluntary request — a strictly better
   source than international benchmarks for this exact question.

Both are corrected here. Neither correction was optional or cosmetic —
using the right site and the right data changes the conclusion, not just
the number. See ASSUMPTIONS_LEDGER and the bottom of this file.
"""

from dataclasses import dataclass


@dataclass
class CapexBenchmark:
    label: str
    mean_gbp_per_mw: float
    median_gbp_per_mw: float
    n_projects: int
    source: str
    evidence_status: str = "GROUNDED"


# Ofgem's own Table 4 (DNO Request for Information), by project size band.
# Source: Ofgem, "Curate – Demand Connections Reform" consultation,
# 29 July 2026, Chapter 4, Table 4.
# DNO data used (not NESO Table 3) because DataVita DV1 is a
# distribution-connected site (SP Distribution), matching the DNO dataset's
# connection type more closely than the NESO transmission-queue dataset.
OFGEM_DNO_CAPEX_BY_SIZE = {
    "Small (0-10MW)": CapexBenchmark(
        "Small (0-10MW)", 27_000_000, 9_545_455, 7,
        "Ofgem consultation, Table 4 (DNO RFI)"),
    "Medium (10-50MW)": CapexBenchmark(
        "Medium (10-50MW)", 13_541_800, 10_051_053, 8,
        "Ofgem consultation, Table 4 (DNO RFI)"),
    "Large (50-100MW)": CapexBenchmark(
        "Large (50-100MW)", 6_778_605, 6_877_222, 13,
        "Ofgem consultation, Table 4 (DNO RFI)"),
    "Extra Large (100-500MW)": CapexBenchmark(
        "Extra Large (100-500MW)", 6_869_376, 7_699_476, 22,
        "Ofgem consultation, Table 4 (DNO RFI)"),
}

# Ofgem's own economy-wide average, used to set the fee itself.
OFGEM_AVERAGE_CAPEX_GBP_MW = 9_500_000

# Ofgem's proposed commitment fee: 2.5%-7.5% of capex, £237,500-£712,500/MW.
# Applies only to projects >=40MW (para 5.1, 5.4 of the consultation).
FEE_LOW_GBP_MW = 237_500
FEE_HIGH_GBP_MW = 712_500
FEE_THRESHOLD_MW = 40.0


def commitment_fee_range(site_mw: float) -> dict:
    if site_mw < FEE_THRESHOLD_MW:
        return {
            "site_mw": site_mw,
            "in_scope": False,
            "note": (
                f"Site is below the {FEE_THRESHOLD_MW}MW threshold — the "
                f"commitment fee does not apply. Any proportionality "
                f"calculation for a sub-threshold site is analysing an "
                f"instrument that would never be levied."
            ),
        }
    return {
        "site_mw": site_mw,
        "in_scope": True,
        "fee_low_gbp": round(FEE_LOW_GBP_MW * site_mw, 0),
        "fee_high_gbp": round(FEE_HIGH_GBP_MW * site_mw, 0),
    }


def proportionality_check(site_mw: float, benchmark: CapexBenchmark) -> dict:
    """
    Checks the commitment fee against a real capex benchmark for a site of
    this size, using both the benchmark's mean and median (Ofgem's own
    Table 4 reports both, precisely because a small sample (n=8 for
    Medium) can be skewed by outliers — reporting only one figure would
    hide that uncertainty).
    """
    fee = commitment_fee_range(site_mw)
    if not fee["in_scope"]:
        return fee

    results = {}
    for stat_name, capex_per_mw in [("mean", benchmark.mean_gbp_per_mw),
                                     ("median", benchmark.median_gbp_per_mw)]:
        capex_total = capex_per_mw * site_mw
        results[f"capex_{stat_name}_total_gbp"] = round(capex_total, 0)
        results[f"fee_pct_of_capex_{stat_name}_low"] = round(fee["fee_low_gbp"] / capex_total * 100, 2)
        results[f"fee_pct_of_capex_{stat_name}_high"] = round(fee["fee_high_gbp"] / capex_total * 100, 2)

    return {
        "site_mw": site_mw,
        "benchmark": benchmark.label,
        "benchmark_source": benchmark.source,
        "benchmark_n_projects": benchmark.n_projects,
        "fee_range_gbp": (fee["fee_low_gbp"], fee["fee_high_gbp"]),
        **results,
        "ofgem_target_range_pct": (2.5, 7.5),
    }


# ─────────────────────────────────────────────────────────────────────────
# ASSUMPTIONS LEDGER (Stage 6, capex component — corrected)
# ─────────────────────────────────────────────────────────────────────────
ASSUMPTIONS_LEDGER = [
    ("Site anchor", "DataVita DV1, 40MW (expansion target) — real, verified, at the exact fee threshold",
     "GROUNDED — corrects the earlier Asanti Livingston (5MW) anchor, which was below the fee's own 40MW threshold"),
    ("Capex benchmark", "Ofgem's own Table 4 (DNO RFI), Medium 10-50MW band: mean £13.54M/MW, median £10.05M/MW, n=8",
     "GROUNDED — corrects the earlier international-literature benchmark ($7-12M/MW), which was the wrong data source for this specific question"),
    ("DNO vs NESO table choice", "Used DNO data (Table 4) since DV1 is distribution-connected",
     "PROVISIONAL — DV1's actual TEA status (whether it triggers Transmission Entry Assessment, which would put it under NESO's process instead) is not confirmed"),
    ("Small sample size (n=8, Medium band)", "Both mean and median reported, not just one",
     "DELIBERATE — Ofgem's own methodology (para 4.12) uses median specifically to manage outlier risk; a single figure would hide that this band's estimate is less stable than the Extra Large band's (n=22)"),
]


if __name__ == "__main__":
    print("Stage 6 — Corrected Commitment Fee Proportionality Check")
    print("=" * 78)
    print(f"\nSite: DataVita DV1, {FEE_THRESHOLD_MW}MW (expansion target, at the fee threshold)")

    benchmark = OFGEM_DNO_CAPEX_BY_SIZE["Medium (10-50MW)"]
    result = proportionality_check(FEE_THRESHOLD_MW, benchmark)

    print(f"\nBenchmark: {result['benchmark']} ({result['benchmark_source']}, n={result['benchmark_n_projects']})")
    print(f"Fee range: £{result['fee_range_gbp'][0]:,.0f} - £{result['fee_range_gbp'][1]:,.0f}")
    print(f"\nUsing MEDIAN capex (£{benchmark.median_gbp_per_mw:,}/MW):")
    print(f"  Fee as % of capex: {result['fee_pct_of_capex_median_low']}% - {result['fee_pct_of_capex_median_high']}%")
    print(f"\nUsing MEAN capex (£{benchmark.mean_gbp_per_mw:,}/MW):")
    print(f"  Fee as % of capex: {result['fee_pct_of_capex_mean_low']}% - {result['fee_pct_of_capex_mean_high']}%")
    print(f"\nOfgem's stated target range: {result['ofgem_target_range_pct'][0]}% - {result['ofgem_target_range_pct'][1]}%")

    print("\n" + "=" * 78)
    print("VERDICT: Both mean and median estimates fall within, or very close to,")
    print("Ofgem's own 2.5%-7.5% target range. The earlier finding — that the fee")
    print("overshoots its target for smaller/brownfield sites — does not survive")
    print("using the correct site anchor and Ofgem's own GB queue evidence.")
    print("=" * 78)

    print("\nAssumptions Ledger:")
    for assumption, detail, status in ASSUMPTIONS_LEDGER:
        print(f"\n  {assumption}:")
        print(f"    {detail}")
        print(f"    Status: {status}")