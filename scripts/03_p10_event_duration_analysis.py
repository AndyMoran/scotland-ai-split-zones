# scripts/03_p10_event_duration_analysis.py
"""
Stage 3 Prep: P10 Event Duration Analysis (HISTORICAL 2023-2024 ONLY)
Identifies contiguous constraint events and calculates their durations to 
inform the co-located BESS sizing and handoff logic.
"""
import requests
import polars as pl
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

API_URL = "https://api.neso.energy/api/3/action/datastore_search"
RESOURCE_ID = "38a18ec1-9e40-465d-93fb-301e80fd1352"  # Day Ahead Constraint Flows
TIMEOUT = (5, 10)
TARGET_BOUNDARY = "SCOTEX"

print("=" * 80)
print("STAGE 3 PREP: P10 EVENT DURATION ANALYSIS (2023-2024 HISTORICAL ONLY)")
print("=" * 80)

# 1. Fetch Data
print(f"\nFetching half-hourly data for {TARGET_BOUNDARY}...")
all_records = []
offset = 0
limit = 10000

while True:
    params = {
        "resource_id": RESOURCE_ID,
        "limit": limit,
        "offset": offset,
        "filters": f'{{"Constraint Group": "{TARGET_BOUNDARY}"}}'
    }
    response = requests.get(API_URL, params=params, timeout=TIMEOUT)
    response.raise_for_status()
    data = response.json()
    
    if not data.get("success"):
        raise RuntimeError(f"API error: {data.get('error')}")
    
    records = data["result"]["records"]
    if not records:
        break
        
    all_records.extend(records)
    offset += limit
    
    total = data["result"].get("total", len(all_records))
    print(f"  Fetched {len(all_records)} of {total} rows", end='\r')
    
    if len(all_records) >= total:
        break

print(f"\n  ✅ Fetched {len(all_records)} total rows.")

# 2. Process and Parse
df = pl.DataFrame(all_records)

df = df.with_columns([
    pl.col("Date (GMT/BST)")
      .str.to_datetime(format="%Y-%m-%d %H:%M:%S", strict=False)
      .fill_null(pl.col("Date (GMT/BST)").str.to_datetime(format="%d/%m/%Y %H:%M", strict=False))
      .fill_null(pl.col("Date (GMT/BST)").str.to_datetime(format="%Y-%m-%dT%H:%M:%S", strict=False))
      .dt.replace_time_zone("Europe/London", ambiguous="earliest", non_existent="null")
      .dt.convert_time_zone("UTC")
      .alias("timestamp"),
    pl.col("Flow (MW)").cast(pl.Float64, strict=False),
    pl.col("Limit (MW)").cast(pl.Float64, strict=False),
])

# 🔥 CRITICAL FIX: Filter STRICTLY to historical 2023 and 2024 data
# This removes all future Day-Ahead forecast artifacts (2025-2026)
df = df.filter(
    pl.col("timestamp").dt.year().is_in([2023, 2024])
)

print(f"  ✅ Filtered to 2023-2024 historical data: {len(df)} rows remaining.")

df = df.filter(pl.col("timestamp").is_not_null()).sort("timestamp")

# 3. Identify Contiguous Constraint Events
df = df.with_columns([
    (pl.col("Flow (MW)") > pl.col("Limit (MW)")).alias("is_constrained")
])

df = df.with_columns([
    (pl.col("is_constrained") != pl.col("is_constrained").shift(1)).fill_null(True).alias("event_change")
])

df = df.with_columns([
    pl.col("event_change").cum_sum().alias("event_id")
])

# Filter to only constrained periods and calculate duration
constrained_df = df.filter(pl.col("is_constrained"))

event_durations = constrained_df.group_by("event_id").agg([
    pl.col("timestamp").min().alias("start_time"),
    pl.col("timestamp").max().alias("end_time"),
    (pl.len() * 0.5).alias("duration_hours")  # Each row is a half-hour
]).sort("duration_hours")

print(f"\n{'=' * 80}")
print("EVENT DURATION STATISTICS (2023-2024 HISTORICAL)")
print(f"{'=' * 80}")
print(f"Total distinct constraint events identified: {len(event_durations)}")

# Calculate percentiles
durations = event_durations["duration_hours"].to_numpy()
p10 = np.percentile(durations, 10)
p25 = np.percentile(durations, 25)
p50 = np.percentile(durations, 50)
p75 = np.percentile(durations, 75)
p90 = np.percentile(durations, 90)
p95 = np.percentile(durations, 95)

print(f"P10 Duration: {p10:.1f} hours")
print(f"P25 Duration: {p25:.1f} hours")
print(f"P50 (Median) Duration: {p50:.1f} hours")
print(f"P75 Duration: {p75:.1f} hours")
print(f"P90 Duration: {p90:.1f} hours")
print(f"P95 Duration: {p95:.1f} hours")

# 4. Deep Dive into the P10 Tail
print(f"\n{'=' * 80}")
print("P10 TAIL ANALYSIS (Events < 1.0 Hour)")
print(f"{'=' * 80}")
p10_events = event_durations.filter(pl.col("duration_hours") < 1.0)
print(f"Number of events < 1.0 hour: {len(p10_events)} ({len(p10_events)/len(event_durations)*100:.1f}% of total)")

if len(p10_events) > 0:
    p10_durations = p10_events["duration_hours"].to_numpy()
    print(f"  - Min duration in P10: {np.min(p10_durations):.1f} hours")
    print(f"  - Median duration in P10: {np.median(p10_durations):.1f} hours")
    print(f"  - Max duration in P10: {np.max(p10_durations):.1f} hours")

# 5. Generate Histogram
print(f"\n{'=' * 80}")
print("GENERATING HISTOGRAM")
print(f"{'=' * 80}")

fig, ax = plt.subplots(1, 1, figsize=(10, 6))
bins = np.arange(0.5, 12.5, 0.5)
counts, bins, patches = ax.hist(durations, bins=bins, edgecolor='black', color='#2E86AB', alpha=0.8)

ax.axvline(x=1.0, color='#F18F01', linestyle='--', linewidth=2, label='1.0h IT Handoff Target')
ax.axvline(x=2.0, color='#A23B72', linestyle='-.', linewidth=2, label='2.0h Battery Duration')

ax.set_xlabel('Event Duration (Hours)', fontsize=11)
ax.set_ylabel('Number of Events', fontsize=11)
ax.set_title(f'{TARGET_BOUNDARY} Constraint Event Duration (2023-2024 Historical)', fontsize=12, fontweight='bold')
ax.legend()

ax.text(p10, ax.get_ylim()[1]*0.9, f'P10\n({p10}h)', ha='center', va='bottom', fontsize=9, color='red')
ax.text(p50, ax.get_ylim()[1]*0.85, f'P50\n({p50}h)', ha='center', va='bottom', fontsize=9, color='black')
ax.text(p90, ax.get_ylim()[1]*0.8, f'P90\n({p90}h)', ha='center', va='bottom', fontsize=9, color='blue')

plt.tight_layout()
output_path = Path("figures/06_p10_event_duration_histogram.png")
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✅ Histogram saved to: {output_path}")

parquet_path = Path("data/processed/03_constraint_event_durations.parquet")
parquet_path.parent.mkdir(parents=True, exist_ok=True)
event_durations.write_parquet(parquet_path)
print(f"✅ Event durations saved to: {parquet_path}")