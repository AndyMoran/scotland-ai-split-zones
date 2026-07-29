# scripts/02b_corrected_volume_calculation.py
"""
CRITICAL FIX: Corrected Scottish Constraint Volume Calculation
The previous calculation likely summed ALL day-ahead forecast differentials,
not just actual constraint events. This script isolates constraint periods
where Flow > Limit and calculates only those volumes.
"""
import requests
import polars as pl
from pathlib import Path

API_URL = "https://api.neso.energy/api/3/action/datastore_search"
RESOURCE_ID = "38a18ec1-9e40-465d-93fb-301e80fd1352"  # Day Ahead Constraint Flows
TIMEOUT = (5, 10)

TARGET_BOUNDARIES = ["SCOTEX", "SSEN-S"]

def fetch_and_calculate_corrected_volume():
    """
    Fetch Day Ahead data and calculate ONLY the volume during actual constraint events
    (where Flow > Limit), not all forecast differentials.
    """
    print("=" * 80)
    print("CRITICAL FIX: Corrected Scottish Constraint Volume Calculation")
    print("=" * 80)
    
    # Fetch all data for target boundaries
    all_records = []
    offset = 0
    limit = 10000
    
    for boundary in TARGET_BOUNDARIES:
        print(f"\nFetching data for {boundary}...")
        
        while True:
            params = {
                "resource_id": RESOURCE_ID,
                "limit": limit,
                "offset": offset,
                "filters": f'{{"Constraint Group": "{boundary}"}}'
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
        
        print(f"\n  ✅ Fetched {len(all_records)} total rows for {boundary}")
    
    # Convert to DataFrame
    df = pl.DataFrame(all_records)
    
    print(f"\n{'=' * 80}")
    print("VOLUME CALCULATION")
    print(f"{'=' * 80}")
    print(f"Total rows fetched: {len(df):,}")
    
    # Parse and cast
    df = df.with_columns([
        pl.col("Date (GMT/BST)")
          .str.to_datetime(strict=False)
          .dt.replace_time_zone("Europe/London", ambiguous="earliest", non_existent="null")
          .dt.convert_time_zone("UTC")
          .alias("timestamp"),
        pl.col("Limit (MW)").cast(pl.Float64, strict=False),
        pl.col("Flow (MW)").cast(pl.Float64, strict=False),
    ]).filter(pl.col("timestamp").is_not_null())
    # 🔥 CRITICAL FIX: Filter STRICTLY to historical 2023 and 2024 data
    # This removes all future Day-Ahead forecast artifacts (2025-2026)
    df = df.filter(
        pl.col("timestamp").dt.year().is_in([2023, 2024])
    )
    print(f"  ✅ Filtered to 2023-2024 historical data: {len(df)} rows remaining.")
    print(f"Rows after timestamp parsing: {len(df):,}")
    
    # Calculate the differential for ALL rows (for comparison)
    df = df.with_columns([
        (pl.col("Flow (MW)") - pl.col("Limit (MW)")).alias("differential_mw"),
    ])
    
    # Calculate total differential (what we did before - likely wrong)
    total_differential_mwh = df.select(
        (pl.col("differential_mw").abs() * 0.5).sum()
    ).to_series()[0]
    
    print(f"\n❌ INCORRECT METHOD (summing all differentials):")
    print(f"   Total differential volume: {total_differential_mwh:,.0f} MWh")
    print(f"   This is {total_differential_mwh / 1_000_000:.2f} TWh")
    print(f"   (This is likely what produced the 22.8 TWh figure)")
    
    # CORRECT METHOD: Filter to ONLY constraint events (Flow > Limit)
    constraint_events = df.filter(pl.col("Flow (MW)") > pl.col("Limit (MW)"))
    
    print(f"\n✅ CORRECT METHOD (summing only constraint events):")
    print(f"   Total rows: {len(df):,}")
    print(f"   Constraint event rows (Flow > Limit): {len(constraint_events):,}")
    print(f"   Constraint event percentage: {len(constraint_events) / len(df) * 100:.2f}%")
    
    # Calculate volume ONLY during constraint events
    constraint_volume_mwh = constraint_events.select(
        ((pl.col("Flow (MW)") - pl.col("Limit (MW)")) * 0.5).sum()
    ).to_series()[0]
    
    print(f"\n   Corrected constraint volume: {constraint_volume_mwh:,.0f} MWh")
    print(f"   This is {constraint_volume_mwh / 1_000_000:.2f} TWh")
    
    # Sanity check
    print(f"\n{'=' * 80}")
    print("SANITY CHECK")
    print(f"{'=' * 80}")
    print(f"Scotland total wind generation: ~25-30 TWh/year")
    print(f"GB-wide constraint costs: ~£500M-£1B/year (NESO reports)")
    print(f"GB-wide curtailed volume: ~3-5 TWh/year (typical)")
    print(f"Scotland's share (2 boundaries): ~1-2 TWh/year (expected)")
    print(f"\nOur corrected figure: {constraint_volume_mwh / 1_000_000:.2f} TWh")
    
    if constraint_volume_mwh / 1_000_000 > 3.0:
        print(f"\n⚠️  WARNING: Figure still seems high. May need further investigation.")
    elif constraint_volume_mwh / 1_000_000 < 0.5:
        print(f"\n⚠️  WARNING: Figure seems low. May need further investigation.")
    else:
        print(f"\n✅ Figure appears reasonable and within expected range.")
    
    # Breakdown by boundary
    print(f"\n{'=' * 80}")
    print("BREAKDOWN BY BOUNDARY")
    print(f"{'=' * 80}")
    
    for boundary in TARGET_BOUNDARIES:
        boundary_events = constraint_events.filter(pl.col("Constraint Group") == boundary)
        boundary_volume = boundary_events.select(
            ((pl.col("Flow (MW)") - pl.col("Limit (MW)")) * 0.5).sum()
        ).to_series()[0]
        
        print(f"\n{boundary}:")
        print(f"  Constraint events: {len(boundary_events):,} half-hours")
        print(f"  Constraint volume: {boundary_volume:,.0f} MWh ({boundary_volume / 1_000_000:.2f} TWh)")
    
    # Save corrected data
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    constraint_events.write_parquet(output_dir / "02b_scottish_constraint_events_corrected.parquet")
    
    print(f"\n✅ Corrected constraint events saved to:")
    print(f"   {output_dir / '02b_scottish_constraint_events_corrected.parquet'}")
    
    return {
        "total_volume_mwh": constraint_volume_mwh,
        "scotex_volume_mwh": constraint_events.filter(pl.col("Constraint Group") == "SCOTEX").select(
            ((pl.col("Flow (MW)") - pl.col("Limit (MW)")) * 0.5).sum()
        ).to_series()[0],
        "ssen_volume_mwh": constraint_events.filter(pl.col("Constraint Group") == "SSEN-S").select(
            ((pl.col("Flow (MW)") - pl.col("Limit (MW)")) * 0.5).sum()
        ).to_series()[0],
    }

if __name__ == "__main__":
    results = fetch_and_calculate_corrected_volume()
    
    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print(f"{'=' * 80}")
    print(f"Total corrected volume: {results['total_volume_mwh']:,.0f} MWh")
    print(f"  SCOTEX: {results['scotex_volume_mwh']:,.0f} MWh")
    print(f"  SSEN-S: {results['ssen_volume_mwh']:,.0f} MWh")
    print(f"\nNext step: Recalculate £/MWh proxy using this corrected volume.")