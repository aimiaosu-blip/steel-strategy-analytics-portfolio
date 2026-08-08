# Medium/Long-Term Micro-economics Model

## Decision question
How could China steel demand, supply discipline, raw-material inflation and EAF transition interact to shape 2025–2030 HRC cash margins?

## Logic
Demand and supply grow from visible 2025 base assumptions. Market tightness is `(demand - supply) / supply`; price responds through a scenario elasticity. Cash cost grows with raw-material inflation and receives a small modeled benefit from the EAF-share pathway. Margin equals modeled steel price minus modeled cash cost.

## Audit trail
Inputs: `data/raw/scenario_assumptions.csv`. Outputs: `data/processed/scenario_outlook_bi.csv`. The Excel workbook exposes the same assumptions and formulas. SQL tables provide an independent check.

## Scenarios
- Downside: faster demand contraction, slower capacity adjustment, lower EAF transition.
- Base: gradual demand decline with modest supply discipline.
- Upside: stable-to-positive demand, stronger adjustment and higher EAF share.

## Sensitivities
The workbook includes price elasticity, cost inflation, demand CAGR, supply CAGR and 2030 EAF share as editable inputs. None is a company forecast.

## Validation / QC
No negative price or cost; scenario-year uniqueness; supply-demand balance arithmetic; margin bridge reconciliation; EAF share bounded between 0 and 100%; weekly ranges checked for plausible portfolio calibration.
