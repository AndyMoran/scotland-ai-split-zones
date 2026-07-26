import polars as pl
from pathlib import Path

print("="*70)
print("SCOTLAND AI SPLIT-ZONES: AUTOMATED STRESS TEST")
print("="*70)

# Load the intermediate data
DATA_INTERMEDIATE = Path("data/intermediate")
absorption_df = pl.read_parquet(DATA_INTERMEDIATE / "renewable_absorption.parquet")

# Filter to Whitelee Wind Farm (Export Constrained)
site_df = absorption_df.filter(pl.col("site_name") == "Whitelee Wind Farm")

print("\n--- STRESS TEST: The Timescale Mismatch Trap ---")
print("Testing a 500 MW AI campus (50% schedulable, 50% curtailment proxy)")
print("Comparing Perfect Match vs. Realistic Intraday Event\n")

# Scenario A: Perfect Match (4h notice, 4h event)
scenario_a = site_df.filter(
    (pl.col("schedulable_fraction") == 0.5) &
    (pl.col("notice_period_h") == 4) &
    (pl.col("event_duration_h") == 4)
)

if scenario_a.is_empty():
    print("ERROR: Scenario A data not found. Check filter conditions.")
else:
    abs_a = scenario_a["renewable_absorption_mw"].to_list()[0]
    schedulable_a = scenario_a["schedulable_ai_load_mw"].to_list()[0]

    # Scenario B: Timescale Mismatch (12h notice, 2h event)
    scenario_b = site_df.filter(
        (pl.col("schedulable_fraction") == 0.5) &
        (pl.col("notice_period_h") == 12) &
        (pl.col("event_duration_h") == 2)
    )

    if scenario_b.is_empty():
        print("ERROR: Scenario B data not found. Check filter conditions.")
    else:
        abs_b = scenario_b["renewable_absorption_mw"].to_list()[0]
        schedulable_b = scenario_b["schedulable_ai_load_mw"].to_list()[0]

        print(f"Scenario A (4h Notice / 4h Event):")
        print(f"  Schedulable AI Load: {schedulable_a:.1f} MW")
        print(f"  Actual Absorption:   {abs_a:.1f} MW")
        print(f"\nScenario B (12h Notice / 2h Event):")
        print(f"  Schedulable AI Load: {schedulable_b:.1f} MW")
        print(f"  Actual Absorption:   {abs_b:.1f} MW")
        print("-" * 70)

        # Calculate losses
        loss_from_flexible = schedulable_a - abs_b
        loss_pct_of_flexible = (loss_from_flexible / schedulable_a) * 100
        loss_pct_of_total = (loss_from_flexible / 500.0) * 100

        print(f"\nRESULT: Of the {schedulable_a:.0f} MW schedulable load:")
        print(f"  • {loss_from_flexible:.1f} MW fails to deliver due to timescale mismatch")
        print(f"  • This is {loss_pct_of_flexible:.1f}% of the *theoretically flexible* load")
        print(f"  • This is {loss_pct_of_total:.1f}% of the *total 500 MW campus* load")
        print(f"\nCLARIFICATION: The remaining 250 MW of the 500 MW campus was never")
        print(f"               flexible to begin with (inflexible baseline). The timescale")
        print(f"               mismatch specifically destroys the *claimed* flexibility,")
        print(f"               not the entire load.")
        print("="*70)