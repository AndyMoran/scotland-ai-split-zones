# scripts/07_verify_data_dates.py
import polars as pl
from pathlib import Path

parquet_path = Path("data/processed/03_constraint_event_durations.parquet")
if parquet_path.exists():
    df = pl.read_parquet(parquet_path)
    print("=" * 80)
    print("PARQUET FILE DATE RANGE CHECK")
    print("=" * 80)
    print(f"Total events: {len(df)}")
    print(f"Min start_time: {df['start_time'].min()}")
    print(f"Max start_time: {df['start_time'].max()}")
    print(f"Min duration: {df['duration_hours'].min()}")
    print(f"Max duration: {df['duration_hours'].max()}")
else:
    print("❌ Parquet file not found.")