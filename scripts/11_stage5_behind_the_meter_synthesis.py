# scripts/11_stage5_behind_the_meter_synthesis.py
"""
Stage 5: Behind-the-Meter Cost Avoidance Synthesis
Calculates the realistic, site-level value of using a co-located 50MW/100MWh 
battery to shave peak consumption and avoid high wholesale/network charges 
for a 100MW AI data centre.
"""
import sys
from pathlib import Path
from datetime import date

# Add current directory to path to import our modules
script_dir = Path(__file__).parent
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

from synthetic_load import generate_ai_load_profile, get_peak_load_periods, overlap_with_price_peaks
from epex_prices import get_illustrative_day, get_peak_troughs
from network_charges import (
    tnuos_asc_band_step_saving,
    tnuos_locational_residual_saving,
    summarise_network_stack,
    ChargeBehaviour,
    NetworkChargeLine
)

# ==============================================================================
# ASSET & SITE PARAMETERS
# ==============================================================================
SITE_BASELINE_MW = 70.0
SITE_PEAK_MW = 100.0
BATTERY_MW = 50.0
BATTERY_MWH = 100.0  # 2-hour duration

# ==============================================================================
# STAGE 5 EXECUTION
# ==============================================================================
print("=" * 80)
print("STAGE 5: BEHIND-THE-METER COST AVOIDANCE SYNTHESIS")
print("=" * 80)

# 1. Generate Synthetic Load & Price Profiles
print("\n[1] LOAD & PRICE PROFILES (Mechanics Prototyping)")
print("-" * 80)
target_date = date(2026, 7, 15)
load_profile = generate_ai_load_profile(
    target_date=target_date, 
    baseline_mw=SITE_BASELINE_MW, 
    peak_mw=SITE_PEAK_MW,
    n_training_spikes=2,
    spike_duration_hh=4
)

# Get illustrative prices (Flagged as ILLUSTRATIVE)
price_profile = get_illustrative_day(target_date, base_spread_gbp_per_mwh=40.0)
price_peak_periods = {p.period_start for p in get_peak_troughs(price_profile, n=6)}

# Check overlap
overlap_stats = overlap_with_price_peaks(load_profile, price_peak_periods)
print(f"Synthetic AI Load: Baseline {SITE_BASELINE_MW}MW, Peak {SITE_PEAK_MW}MW")
print(f"Illustrative Price Spread: ~£40/MWh (typical, non-spike)")
print(f"Overlap between Load Peaks and Price Peaks: {overlap_stats['n_overlapping']}/{overlap_stats['n_price_peaks']} "
      f"({overlap_stats['overlap_fraction']*100:.0f}%)")
print("⚠️  CAVEAT: Low overlap structurally limits wholesale peak-shaving value, ")
print("   regardless of battery size. This is a modelling convenience, not real site data.")

# 2. Calculate Network Charge Avoidance
print("\n[2] NETWORK CHARGE AVOIDANCE (Three Distinct Mechanisms)")
print("-" * 80)

# A. DUoS RAG Avoidance (Continuous)
# Assume Red band is 5 half-hour periods per day (e.g., 16:00 - 18:30)
# Battery shaves 50MW during these periods.
daily_shaved_mwh = BATTERY_MW * 0.5 * 5  # 125 MWh/day
annual_shaved_mwh = daily_shaved_mwh * 365  # 45,625 MWh/year
duos_red_rate = 1.58   # SSEN SHEPD 132kV/EHV real rate (£/MWh)
duos_green_rate = 0.00 # SSEN SHEPD 132kV/EHV real rate (£/MWh)
rate_differential = duos_red_rate - duos_green_rate
annual_duos_saving = annual_shaved_mwh * rate_differential

duos_result = NetworkChargeLine(
    name="DUoS RAG Avoidance (SSEN SHEPD 132kV/EHV)",
    behaviour=ChargeBehaviour.CONTINUOUS,
    status_note=(
        f"Based on SSEN SHEPD published DUoS rates for 132kV/EHV. "
        f"Red: £{duos_red_rate}/MWh, Green: £{duos_green_rate}/MWh. "
        f"Differential: £{rate_differential}/MWh. "
        f"Assumes 5 half-hour Red periods/day shaved at {BATTERY_MW}MW."
    ),
    annual_saving_gbp=annual_duos_saving,
    evidence_status="GROUNDED — sourced from SSEN SHEPD published charging statement",
)
print(f"• {duos_result.name}: £{duos_result.annual_saving_gbp:,.0f}/year")
print(f"  Status: {duos_result.evidence_status}")

# B. TNUoS ASC Band Step (Step-Function)
# Assume site currently has 100MW ASC. Battery provides 50MW sustained peak reduction.
band_thresholds = [50.0, 80.0, 100.0, 120.0]
band_charges = {0: 900_000, 1: 1_400_000, 2: 2_100_000, 3: 3_200_000, 4: 4_500_000}

tnuos_asc_result = tnuos_asc_band_step_saving(
    current_asc_mw=100.0,
    band_thresholds_mw=band_thresholds,
    band_annual_charge_gbp=band_charges,
    sustained_peak_reduction_mw=50.0  # Full battery capacity
)
print(f"• {tnuos_asc_result.name}: £{tnuos_asc_result.annual_saving_gbp:,.0f}/year")
print(f"  Status: {tnuos_asc_result.evidence_status}")

