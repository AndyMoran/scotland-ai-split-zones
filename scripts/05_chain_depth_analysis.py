# scripts/05_chain_depth_analysis.py
"""
Stage 3 Prep: Event Chain Depth Analysis
Measures how often 3+ constraint events occur within rolling time windows,
to stress-test the 2-hour battery spec against multi-event chains.
"""
import polars as pl
import numpy as np
from pathlib import Path

print("=" * 80)
print("STAGE 3 PREP: EVENT CHAIN DEPTH ANALYSIS")
print("=" * 80)

# 1. Load event durations
parquet_path = Path("data/processed/03_constraint_event_durations.parquet")
events = pl.read_parquet(parquet_path).sort("start_time")

print(f"Total events loaded: {len(events)}")

# 2. Define the battery's discharge budget
BATTERY_USABLE_MWH = 85  # 95% - 10% of 100 MWh nameplate
HANDOFF_CAP_MWH = 50     # Max battery obligation per event (1hr × 50 MW)
P10_DISCHARGE_MWH = 25   # 0.5h × 50 MW

# 3. Simulate SoC depletion across consecutive event chains
# For each event, calculate: "How many subsequent events can the battery 
# survive before breaching the 10% SoC floor?"
print("\n" + "=" * 80)
print("CHAIN DEPTH SIMULATION (No Recharge, Handoff-Capped)")
print("=" * 80)

start_times = events["start_time"].to_list()
end_times = events["end_time"].to_list()
durations = events["duration_hours"].to_list()

chain_depths = []  # How many events the battery survives starting from each event

for i in range(len(events)):
    soc_remaining = BATTERY_USABLE_MWH  # Start full (95 MWh above 10% floor)
    depth = 0
    
    for j in range(i, len(events)):
        # Calculate discharge for this event (capped at handoff limit)
        if durations[j] <= 1.0:
            # Short event: battery covers entire duration
            discharge = 50 * durations[j]  # 50 MW × duration
        else:
            # Long event: battery only covers first 1 hour (handoff cap)
            discharge = HANDOFF_CAP_MWH
        
        soc_remaining -= discharge
        depth += 1
        
        if soc_remaining <= 0:
            break  # Battery breached
    
    chain_depths.append(depth)

chain_depths = np.array(chain_depths)

# 4. Report statistics
print(f"\nBattery survival depth (starting from each event, no recharge):")
print(f"  Mean chain depth: {np.mean(chain_depths):.1f} events")
print(f"  Median chain depth: {np.median(chain_depths):.1f} events")
print(f"  P10 chain depth: {np.percentile(chain_depths, 10):.0f} events")
print(f"  P25 chain depth: {np.percentile(chain_depths, 25):.0f} events")
print(f"  Min chain depth: {np.min(chain_depths)} events")

# 5. Specifically: Starting from P10 (0.5h) events only
p10_mask = np.array([d == 0.5 for d in durations])
p10_chain_depths = chain_depths[p10_mask]

print(f"\n🔥 CHAIN DEPTH STARTING FROM 0.5h (P10) EVENTS:")
print(f"  Total 0.5h starting events: {len(p10_chain_depths)}")
print(f"  Mean survival depth: {np.mean(p10_chain_depths):.1f} events")
print(f"  Median survival depth: {np.median(p10_chain_depths):.1f} events")
print(f"  % surviving 2+ events: {np.sum(p10_chain_depths >= 2) / len(p10_chain_depths) * 100:.1f}%")
print(f"  % surviving 3+ events: {np.sum(p10_chain_depths >= 3) / len(p10_chain_depths) * 100:.1f}%")
print(f"  % surviving 4+ events: {np.sum(p10_chain_depths >= 4) / len(p10_chain_depths) * 100:.1f}%")

# 6. Rolling window analysis: How many events fall within 2h / 4h windows?
print(f"\n{'=' * 80}")
print("ROLLING WINDOW EVENT DENSITY")
print("=" * 80)

window_2h_counts = []
window_4h_counts = []

for i in range(len(events)):
    t_start = start_times[i]
    count_2h = sum(1 for j in range(i, len(events)) 
                   if (start_times[j] - t_start).total_seconds() <= 7200)  # 2 hours
    count_4h = sum(1 for j in range(i, len(events)) 
                   if (start_times[j] - t_start).total_seconds() <= 14400)  # 4 hours
    window_2h_counts.append(count_2h)
    window_4h_counts.append(count_4h)

window_2h_counts = np.array(window_2h_counts)
window_4h_counts = np.array(window_4h_counts)

print(f"\nEvents within a 2-hour rolling window:")
print(f"  Mean: {np.mean(window_2h_counts):.1f}")
print(f"  Median: {np.median(window_2h_counts):.0f}")
print(f"  P90: {np.percentile(window_2h_counts, 90):.0f}")
print(f"  Max: {np.max(window_2h_counts)}")
print(f"  % of windows with 3+ events: {np.sum(window_2h_counts >= 3) / len(window_2h_counts) * 100:.1f}%")

print(f"\nEvents within a 4-hour rolling window:")
print(f"  Mean: {np.mean(window_4h_counts):.1f}")
print(f"  Median: {np.median(window_4h_counts):.0f}")
print(f"  P90: {np.percentile(window_4h_counts, 90):.0f}")
print(f"  Max: {np.max(window_4h_counts)}")
print(f"  % of windows with 3+ events: {np.sum(window_4h_counts >= 3) / len(window_4h_counts) * 100:.1f}%")
print(f"  % of windows with 4+ events: {np.sum(window_4h_counts >= 4) / len(window_4h_counts) * 100:.1f}%")

print(f"\n{'=' * 80}")
print("ANALYSIS COMPLETE")
print("=" * 80)