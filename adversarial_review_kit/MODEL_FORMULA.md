# Renewable Absorption Model: Explicit Formula

## Core Calculation
The model calculates renewable absorption as the minimum of three physical constraints:

```python
renewable_absorption_mw = min(
    schedulable_ai_load_mw,        # Demand-side ceiling
    available_curtailed_mw_proxy,  # Supply-side ceiling
    site_connection_capacity_mw    # Physical infrastructure limit
)

## 1. Schedulable AI Load (Demand-Side Ceiling)

schedulable_ai_load_mw = (
    AI_CAMPUS_LOAD_MW *           # Total campus power draw (500 MW)
    schedulable_fraction *         # % of workload that can be shifted (0.5)
    duration_compatibility_factor  # Timescale matching coefficient
)

Where:

duration_compatibility_factor = min(1.0, event_duration_h / notice_period_h)

**Interpretation:** If the grid event is shorter than the IT notice period, the compatibility factor scales down proportionally. A 2-hour event with 12-hour notice = 2/12 = 0.167 compatibility.

## 2. Available Curtailed Wind (Supply-Side Ceiling)    

available_curtailed_mw_proxy = site_capacity_mw * curtailment_availability_factor

Where curtailment_availability_factor = 0.5 (MVP heuristic based on NESO 2022 data showing ~50% of constraint events coincide with high wind generation in export zones).

3. Site Connection Capacity (Infrastructure Limit)

site_connection_capacity_mw = site_capacity_mw  # Physical wires limit

## Example Calculation: Timescale Mismatch Scenario

Inputs:

- AI Campus Load: 500 MW
- Schedulable Fraction: 50% (0.5)
- Notice Period: 12 hours
- Event Duration: 2 hours
- Site Capacity: 539 MW (Whitelee Wind Farm)
- Curtailment Factor: 0.5

Step 1: Duration Compatibility

duration_compatibility_factor = min(1.0, 2 / 12) = 0.167

Step 2: Schedulable AI Load

schedulable_ai_load_mw = 500 * 0.5 * 0.167 = 41.7 MW

Step 3: Available Curtailed Wind

available_curtailed_mw_proxy = 539 * 0.5 = 269.5 MW

Step 4: Actual Absorption

renewable_absorption_mw = min(41.7, 269.5, 539) = 41.7 MW

Result: The AI campus absorbs only 41.7 MW, not the 250 MW it could theoretically provide under perfect conditions. The timescale mismatch destroys 208.3 MW of potentially flexible load (83% of the schedulable portion).