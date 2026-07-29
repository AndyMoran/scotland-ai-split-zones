# scripts/04_inter_event_gap_analysis.py
"""
Stage 3 Prep: Inter-Event Gap Analysis
Calculates the actual time gap between consecutive constraint events to 
empirically validate the "event stacking" hypothesis for battery sizing.
"""
import polars as pl
import numpy as np
from pathlib import Path

print("=" * 80)
print("STAGE 3 PREP: INTER-EVENT GAP ANALYSIS")
print("=" * 80)

# 1. Load the event durations dataset
parquet_path = Path("data/processed/03_constraint_event_durations.parquet")
if not parquet_path.exists():
    print("❌ ERROR: Event durations parquet file not found. Run script 03 first.")
    exit()

events = pl.read_parquet(parquet_path)

# 2. Sort chronologically by start time
events = events.sort("start_time")

# 3. Calculate the gap to the NEXT event
# Gap = Next event's start_time - Current event's end_time
events = events.with_columns([
    (pl.col("start_time").shift(-1) - pl.col("end_time")).dt.total_hours().alias("gap_to_next_event_hours")
])

# 4. Analyze ALL events first (baseline)
print("\n" + "=" * 80)
print("BASELINE: ALL 808 EVENTS")
print("=" * 80)
all_gaps = events["gap_to_next_event_hours"].drop_nulls().to_numpy()
print(f"Median gap between ANY two consecutive events: {np.median(all_gaps):.1f} hours")
print(f"Percentage of events followed by another event within 2 hours: {(np.sum(all_gaps <= 2.0) / len(all_gaps) * 100):.1f}%")
print(f"Percentage of events followed by another event within 4 hours: {(np.sum(all_gaps <= 4.0) / len(all_gaps) * 100):.1f}%")

# 5. Deep Dive: The P10 (0.5h) Events
print("\n" + "=" * 80)
print("DEEP DIVE: 0.5-HOUR (P10) EVENTS")
print("=" * 80)
p10_events = events.filter(pl.col("duration_hours") == 0.5)
print(f"Total 0.5h events: {len(p10_events)}")

p10_gaps = p10_events["gap_to_next_event_hours"].drop_nulls().to_numpy()

if len(p10_gaps) > 0:
    print(f"Median gap after a 0.5h event: {np.median(p10_gaps):.1f} hours")
    
    # Calculate conditional probabilities
    gap_1h = np.sum(p10_gaps <= 1.0) / len(p10_gaps) * 100
    gap_2h = np.sum(p10_gaps <= 2.0) / len(p10_gaps) * 100
    gap_4h = np.sum(p10_gaps <= 4.0) / len(p10_gaps) * 100
    
    print(f"\n🔥 EMPIRICAL STACKING METRICS:")
    print(f"   - {gap_1h:.1f}% of 0.5h events are followed by another event within 1 hour.")
    print(f"   - {gap_2h:.1f}% of 0.5h events are followed by another event within 2 hours.")
    print(f"   - {gap_4h:.1f}% of 0.5h events are followed by another event within 4 hours.")
    
    if gap_2h > 20:
        print("\n   💡 CONCLUSION: Event stacking is empirically significant. A 1-hour battery")
        print("      would frequently be caught depleted during a secondary event, validating")
        print("      the need for 2-hour duration to ensure grid reliability and merchant optionality.")
    else:
        print("\n   💡 CONCLUSION: Event stacking is rare. The 2-hour duration is primarily")
        print("      justified by merchant revenue stacking (arbitrage/balancing), not P10 recurrence.")
else:
    print("No 0.5h events found with a subsequent event.")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)