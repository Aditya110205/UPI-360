"""ML layers on the full UPI monthly series (all months, no row dropped).

1. Forecast  : 6-month holdout, naive vs drift vs damped ETS, best model refit on all data
2. Phases    : K-means (k=3) on log volume -> launch / scale-up / mature
3. Anomalies : Isolation Forest on detrended growth + ticket-size change
Also: detrended seasonality (ratio to centred 12-month average) + festive test.

Run from anywhere:  python src/models.py
Writes: DuckDB tables, reports/ml_models_report.md, reports/dashboard_data.json
"""
import json
import warnings
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.holtwinters import ExponentialSmoothing

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "upi.duckdb"
HOLDOUT, HORIZON, SEED = 6, 6, 42

con = duckdb.connect(str(DB))
df = con.execute("SELECT date, num_banks, volume_mn, value_cr FROM upi_monthly ORDER BY date").df()
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")
df["ticket"] = df["value_cr"] * 1e7 / (df["volume_mn"] * 1e6)  # average rupees per transaction
v = df["volume_mn"]
n = len(df)
assert n == 114, f"expected 114 months, found {n}"


# ---------------------------------------------------------------- 1. forecast
def forecast(name, s, h):
    if name == "naive":
        return np.repeat(s.iloc[-1], h)
    if name == "drift_12m":
        slope = (s.iloc[-1] - s.iloc[-13]) / 12
        return s.iloc[-1] + slope * np.arange(1, h + 1)
    if name == "ets_damped_log":
        fit = ExponentialSmoothing(np.log(s.values), trend="add", damped_trend=True).fit()
        return np.exp(fit.forecast(h))
    raise ValueError(name)


mape = lambda a, p: float(np.mean(np.abs((a - p) / a)) * 100)
MODELS = ["naive", "drift_12m", "ets_damped_log"]
train, test = v.iloc[:-HOLDOUT], v.iloc[-HOLDOUT:]
holdout = {m: forecast(m, train, HOLDOUT) for m in MODELS}
scores = {m: mape(test.values, holdout[m]) for m in MODELS}
best = min(scores, key=scores.get)

future_idx = pd.date_range(v.index[-1] + pd.offsets.MonthBegin(1), periods=HORIZON, freq="MS")
fut = forecast(best, v, HORIZON)
g = np.log(v).diff().dropna()
sigma = float(g.iloc[-24:].std())  # recent month-on-month volatility
steps = np.arange(1, HORIZON + 1)
lo, hi = fut * np.exp(-1.28 * sigma * np.sqrt(steps)), fut * np.exp(1.28 * sigma * np.sqrt(steps))  # ~80% band

# ------------------------------------------------------------- seasonality
ratio = (v / v.rolling(12, center=True).mean()).dropna()
season = ratio.groupby(ratio.index.month).mean()
festive = ratio[ratio.index.month.isin([10, 11, 12])]
other = ratio[~ratio.index.month.isin([10, 11, 12])]
u_stat, p_festive = stats.mannwhitneyu(festive, other, alternative="two-sided")

# ---------------------------------------------------------------- 2. phases
X = StandardScaler().fit_transform(np.log(v.values).reshape(-1, 1))
km = KMeans(n_clusters=3, random_state=SEED, n_init=10).fit(X)
order = np.argsort([v.values[km.labels_ == k].mean() for k in range(3)])
names = {int(order[0]): "Launch & ramp-up", int(order[1]): "Scale-up", int(order[2]): "Mature"}
df["phase"] = [names[int(k)] for k in km.labels_]

# -------------------------------------------------------------- 3. anomalies
lg = np.log(v).diff()
lt = np.log(df["ticket"]).diff()
dev_v = lg - lg.rolling(12, min_periods=6).median().shift(1)
dev_t = lt - lt.rolling(12, min_periods=6).median().shift(1)
feat = pd.DataFrame({"dev_volume": dev_v, "dev_ticket": dev_t}).iloc[13:]
iso = IsolationForest(contamination=0.06, random_state=SEED, n_estimators=300)
iso.fit(StandardScaler().fit_transform(feat))
flag = iso.predict(StandardScaler().fit_transform(feat)) == -1
score = -iso.score_samples(StandardScaler().fit_transform(feat))  # higher = more unusual
an = feat.copy()
an["is_anomaly"], an["score"] = flag, score
an["volume_mn"] = v.loc[an.index]
an["mom_pct"] = (np.exp(lg.loc[an.index]) - 1) * 100
an["trend_mom_pct"] = (np.exp(lg.rolling(12, min_periods=6).median().shift(1).loc[an.index]) - 1) * 100

# --------------------------------------------------------------------- save
def to_db(name, frame):
    out = frame.copy()
    out.insert(0, "date", out.index.strftime("%Y-%m-%d"))
    con.execute(f"DROP TABLE IF EXISTS {name}")
    con.register("tmp_df", out.reset_index(drop=True))
    con.execute(f"CREATE TABLE {name} AS SELECT * FROM tmp_df")
    con.unregister("tmp_df")


