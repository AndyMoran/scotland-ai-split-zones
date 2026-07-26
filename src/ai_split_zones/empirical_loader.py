import polars as pl
from pathlib import Path

# Strict schemas (Manifesto Rule: Schema Before Analysis)
TARGET_SCHEMA = {
    "planning_reference": pl.Utf8,
    "site_name": pl.Utf8,
    "developer": pl.Utf8,
    "capacity_mw": pl.Float64,
    "latitude": pl.Float64,
    "longitude": pl.Float64,
    "planning_status": pl.Utf8,
}

def load_repd_projects(raw_path: Path) -> pl.DataFrame:
    """
    Loads the REPD renewable projects register.
    Fails loudly if physical boundaries are violated.
    """
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw REPD data not found at {raw_path}.")
        
    df = pl.read_csv(raw_path)
    
    # Normalize column names to handle variations in gov.uk exports
    # Only rename columns that actually exist to avoid ColumnNotFoundError
    rename_map = {
        "Capacity (MW)": "capacity_mw",
        "Capacity_MW": "capacity_mw",
        "Planning Reference": "planning_reference",
        "Site Name": "site_name",
        "Planning Status": "planning_status"
    }
    valid_rename_map = {k: v for k, v in rename_map.items() if k in df.columns}
    if valid_rename_map:
        df = df.rename(valid_rename_map)
    
    # 1. Check required columns
    required_cols = set(TARGET_SCHEMA.keys())
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise ValueError(f"REPD data missing required columns: {missing_cols}")
        
    # 2. Select and cast to strict schema
    df = df.select(list(required_cols)).cast(TARGET_SCHEMA)
    
    # 3. Assertions Protect Physics (Manifesto Rule 5)
    assert df["capacity_mw"].min() >= 0, "Physical violation: Site capacity cannot be negative."
    assert df["latitude"].is_between(-90, 90).all(), "Physical violation: Latitude out of bounds."
    assert df["longitude"].is_between(-180, 180).all(), "Physical violation: Longitude out of bounds."
    
    # 4. Filter to Scotland only (approximate bounding box for MVP)
    df = df.filter(
        (pl.col("latitude") > 54.5) & 
        (pl.col("longitude") < -1.5)
    )
    
    return df
