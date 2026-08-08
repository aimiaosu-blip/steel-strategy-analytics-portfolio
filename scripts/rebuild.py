from pathlib import Path
import csv, sqlite3, sys
root=Path(__file__).resolve().parents[1]
db=root/'data/steel_strategy.sqlite'
con=sqlite3.connect(db)
checks=[]
checks.append(con.execute('SELECT COUNT(*) FROM weekly_market').fetchone()[0]==104)
checks.append(con.execute('SELECT COUNT(*) FROM weekly_market WHERE is_synthetic<>1 OR hrc_usd_t<=0').fetchone()[0]==0)
checks.append(con.execute('SELECT COUNT(*) FROM scenario_outlook').fetchone()[0]==18)
for q in (root/'sql/quality_tests.sql').read_text().split(';'):
    if q.strip(): con.execute(q)
con.close()
if not all(checks): raise SystemExit('validation failed')
print('steel portfolio checks passed')
