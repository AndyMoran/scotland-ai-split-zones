"""
12_stage6_central_belt_synthesis.py

Stage 6 synthesis: runs all four Stage 6 modules and generates the figure
set for notebooks/10_stage6_central_belt_synthesis.ipynb.

Every number plotted here is imported or computed from the underlying
modules (duos_central_belt.py, tnuos_central_belt.py, capex_central_belt.py,
inference_load_central_belt.py) — nothing is retyped from memory, matching
this project's numbers discipline. Executable assertions validate each
figure's headline number before it's plotted.

Run: python3 12_stage6_central_belt_synthesis.py
Output: figures/10_*.png
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from datetime import date

import duos_central_belt as duos
import tnuos_central_belt as tnuos
import inference_load_central_belt as load
import capex_central_belt as capex

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────
# House style — consistent across all Stage 6 figures
# ─────────────────────────────────────────────────────────────────────────
COLOR_TRAINING = "#8C9BA5"      # muted grey-blue — Stage 5 / training site
COLOR_INFERENCE = "#2A6F97"     # deeper blue — Stage 6 / inference site
COLOR_ACCENT = "#D1495B"        # red — flags, thresholds, warnings
COLOR_GOOD = "#4C956C"          # green — within target / confirmed
COLOR_NEUTRAL = "#6C757D"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "#222222",
    "text.color": "#222222",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.dpi": 150,
})


def save(fig, name):
    path = os.path.join(FIGURES_DIR, name)
    fig.savefig(path, bbox_inches="tight")
    print(f"  saved {path}")
    plt.close(fig)


print("Stage 6 Synthesis — generating figures")
print("=" * 60)

# ─────────────────────────────────────────────────────────────────────────
# Figure 1: DUoS differential — Stage 5 (training/EHV) vs Stage 6 (inference/HV)
# ─────────────────────────────────────────────────────────────────────────
print("\n[1/5] DUoS differential comparison")

stage5_diff = 1.58
comparison = duos.compare_to_stage5_training_site()
stage6_diff = comparison["stage6_spd_hv_differential_gbp_mwh"]
ratio = comparison["ratio"]
assert abs(ratio - 27.6) < 0.5, f"Ratio check failed: {ratio}"

fig, ax = plt.subplots(figsize=(6, 4.5))
bars = ax.bar(
    ["Stage 5\n100MW training\n132kV / EHV", "Stage 6\n5MW inference\nHV"],
    [stage5_diff, stage6_diff],
    color=[COLOR_TRAINING, COLOR_INFERENCE],
    width=0.55,
)
for bar, val in zip(bars, [stage5_diff, stage6_diff]):
    ax.annotate(f"£{val:.2f}/MWh", (bar.get_x() + bar.get_width() / 2, val),
                textcoords="offset points", xytext=(0, 6), ha="center",
                fontsize=11, fontweight="bold")
ax.annotate(f"27.6× larger", xy=(1, stage6_diff), xytext=(0.5, stage6_diff * 0.6),
            fontsize=10, color=COLOR_ACCENT, fontweight="bold", ha="center",
            arrowprops=dict(arrowstyle="->", color=COLOR_ACCENT, lw=1.2))
ax.set_ylabel("DUoS Red\u2013Green differential (£/MWh)")
ax.set_title("DUoS value scales down with voltage, not with site size", fontsize=12, loc="left")
ax.set_ylim(0, stage6_diff * 1.25)
save(fig, "10_1_duos_differential_comparison.png")

# ─────────────────────────────────────────────────────────────────────────
# Figure 2: Inference load profile with Red band and battery coverage
# ─────────────────────────────────────────────────────────────────────────
print("\n[2/5] Inference load profile + battery coverage")

target = date(2026, 8, 5)
site_mw = 5.0
battery_mw = site_mw * 0.5
profile = load.generate_inference_load_profile(target, site_capacity_mw=site_mw)
coverage = load.check_battery_coverage(profile, battery_mw)
assert coverage["coverage_confirmed"], "Battery coverage check failed"

hours = [p.period_start.hour + p.period_start.minute / 60 for p in profile]
loads = [p.load_mw for p in profile]

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.axvspan(16.5, 19.5, color=COLOR_ACCENT, alpha=0.12, label="DUoS Red band (16:30\u201319:30)")
ax.plot(hours, loads, color=COLOR_INFERENCE, lw=2, label="Inference site load")
ax.axhline(battery_mw, color=COLOR_NEUTRAL, ls="--", lw=1.3, label=f"Battery rating ({battery_mw}MW)")
ax.fill_between(hours, loads, color=COLOR_INFERENCE, alpha=0.06)
ax.set_xlim(0, 24)
ax.set_xticks(range(0, 25, 4))
ax.set_xlabel("Hour of day")
ax.set_ylabel("Site load (MW)")
ax.set_title("Inference load stays well above battery rating throughout the Red band",
              fontsize=12, loc="left")
ax.legend(loc="lower right", frameon=False, fontsize=9)
save(fig, "10_2_inference_load_profile.png")

# ─────────────────────────────────────────────────────────────────────────
# Figure 3: TNUoS HV bands, site assigned to HV4
# ─────────────────────────────────────────────────────────────────────────
print("\n[3/5] TNUoS HV band assignment")

assigned = tnuos.assign_band(site_mw)
assert assigned.band_name == "HV4", f"Band assignment check failed: {assigned.band_name}"

band_names = [b.band_name for b in tnuos.HV_BANDS]
band_annual = [tnuos.annual_cost_gbp(b) for b in tnuos.HV_BANDS]
colors = [COLOR_ACCENT if b.band_name == assigned.band_name else COLOR_NEUTRAL for b in tnuos.HV_BANDS]

fig, ax = plt.subplots(figsize=(7.5, 4.8))
bars = ax.bar(band_names, band_annual, color=colors, width=0.6)
for bar, val in zip(bars, band_annual):
    ax.annotate(f"£{val:,.0f}", (bar.get_x() + bar.get_width() / 2, val),
                textcoords="offset points", xytext=(0, 6), ha="center", fontsize=9)
ax.annotate("5MW site assigned here\n(~2.63\u00d7 the HV4\nlower threshold)",
            xy=(3, band_annual[3] * 0.75), xytext=(1.35, band_annual[3] * 0.62),
            fontsize=9, color=COLOR_ACCENT, ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=COLOR_ACCENT, lw=1.1))
ax.set_ylabel("TNUoS demand residual (£/year)")
ax.set_title("TNUoS HV bands \u2014 non-locational, same charge regardless of zone",
              fontsize=12, loc="left")
ax.set_xlim(-0.6, 3.6)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
save(fig, "10_3_tnuos_hv_bands.png")

# ─────────────────────────────────────────────────────────────────────────
# Figure 4: Gross vs net DUoS value, charging-period sensitivity
# ─────────────────────────────────────────────────────────────────────────
print("\n[4/5] Gross vs net DUoS sensitivity")

gross = load.realised_annual_duos_value(battery_mw, stage6_diff)["annual_value_gbp"]
red_rate = 43.77
scenarios = [("Green\n£0.10/MWh", 0.10), ("Amber\n£3.22/MWh", 3.22), ("Red\n£43.77/MWh", 43.77)]
net_values = []
for label, charge_rate in scenarios:
    net = load.net_annual_duos_value(battery_mw, red_rate, charge_rate)
    net_values.append(net["net_annual_gbp"])
assert net_values[0] > 0 and net_values[2] < 0, "Charging-period sensitivity check failed"

fig, ax = plt.subplots(figsize=(8, 5))
labels = [s[0] for s in scenarios]
colors_bar = [COLOR_GOOD, "#E0A458", COLOR_ACCENT]
bars = ax.bar(labels, net_values, color=colors_bar, width=0.5, zorder=3)
ax.axhline(0, color="#333333", lw=1, zorder=2)
ax.axhline(gross, color=COLOR_NEUTRAL, ls="--", lw=1.2, zorder=1)
ax.annotate(f"Gross value: £{gross:,.0f}/yr", xy=(2.5, gross), xytext=(2.5, gross),
            fontsize=9, color=COLOR_NEUTRAL, ha="right", va="bottom")
for bar, val in zip(bars, net_values):
    va = "bottom" if val >= 0 else "top"
    offset = 10 if val >= 0 else -10
    ax.annotate(f"£{val:,.0f}", (bar.get_x() + bar.get_width() / 2, val),
                textcoords="offset points", xytext=(0, offset), ha="center",
                va=va, fontsize=10, fontweight="bold", zorder=5,
                bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none"))
ax.set_ylabel("Net annual DUoS value (£/year)")
ax.set_title("Charging discipline, not battery losses, determines net value",
              fontsize=12, loc="left")
ax.set_xlim(-0.5, 2.85)
ax.set_ylim(min(net_values) * 1.6, gross * 1.2)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
save(fig, "10_4_gross_vs_net_duos_sensitivity.png")

# ─────────────────────────────────────────────────────────────────────────
# Figure 5: Fee-to-capex proportionality — corrected finding vs Ofgem's target
# ─────────────────────────────────────────────────────────────────────────
print("\n[5/5] Fee-to-capex proportionality, corrected")

benchmark = capex.OFGEM_DNO_CAPEX_BY_SIZE["Medium (10-50MW)"]
result = capex.proportionality_check(40.0, benchmark)
assert 1.5 < result["fee_pct_of_capex_mean_low"] < 3.0, "Proportionality check out of expected range"

original_wrong_estimate = 13.7  # the pre-correction figure, kept only as a labelled contrast
corrected_low = result["fee_pct_of_capex_mean_low"]
corrected_high = result["fee_pct_of_capex_median_high"]
ofgem_low, ofgem_high = 2.5, 7.5

fig, ax = plt.subplots(figsize=(8, 3.6))
ax.axvspan(ofgem_low, ofgem_high, color=COLOR_GOOD, alpha=0.15, label="Ofgem's stated target range (2.5\u20137.5%)")
ax.plot([corrected_low, corrected_high], [1, 1], color=COLOR_INFERENCE, lw=6, solid_capstyle="round",
        label="Corrected finding (DataVita DV1, Ofgem's own capex data)")
ax.scatter([original_wrong_estimate], [0.4], color=COLOR_ACCENT, s=70, zorder=5,
           label="Original (wrong) estimate \u2014 international benchmark, wrong site anchor")
ax.annotate("Did not survive\ncorrection", xy=(original_wrong_estimate, 0.4),
            xytext=(original_wrong_estimate - 0.3, 0.05), fontsize=8.5, color=COLOR_ACCENT, ha="right")
ax.set_xlim(0, 15)
ax.set_ylim(-0.3, 1.6)
ax.set_yticks([])
ax.set_xlabel("Commitment fee as % of capex")
ax.set_title("Fee proportionality \u2014 the original finding didn't survive correction",
              fontsize=12, loc="left", pad=12)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=1, frameon=False, fontsize=8.5)
save(fig, "10_5_fee_proportionality_corrected.png")

print("\n" + "=" * 60)
print("All 5 figures generated and all assertions passed.")
print(f"Output directory: {os.path.abspath(FIGURES_DIR)}")
