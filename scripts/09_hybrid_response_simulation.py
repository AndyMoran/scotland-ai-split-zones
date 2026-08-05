# scripts/09_hybrid_response_simulation.py (CORRECTED)
"""
Stage 3: Hybrid AI-Battery Response Simulation
Quantifies the marginal value of co-located BESS for capturing P10 events
that AI alone cannot handle due to timescale mismatch.
"""
import polars as pl
import numpy as np
from pathlib import Path

# Constants from verified data
COST_PROXY_GBP_PER_MWH = 164.89
AI_SITE_MW = 100  # 100 MW AI training hub
BATTERY_MW = 50   # 50 MW battery power rating
BATTERY_MWH = 100 # 100 MWh battery energy capacity
IT_HANDOFF_HOURS = 1.0  # Battery covers first 1h while AI checkpoints
ROUND_TRIP_EFFICIENCY = 0.85  # 85% AC-AC efficiency

# Battery SoC constraints
MIN_SOC = 0.10  # 10% minimum
MAX_SOC = 0.95  # 95% maximum
USABLE_MWH = BATTERY_MWH * (MAX_SOC - MIN_SOC)  # 85 MWh usable

print("=" * 80)
print("STAGE 3: HYBRID AI-BATTERY RESPONSE SIMULATION (CORRECTED)")
print("=" * 80)

# 1. Load verified historical events
parquet_path = Path("data/processed/03_constraint_event_durations.parquet")
events = pl.read_parquet(parquet_path).sort("start_time")
print(f"\n✅ Loaded {len(events)} verified historical constraint events.")

# 2. Simulate AI-only response
print("\n" + "=" * 80)
print("SCENARIO 1: AI-ONLY RESPONSE")
print("=" * 80)

ai_only_captured_mwh = 0.0
ai_only_events_handled = 0

for row in events.iter_rows(named=True):
    duration = row["duration_hours"]
    
    if duration >= IT_HANDOFF_HOURS:
        # AI can respond: captures (duration - 1h) at 100 MW
        captured = (duration - IT_HANDOFF_HOURS) * AI_SITE_MW
        ai_only_captured_mwh += captured
        ai_only_events_handled += 1
    else:
        # AI cannot respond (timescale mismatch): 0 MWh captured
        pass

print(f"Events handled by AI-only: {ai_only_events_handled} / {len(events)}")
print(f"Total MWh captured by AI-only: {ai_only_captured_mwh:,.0f} MWh")
print(f"Annualized (over 2 years): {ai_only_captured_mwh / 2:,.0f} MWh/year")
print(f"Annualized value at £{COST_PROXY_GBP_PER_MWH}/MWh: £{ai_only_captured_mwh / 2 * COST_PROXY_GBP_PER_MWH / 1e6:.1f}M/year")

# 3. Simulate AI + BESS response
print("\n" + "=" * 80)
print("SCENARIO 2: AI + 50MW/100MWh BESS RESPONSE")
print("=" * 80)

hybrid_captured_mwh = 0.0
hybrid_events_handled = 0
battery_discharged_mwh = 0.0
battery_recharged_mwh = 0.0  # AC-side energy consumed for charging

# Track battery SoC (start at 95%)
soc_mwh = BATTERY_MWH * MAX_SOC  # 95 MWh

# Track marginal capture by event type
p10_marginal_mwh = 0.0
handoff_marginal_mwh = 0.0

for i, row in enumerate(events.iter_rows(named=True)):
    duration = row["duration_hours"]
    start_time = row["start_time"]
    
    # Calculate recharge since last event (if any)
    if i > 0:
        prev_end_time = events.row(i - 1, named=True)["end_time"]
        gap_hours = (start_time - prev_end_time).total_seconds() / 3600
        
        # Recharge at 50 MW during the gap (up to max SoC)
        # Account for round-trip efficiency: need more AC energy to charge
        recharge_potential_dc = min(gap_hours * BATTERY_MW, (BATTERY_MWH * MAX_SOC) - soc_mwh)
        recharge_potential_ac = recharge_potential_dc / ROUND_TRIP_EFFICIENCY  # AC-side energy consumed
        
        soc_mwh += recharge_potential_dc
        battery_recharged_mwh += recharge_potential_ac  # Track AC-side energy
    
    # Calculate discharge for this event
    if duration < IT_HANDOFF_HOURS:
        # Short event: battery handles entire duration (the P10 win!)
        discharge_needed = duration * BATTERY_MW
    else:
        # Long event: battery covers first 1h (handoff cap)
        discharge_needed = IT_HANDOFF_HOURS * BATTERY_MW  # 50 MWh
    
    # Check if battery has enough capacity
    min_soc_mwh = BATTERY_MWH * MIN_SOC  # 10 MWh
    available_mwh = soc_mwh - min_soc_mwh
    
    if available_mwh >= discharge_needed:
        # Battery can handle it
        soc_mwh -= discharge_needed
        battery_discharged_mwh += discharge_needed
        
        # Calculate total captured (battery + AI)
        if duration < IT_HANDOFF_HOURS:
            # Battery handled entire event at 50 MW
            captured = duration * BATTERY_MW
            p10_marginal_mwh += captured  # This is purely battery-enabled
        else:
            # Battery handled first 1h (50 MWh), AI handled rest (100 MW)
            captured = (IT_HANDOFF_HOURS * BATTERY_MW) + ((duration - IT_HANDOFF_HOURS) * AI_SITE_MW)
            handoff_marginal_mwh += IT_HANDOFF_HOURS * BATTERY_MW  # 50 MWh handoff coverage
        
        hybrid_captured_mwh += captured
        hybrid_events_handled += 1
    else:
        # Battery cannot handle it (insufficient SoC)
        # AI still handles it if duration >= 1h
        if duration >= IT_HANDOFF_HOURS:
            captured = (duration - IT_HANDOFF_HOURS) * AI_SITE_MW
            hybrid_captured_mwh += captured
            hybrid_events_handled += 1

