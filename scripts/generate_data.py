"""Deterministically regenerate the synthetic steel datasets and SQLite model."""
from pathlib import Path
from datetime import date, timedelta
import csv, math, random, sqlite3

ROOT=Path(__file__).resolve().parents[1]; SEED=20260809
def write_csv(path,rows):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)

rng=random.Random(SEED);weeks=[];start=date(2024,1,1)
for i in range(104):
    d=start+timedelta(days=7*i); season=math.sin(2*math.pi*i/52)
    iron=108+12*season-.10*i+rng.gauss(0,3.2); coal=236+35*math.sin(2*math.pi*(i+8)/52)-.22*i+rng.gauss(0,7)
    scrap=362+21*season-.12*i+rng.gauss(0,6); hrc=555+24*season-.23*i+rng.gauss(0,8); rebar=520+27*math.sin(2*math.pi*(i-4)/52)-.28*i+rng.gauss(0,8)
    output=19.6+.9*season-.007*i+rng.gauss(0,.22); demand=19+.75*season-.012*i+rng.gauss(0,.25); exports=2.05+.012*i+.12*season+rng.gauss(0,.05)
    bf=1.60*iron+.50*coal+58; eaf=.78*scrap+66; cost=.88*bf+.12*eaf; margin=hrc-cost-34
    weeks.append(dict(week_start=d.isoformat(),hrc_usd_t=round(hrc,2),rebar_usd_t=round(rebar,2),iron_ore_usd_t=round(iron,2),coking_coal_usd_t=round(coal,2),scrap_usd_t=round(scrap,2),crude_steel_output_mt=round(output,3),apparent_demand_mt=round(demand,3),exports_mt=round(exports,3),bf_bof_cost_usd_t=round(bf,2),eaf_cost_usd_t=round(eaf,2),blended_cost_usd_t=round(cost,2),hrc_margin_usd_t=round(margin,2),is_synthetic=True))
write_csv(ROOT/'data/raw/weekly_market_synthetic.csv',weeks)
bucket={}
for r in weeks: bucket.setdefault(r['week_start'][:7],[]).append(r)
monthly=[]
for m,rows in sorted(bucket.items()):
    monthly.append({'month':m,**{c:round(sum(r[c] for r in rows)/len(rows),2) for c in ['hrc_usd_t','rebar_usd_t','iron_ore_usd_t','coking_coal_usd_t','scrap_usd_t','blended_cost_usd_t','hrc_margin_usd_t']},**{c:round(sum(r[c] for r in rows),2) for c in ['crude_steel_output_mt','apparent_demand_mt','exports_mt']}})
write_csv(ROOT/'data/processed/monthly_market_bi.csv',monthly)
assumptions=list(csv.DictReader((ROOT/'data/raw/scenario_assumptions.csv').open()))
for r in assumptions:
    for k in r:
        if k!='scenario':r[k]=float(r[k])
out=[]
for a in assumptions:
    for year in range(2025,2031):
        n=year-2025; dem=980*(1+a['demand_cagr'])**n; sup=995*(1+a['supply_cagr'])**n; tight=(dem-sup)/sup
        price=520*(1+a['cost_inflation'])**n*(1+a['price_elasticity']*tight); cost=455*(1+a['cost_inflation'])**n*(1-.025*n*(a['eaf_share_2030']-.15))
        out.append(dict(scenario=a['scenario'],year=year,demand_mt=round(dem,1),supply_mt=round(sup,1),balance_mt=round(sup-dem,1),steel_price_usd_t=round(price,1),cash_cost_usd_t=round(cost,1),margin_usd_t=round(price-cost,1),eaf_share=round(.15+(a['eaf_share_2030']-.15)*n/5,3)))
write_csv(ROOT/'data/processed/scenario_outlook_bi.csv',out)
competitors=list(csv.DictReader((ROOT/'data/raw/competitor_profiles_public.csv').open()))
db=ROOT/'data/steel_strategy.sqlite';db.unlink(missing_ok=True);con=sqlite3.connect(db)
for name,rows in [('weekly_market',weeks),('monthly_market',monthly),('scenario_assumptions',assumptions),('scenario_outlook',out),('competitors',competitors)]:
    cols=list(rows[0]); defs=[]
    for c in cols:
        v=rows[0][c];defs.append(f'"{c}" '+('INTEGER' if isinstance(v,(bool,int)) else 'REAL' if isinstance(v,float) else 'TEXT'))
    con.execute(f'CREATE TABLE {name} ({",".join(defs)})');con.executemany(f'INSERT INTO {name} VALUES ({",".join("?" for _ in cols)})',[[r[c] for c in cols] for r in rows])
con.commit();con.close();print(f'regenerated with seed {SEED}')
