# scripts/02c_cost_proportion_volume_proxy.py
"""
CRITICAL FIX: Calculate defensible boundary constraint volume proxy.
Method: Allocate total GB thermal constraint volume proportionally based on 
boundary-specific thermal constraint costs.
"""
import requests
import polars as pl
from pathlib import Path
import datetime as dt

API_URL = "https://api.neso.energy/api/3/action/datastore_search"
TIMEOUT = (5, 10)

# Dataset 1: System-wide constraint breakdown (has volume)
BREAKDOWN_RESOURCE_ID = "24d067d8-1328-452a-9720-21cb691e491e" 

# Dataset 2: Boundary-specific costs
BOUNDARY_COST_RESOURCE_ID = "75c9c564-af38-4421-a461-a612a6921212" 

def fetch_data(resource_id: str, limit: int = 10000) -> pl.DataFrame:
    params = {"resource_id": resource_id, "limit": limit}
    resp = requests.get(API_URL, params=params, timeout=TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"API error: {data.get('error')}")
    return pl.DataFrame(data["result"]["records"])

print("=" * 80)
print("CALCULATING DEFENSIBLE CONSTRAINT VOLUME PROXY (FINAL)")
print("=" * 80)

# 1. Get system-wide totals
print("\n1. Fetching system-wide Constraint Breakdown (23-24)...")
breakdown_df = fetch_data(BREAKDOWN_RESOURCE_ID)

# FIX: Use str.to_date to avoid Polars deprecation warnings
breakdown_df = breakdown_df.with_columns(
    pl.col("Date").str.to_date(strict=False).alias("Date_parsed")
)

fy23_24_df = breakdown_df.filter(
    (pl.col("Date_parsed") >= dt.date(2023, 4, 1)) & 
    (pl.col("Date_parsed") <= dt.date(2024, 3, 31))
)

total_gb_thermal_cost = fy23_24_df.select(pl.col("Thermal constraints cost").cast(pl.Float64).sum()).to_series()[0]

# FIX: Use abs() to convert negative curtailed volume to positive physical volume
total_gb_thermal_volume = abs(fy23_24_df.select(pl.col("Thermal constraints volume").cast(pl.Float64).sum()).to_series()[0])

print(f"   Total GB Thermal Constraint Cost (23-24): £{total_gb_thermal_cost:,.0f}")
print(f"   Total GB Thermal Constraint Volume (23-24): {total_gb_thermal_volume:,.0f} MWh ({total_gb_thermal_volume/1_000_000:.2f} TWh)")

# 2. Get boundary-specific costs
print("\n2. Fetching boundary-specific Thermal Constraint Costs (23-24)...")
boundary_df = fetch_data(BOUNDARY_COST_RESOURCE_ID)
boundary_df = boundary_df.with_columns(pl.col("Daily Cost (GBP)").cast(pl.Float64))

# Include all major Scottish export boundaries present in the cost dataset
target_boundaries = ["SCOTEX", "SSE-SP", "SSHARN"]
scotland_cost_df = boundary_df.filter(pl.col("Constraint Group").is_in(target_boundaries))
total_scotland_thermal_cost = scotland_cost_df.select(pl.col("Daily Cost (GBP)").sum()).to_series()[0]

print(f"   Total Scottish Thermal Constraint Cost (SCOTEX + SSE-SP + SSHARN): £{total_scotland_thermal_cost:,.0f}")

# 3. Calculate proxy
print("\n3. Calculating Volume Proxy...")
scotland_cost_share = total_scotland_thermal_cost / total_gb_thermal_cost
estimated_scotland_thermal_volume = total_gb_thermal_volume * scotland_cost_share

print(f"   Scotland Cost Share: {scotland_cost_share:.1%}")
print(f"   Estimated Scottish Thermal Constraint Volume: {estimated_scotland_thermal_volume:,.0f} MWh ({estimated_scotland_thermal_volume/1_000_000:.2f} TWh)")

# 4. Calculate the new £/MWh proxy
print("\n" + "=" * 80)
print("NEW EMPIRICAL £/MWh PROXY (DEFENSIBLE)")
print("=" * 80)
gb_average_proxy = total_gb_thermal_cost / total_gb_thermal_volume
scotland_average_proxy = total_scotland_thermal_cost / estimated_scotland_thermal_volume

print(f"   GB System-Wide Average: £{gb_average_proxy:,.2f} / MWh")
print(f"   Scottish Boundary Average: £{scotland_average_proxy:,.2f} / MWh")
print(f"\n   Methodology: Total Outturn Cost / Total Outturn Curtailed Volume.")
print(f"   (Note: This is an average cost proxy. Marginal costs during specific events may vary.)")
print(f"\n   TOTAL SCOTTISH ADDRESSABLE MARKET: £{total_scotland_thermal_cost:,.0f} / year")