-- Weekly market update
SELECT week_start, hrc_usd_t, iron_ore_usd_t, coking_coal_usd_t, hrc_margin_usd_t FROM weekly_market ORDER BY week_start DESC LIMIT 13;
-- Monthly update and spread
SELECT month, hrc_usd_t, blended_cost_usd_t, hrc_margin_usd_t, crude_steel_output_mt, apparent_demand_mt FROM monthly_market ORDER BY month;
-- Scenario sensitivity
SELECT scenario, year, demand_mt, supply_mt, balance_mt, steel_price_usd_t, cash_cost_usd_t, margin_usd_t FROM scenario_outlook ORDER BY scenario,year;
-- Competitor comparison
SELECT producer, "2024_crude_steel_mt", rank_2024, profile_focus, watch_metric FROM competitors ORDER BY rank_2024;
