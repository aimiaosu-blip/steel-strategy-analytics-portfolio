SELECT CASE WHEN COUNT(*)=104 THEN 1 ELSE 0 END AS pass_row_count FROM weekly_market;
SELECT COUNT(*) AS invalid_rows FROM weekly_market WHERE hrc_usd_t<=0 OR blended_cost_usd_t<=0 OR is_synthetic<>1;
SELECT COUNT(*) AS duplicate_weeks FROM (SELECT week_start FROM weekly_market GROUP BY week_start HAVING COUNT(*)>1);
SELECT COUNT(*) AS scenario_gaps FROM (SELECT scenario FROM scenario_outlook GROUP BY scenario HAVING COUNT(*)<>6);
