"""Builds dashboard/index.html from dashboard/template.html + reports/dashboard_data.json.
Run after `python src/models.py`:   python src/build_dashboard.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = (ROOT / "reports" / "dashboard_data.json").read_text(encoding="utf-8")
tpl = (ROOT / "dashboard" / "template.html").read_text(encoding="utf-8")
assert "/*DATA*/null" in tpl, "placeholder missing in template.html"
head = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>html,body{margin:0}</style></head><body>'
(ROOT / "dashboard" / "index.html").write_text(head + tpl.replace("/*DATA*/null", data) + "</body></html>", encoding="utf-8")
print("Wrote dashboard/index.html")