to_db("segments", df[["volume_mn", "phase"]].rename(columns={"phase": "segment_name"}))
to_db("anomalies", an[["volume_mn", "mom_pct", "trend_mom_pct", "score", "is_anomaly"]])
to_db("forecast_holdout", pd.DataFrame({"actual": test.values, **{m: holdout[m] for m in MODELS}}, index=test.index))
to_db("forecast_future", pd.DataFrame({"forecast": fut, "lo80": lo, "hi80": hi}, index=future_idx))

phases = []
for p in ["Launch & ramp-up", "Scale-up", "Mature"]:
    s = df[df["phase"] == p]
    phases.append({"name": p, "months": int(len(s)), "from": s.index.min().strftime("%b %Y"),
                   "to": s.index.max().strftime("%b %Y"), "avg_volume": round(float(s.volume_mn.mean()), 1),
                   "avg_ticket": round(float(s.ticket.mean()))})

flagged = an[an.is_anomaly].sort_values("score", ascending=False)
payload = {
    "months": [{"d": d.strftime("%Y-%m"), "b": int(r.num_banks), "v": round(float(r.volume_mn), 2),
                "c": round(float(r.value_cr), 2), "t": round(float(r.ticket), 1), "p": r.phase}
               for d, r in df.iterrows()],
    "forecast": [{"d": d.strftime("%Y-%m"), "f": round(float(f)), "lo": round(float(l)), "hi": round(float(h))}
                 for d, f, l, h in zip(future_idx, fut, lo, hi)],
    "holdout": {"months": [d.strftime("%Y-%m") for d in test.index], "actual": [round(float(x)) for x in test],
                "pred": {m: [round(float(x)) for x in holdout[m]] for m in MODELS},
                "mape": {m: round(scores[m], 2) for m in MODELS}, "best": best},
    "season": {str(m): round(float(x), 4) for m, x in season.items()},
    "festive": {"festive_mean": round(float(festive.mean()), 4), "other_mean": round(float(other.mean()), 4),
                "p": round(float(p_festive), 4)},
    "phases": phases,
    "anomalies": [{"d": d.strftime("%Y-%m"), "v": round(float(r.volume_mn), 1), "mom": round(float(r.mom_pct), 1),
                   "trend": round(float(r.trend_mom_pct), 1), "s": round(float(r.score), 3), "f": bool(r.is_anomaly)}
                  for d, r in an.iterrows()],
}
(ROOT / "reports").mkdir(exist_ok=True)
(ROOT / "reports" / "dashboard_data.json").write_text(json.dumps(payload))

lines = [
    "# ML Models Report", "",
    f"All results computed on the full series: {n} months, {v.index[0]:%b %Y} to {v.index[-1]:%b %Y}.", "",
    f"## 1. Forecast (holdout: train to {train.index[-1]:%b %Y}, test {test.index[0]:%b %Y} to {test.index[-1]:%b %Y})", "",
    "| Model | Holdout MAPE |", "|---|---|",
    *[f"| {m}{' (selected)' if m == best else ''} | {scores[m]:.2f}% |" for m in MODELS], "",
    f"Selected model refit on all data. Next {HORIZON} months (approx. 80% band from recent volatility):", "",
    "| Month | Forecast (M txns) | Low | High |", "|---|---|---|---|",
    *[f"| {d:%b %Y} | {f:,.0f} | {l:,.0f} | {h:,.0f} |" for d, f, l, h in zip(future_idx, fut, lo, hi)], "",
    "## 2. Seasonality (detrended: ratio to centred 12-month average)", "",
    f"- Highest month index: {int(season.idxmax())} ({season.max():.3f}); lowest: {int(season.idxmin())} ({season.min():.3f})",
    f"- Oct-Dec vs rest, Mann-Whitney p = {p_festive:.4f} (festive mean {festive.mean():.3f} vs {other.mean():.3f})", "",
    "## 3. Growth phases (K-means k=3 on log volume)", "",
    "| Phase | Months | Period | Avg volume (M) | Avg ticket (Rs) |", "|---|---|---|---|---|",
    *[f"| {p['name']} | {p['months']} | {p['from']} to {p['to']} | {p['avg_volume']:,} | {p['avg_ticket']:,} |" for p in phases], "",
    f"## 4. Anomalies (Isolation Forest, contamination 6%, {len(an)} months scored from {an.index[0]:%b %Y})", "",
    "Features: deviation of month-on-month volume growth and of ticket-size change from their trailing 12-month median.", "",
    "| Month | Volume (M) | MoM % | Trend MoM % | Score |", "|---|---|---|---|---|",
    *[f"| {d:%b %Y} | {r.volume_mn:,.0f} | {r.mom_pct:+.1f} | {r.trend_mom_pct:+.1f} | {r.score:.3f} |" for d, r in flagged.iterrows()], "",
]
(ROOT / "reports" / "ml_models_report.md").write_text("\n".join(lines))
print("best", best, scores)
print("festive p", round(p_festive, 4))
print([(p["name"], p["months"], p["from"], p["to"]) for p in phases])
print(flagged[["volume_mn", "mom_pct", "trend_mom_pct", "score"]].round(2).to_string())
print(pd.DataFrame({"f": fut, "lo": lo, "hi": hi}, index=future_idx).round(0).to_string())