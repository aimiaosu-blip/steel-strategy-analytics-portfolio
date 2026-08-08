# BI Handoff

Import `data/processed/monthly_market_bi.csv`, `scenario_outlook_bi.csv`, and `data/raw/competitor_profiles_public.csv`. Recommended relationships: scenario to scenario/year outlook; calendar month to monthly market. Build cards for latest HRC, blended cash cost and margin; a weekly/monthly trend; scenario stacked columns; and competitor ranked bars. Refresh is file-based. All prices and model outputs are synthetic; competitor tonnage is public-source factual context.

Excel limitation: the supplied workbook contains formula-backed pivot-style summaries and native charts. The current authoring environment does not create genuine Excel PivotTable cache objects, so this is explicitly not claimed as a real PivotTable.