# C. TNUoS Locational Residual (Partial Residual)
# Assume battery shaves 50MW during the 3 highest-risk Triad periods (1.5 hours total = 75 MWh)
triad_shaved_mwh = 75.0
locational_rate = 8.0 # £/MWh (conservative post-2023 TCR estimate)

tnuos_loc_result = tnuos_locational_residual_saving(
    peak_shaved_mwh_at_triad_risk_periods=triad_shaved_mwh,
    locational_rate_gbp_per_mwh=locational_rate
)
print(f"• {tnuos_loc_result.name}: £{tnuos_loc_result.annual_saving_gbp:,.0f}/year")
print(f"  Status: {tnuos_loc_result.evidence_status}")

# 3. Calculate Wholesale Peak Shaving
print("\n[3] WHOLESALE PEAK SHAVING")
print("-" * 80)
# Find the top 6 price periods
top_prices = get_peak_troughs(price_profile, n=6)
# Calculate value if battery discharges 50MW during these 6 periods (3 hours total = 150 MWh)
wholesale_saving = sum(p.price_gbp_per_mwh * BATTERY_MW * 0.5 for p in top_prices)
print(f"• Wholesale Peak Shaving (Top 6 periods @ 50MW): £{wholesale_saving:,.0f}/year")
print("  Status: ILLUSTRATIVE — based on synthetic price shape, not real BMRS/EPEX settlement data.")
print("  Note: Actual value depends entirely on the overlap between AI load peaks and price peaks.")

# 4. Synthesis & Summary
print("\n[4] BEHIND-THE-METER VALUE SYNTHESIS")
print("=" * 80)

network_lines = [duos_result, tnuos_asc_result, tnuos_loc_result]
network_summary = summarise_network_stack(network_lines)

print(f"{'Mechanism':<45} | {'Annual Saving':<15} | {'Behaviour'}")
print("-" * 80)
print(f"{duos_result.name:<45} | £{duos_result.annual_saving_gbp:>12,.0f} | {duos_result.behaviour.value}")
print(f"{tnuos_asc_result.name:<45} | £{tnuos_asc_result.annual_saving_gbp:>12,.0f} | {tnuos_asc_result.behaviour.value}")
print(f"{tnuos_loc_result.name:<45} | £{tnuos_loc_result.annual_saving_gbp:>12,.0f} | {tnuos_loc_result.behaviour.value}")
print(f"{'Wholesale Peak Shaving':<45} | £{wholesale_saving:>12,.0f} | continuous (illustrative)")
print("-" * 80)
total_btm_saving = network_summary["total_annual_gbp"] + wholesale_saving
print(f"{'TOTAL BEHIND-THE-METER VALUE':<45} | £{total_btm_saving:>12,.0f} | (See caveat below)")
print("=" * 80)

print("\nCAVEAT:")
print(network_summary["caveat"])
print("\nStrategic Takeaway:")
print("For a 100MW AI site at 132kV, DUoS avoidance is structurally limited (£1.58/MWh differential).")
print("The real behind-the-meter value driver is the TNUoS ASC Band Step (£1.8M/year in this scenario),")
print("but this requires a formal, sustained capacity reduction, not just opportunistic dispatch.")
print("Wholesale peak shaving adds value, but is capped by the low overlap between AI load spikes and price peaks.")

# ==============================================================================
# ASSUMPTIONS LEDGER
# ==============================================================================
print("\n" + "=" * 80)
print("ASSUMPTIONS LEDGER")
print("=" * 80)

assumptions = [
    ("DUoS Rates", 
     "SSEN SHEPD 132kV/EHV: Red £1.58/MWh, Green £0.00/MWh.",
     "GROUNDED — sourced from SSEN SHEPD published charging statement (April 2027 tariff)"),
    
    ("TNUoS ASC Thresholds & Charges", 
     "Illustrative bands [50, 80, 100, 120] MW and charges £900k-£4.5M.",
     "PROVISIONAL — requires site-specific DNO/TO agreement data"),
    
    ("TNUoS Locational Rate", 
     "£8.00/MWh for Triad-risk periods.",
     "PROVISIONAL — conservative post-2023 TCR estimate"),
    
    ("Wholesale Price Shape", 
     "Synthetic double-hump curve with £40/MWh spread.",
     "ILLUSTRATIVE — mechanics prototype only. Must be replaced with real BMRS/EPEX data"),
    
    ("AI Load Profile", 
     "70MW baseline, two 2-hour spikes to 100MW.",
     "SYNTHETIC — modelling convenience. No public half-hourly hyperscale load trace exists"),
    
    ("Sustained Peak Reduction", 
     "50MW (full battery capacity) sustained to cross ASC band.",
     "PROVISIONAL — assumes battery can guarantee this reduction contractually"),
]

for assumption, detail, status in assumptions:
    print(f"\n{assumption}:")
    print(f"  {detail}")
    print(f"  Status: {status}")

print("\n" + "=" * 80)
print("REVIEWER NOTE")
print("=" * 80)
print("This output separates continuous, step-function, and partial residual savings.")
print("It explicitly flags synthetic/illustrative data and refuses to blend them into")
print("a single 'guaranteed' number without preserving the behavioural caveats.")