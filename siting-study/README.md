# The B4/B6 siting-mismatch study

**Where would additional flexible electricity demand in Scotland do the most to reduce renewable curtailment — and does the current AI/data-centre development pipeline overlap with those locations?**

Independent analysis by Andy Moran (Heaviside Analytics), working in a personal capacity. Not commissioned by, or written on behalf of, any developer, DNO, TO, or other stakeholder.

## The short version

Scotland generates more wind power than its grid can move south at some hours. When that happens, wind farms get paid to switch off ("curtailed") — a cost of roughly £350m/year, ultimately passed to consumers. AI data centres are one of the few loads big enough, and for some workloads flexible enough, to absorb that otherwise-wasted power *if* they're built in the right place.

They mostly aren't. Of 23 verified Scottish AI/data-centre projects, 91%+ of proposed capacity sits south of B4 — the transmission boundary into the most curtailed part of the grid — while the three most-curtailed wind assets in the country sit north of it. On its face, that looks like a mismatch.

It's more interesting than that once you check *why*.

## Two reversals, not one story

**First: for reused industrial/brownfield sites, the land itself mostly explains the pattern.** Scotland's derelict/vacant land is itself 85% concentrated south of B4 (checked against the Scottish Government's full 2025 site register, 3,091 sites). Land availability alone would predict something like an 81-87% southern pipeline — not far off the 91-96% actually observed. The residual gap is real but modest, and at the edge of what a 23-project sample can distinguish from noise.

**Second, and this only emerged in the latest pass: for ordinary farmland — where most of the pipeline actually sits — the opposite is true.** Checked against Scottish Government agricultural-census data, Scotland's total farmland is *majority north* of B4 (61%/39%), not south. The north's abundance is concentrated in lower-quality rough grazing rather than the crop-and-fallow land the pipeline's own farmland sites (Coldstream, Ochiltree, Duns, Auchtertool, and others) actually use — but under any reasonable reading, land availability explains *less* of the farmland-sited majority's southern concentration than it does for the brownfield-reuse minority, not more.

So the pipeline's overall southern concentration has two different explanations sitting underneath it: mostly-explained-by-land for the brownfield minority, and not-well-explained-by-land for the farmland majority. That's a genuinely more interesting finding than either "it's all just land availability" or "it's all curtailment blindness" — and it's the kind of thing that only shows up once you check both halves of the pipeline separately instead of treating "commercially plausible site" as one undifferentiated category.

## What else this checked

- **Connection feasibility**: SSEN Transmission's own connection registers show large flexible-demand connections (green hydrogen, battery storage) actively being sought and granted north of B4 — including at New Deer, the same substation one of the three most-curtailed wind farms connects at. The "no connection was available" explanation doesn't hold up.
- **Developer rationale**: five different developers, five different public siting rationales (economic-corridor branding, transmission-loss reduction, industrial-hub reuse, explicit renewables-proximity, and Apatura's own "north of B6" framing, which is trivially satisfied by any Scottish site) — none of them curtailment-specific, and all landing south of B4 regardless.
- **Whether the economics would even work**: NESO's own stated position is that high UK energy prices rule out most AI training here. That holds for ordinary grid power. A real government discount exists for exactly the curtailed-wind scenario (the AI Growth Zones scheme, up to £24/MWh for a 500MW Scottish site) — but it's modest, and NESO's own public forecasting documents don't yet appear to account for it. Behind-the-meter/private-wire supply is real and legal, but its main saving is on policy levies, not the transmission charges people assume it avoids, and it's reported as infeasible for offshore wind specifically — which rules it out for the exact three curtailed assets (Seagreen, Moray East, Moray West) anchoring this study's own headline numbers. If a genuine curtailment-arbitrage opportunity exists, it's narrower and more specific than "build in the north" — it's "build within 5-10km of a specific curtailed onshore wind, solar, or hydro asset," and nothing in the current pipeline appears to be doing that.

## Verdict

**Not confirmed, and not displaced.** The pipeline's southern concentration is real, well-evidenced, and only partly explained by land availability — more so for brownfield reuse, less so for farmland. Whether the unexplained residual reflects a genuine missed opportunity, or factors this analysis can't see (fibre, workforce, flatness, actual land-sale availability), remains open. See the study design doc for the full reasoning and the evidence log for every individual claim, its verdict, and its source.

## Relationship to the Constraint-Direction Framework (Stages 1–6)

This study does not test whether the Constraint-Direction Framework's siting logic is *wrong*. It tests whether the real-world pipeline is *following* it — a different question, with a different answer. Stages 1–6 model what optimal siting would be worth if a developer did it; this study checks whether developers actually have. The two are consistent, not in tension: Stage 5's own economics were already modest and contingent (an 8.6–18.7 year payback, resting partly on a TNUoS figure Stage 5's own ledger marks provisional), and finding that the real pipeline mostly sits away from the most-curtailed assets fits a market that hasn't found this an obvious trade — it isn't evidence the trade doesn't work.

Where this study does bear directly on Stages 1–6: it confirms flexible-demand connections north of B4 are genuinely available, not a theoretical construct (SSEN Transmission's own registers). It also clarifies that the "behind-the-meter" value Stage 5 models is network-charge optimisation for a site that stays grid-connected — not a literal private wire to one turbine, which this study separately finds reported as infeasible for offshore wind specifically. Full reasoning in the evidence log.

## What's in this folder

- **`b4-b6-siting-mismatch-study-design.md`** — the full study: hypothesis, methodology, all three evidence tiers, the complete 23-project pipeline table, and the current verdict.
- **`evidence-log.md`** — the audit trail. Every checkable claim this work has made, one row each: what was claimed, what was found, the source, and an honest verdict (confirmed / refuted / unverified / etc.). Includes several claims this analysis got wrong on first pass and corrected on re-check — logged rather than quietly fixed.
- **`btm-training-gap-note-for-split-zones.md`** — a focused note on behind-the-meter/private-wire supply mechanics, written for this repo's own Constraint-Direction Siting framework specifically.
- **`data/`** — the raw supporting data behind the land-availability and connection-feasibility claims (SSEN Transmission registers, the Scottish Vacant and Derelict Land Survey 2025 register), so the findings can be checked directly rather than taken on citation alone. See `data/SOURCES.md` for licensing and attribution.

## Methodology discipline

Every figure here traces to a primary source or a logged verification — not a half-remembered summary of one. Mean and median are never used interchangeably. Small samples are flagged, not extrapolated from. Claims are checked with the same rigour regardless of whether they came from an external source, a collaborator's suggestion, or this analysis's own earlier reasoning within the same working session — several genuine self-corrections are logged in the evidence log rather than silently revised.

## Licence

Analysis and text: CC BY 4.0. Any code released alongside this (data-processing scripts) is MIT-licensed. Please attribute Heaviside Analytics / Andy Moran if reusing.

## Get in touch

This is independent, ongoing work. Corrections, pushback, and better data are genuinely welcome — particularly on the open items listed at the end of the study design doc.
