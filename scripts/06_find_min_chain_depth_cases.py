# scripts/06_find_min_chain_depth_cases.py
"""
Find the specific events where chain depth = 1 (the actual worst case)
"""
import polars as pl
import numpy as np
from pathlib import Path

print("=" * 80)
print("FINDING MIN CHAIN DEPTH CASES (Chain Depth = 1)")
print("=" * 80)

# Load event durations
parquet_path = Path("data/processed/03_constraint_event_durations.parquet")
events = pl.read_parquet(parquet_path).sort("start_time")

# Constants
BATTERY_USABLE_MWH = 85
HANDOFF_CAP_MWH = 50

# Recalculate chain depths
start_times = events["start_time"].to_list()
end_times = events["end_time"].to_list()
durations = events["duration_hours"].to_list()

chain_depths = []
for i in range(len(events)):
    soc_remaining = BATTERY_USABLE_MWH
    depth = 0
    for j in range(i, len(events)):
        if durations[j] <= 1.0:
            discharge = 50 * durations[j]
        else:
            discharge = HANDOFF_CAP_MWH
        soc_remaining -= discharge
        depth += 1
        if soc_remaining <= 0:
            break
    chain_depths.append(depth)

# Find all cases where chain depth = 1
min_depth_indices = [i for i, d in enumerate(chain_depths) if d == 1]

print(f"\nTotal cases with chain depth = 1: {len(min_depth_indices)}")

if len(min_depth_indices) > 0:
    print("\n" + "=" * 80)
    print("WORST-CASE EVENT DETAILS")
    print("=" * 80)
    
    for idx in min_depth_indices[:5]:  # Show first 5 cases
        event = events.row(idx, named=True)
        print(f"\nCase {min_depth_indices.index(idx) + 1}:")
        print(f"  Event start: {event['start_time']}")
        print(f"  Event end: {event['end_time']}")
        print(f"  Duration: {event['duration_hours']:.1f} hours")
        print(f"  Discharge (handoff-capped): {min(HANDOFF_CAP_MWH, 50 * event['duration_hours']):.0f} MWh")
        print(f"  Remaining SoC after this event: {BATTERY_USABLE_MWH - min(HANDOFF_CAP_MWH, 50 * event['duration_hours']):.0f} MWh")
        
        # Show the next event that tips it over
        if idx + 1 < len(events):
            next_event = events.row(idx + 1, named=True)
            gap_hours = (next_event['start_time'] - event['end_time']).total_seconds() / 3600
            print(f"\n  Next event:")
            print(f"    Start: {next_event['start_time']}")
            print(f"    Gap from previous event end: {gap_hours:.1f} hours")
            print(f"    Duration: {next_event['duration_hours']:.1f} hours")
            print(f"    Discharge: {min(HANDOFF_CAP_MWH, 50 * next_event['duration_hours']):.0f} MWh")
            print(f"    This tips the battery over the edge (SoC would go negative)")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)