print(f"Events handled by hybrid system: {hybrid_events_handled} / {len(events)}")
print(f"Total MWh captured by hybrid: {hybrid_captured_mwh:,.0f} MWh")
print(f"Annualized (over 2 years): {hybrid_captured_mwh / 2:,.0f} MWh/year")
print(f"Annualized value at £{COST_PROXY_GBP_PER_MWH}/MWh: £{hybrid_captured_mwh / 2 * COST_PROXY_GBP_PER_MWH / 1e6:.1f}M/year")

# 4. Calculate marginal value (with breakdown)
print("\n" + "=" * 80)
print("MARGINAL VALUE OF BATTERY (BREAKDOWN)")
print("=" * 80)

marginal_mwh = hybrid_captured_mwh - ai_only_captured_mwh
marginal_value_gbp = marginal_mwh * COST_PROXY_GBP_PER_MWH

print(f"Total marginal MWh: {marginal_mwh:,.0f} MWh")
print(f"  - P10 events (<1h, battery-enabled): {p10_marginal_mwh:,.0f} MWh")
print(f"  - Handoff coverage (≥1h events): {handoff_marginal_mwh:,.0f} MWh")
print(f"Annualized marginal MWh: {marginal_mwh / 2:,.0f} MWh/year")
print(f"Annualized marginal value: £{marginal_value_gbp / 2 / 1e6:.2f}M/year")

# 5. Battery utilization stats (with RTE correction)
print("\n" + "=" * 80)
print("BATTERY UTILIZATION STATS (WITH ROUND-TRIP EFFICIENCY)")
print("=" * 80)
print(f"Total discharged (DC-side): {battery_discharged_mwh:,.0f} MWh")
print(f"Total recharged (AC-side): {battery_recharged_mwh:,.0f} MWh")
print(f"Round-trip efficiency: {ROUND_TRIP_EFFICIENCY*100:.0f}%")
print(f"Energy lost to heat: {battery_recharged_mwh - battery_discharged_mwh:,.0f} MWh")
print(f"Annual throughput (DC-side): {battery_discharged_mwh / 2:,.0f} MWh/year")

# 6. Simple breakeven analysis
print("\n" + "=" * 80)
print("SIMPLE BREAKEVEN ANALYSIS")
print("=" * 80)

# Battery CAPEX (from YAML: £250k/MWh × 100 MWh = £25M)
BATTERY_CAPEX_GBP = 250_000 * BATTERY_MWH
annual_marginal_value = marginal_value_gbp / 2

# Simple payback (no discounting, no O&M)
simple_payback_years = BATTERY_CAPEX_GBP / annual_marginal_value if annual_marginal_value > 0 else float('inf')

print(f"Battery CAPEX: £{BATTERY_CAPEX_GBP / 1e6:.1f}M")
print(f"Annual marginal value (constraint capture only): £{annual_marginal_value / 1e6:.2f}M/year")
print(f"Simple payback period: {simple_payback_years:.1f} years")

if simple_payback_years > 15:
    print("\n⚠️  VERDICT: Battery does NOT breakeven on constraint value alone.")
    print("   The battery must rely on merchant revenue stacking (arbitrage, balancing services)")
    print("   to be investable. This validates the 2-hour duration spec for multi-revenue optionality.")
else:
    print(f"\n✅ VERDICT: Battery breakevens in {simple_payback_years:.1f} years on constraint value alone.")

print("\n" + "=" * 80)
print("SIMULATION COMPLETE")
print("=" * 80)