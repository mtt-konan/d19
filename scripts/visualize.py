"""
Visualize rational-distance search results.

Generates an interactive HTML report from a JSON results file.

Usage:
    uv run python scripts/visualize.py results.json
    uv run python scripts/visualize.py results.json --out report.html
    uv run python scripts/visualize.py results.json --inside   # only show points inside unit square

Opens the HTML file in the default browser when done.
"""

import argparse
import json
import webbrowser
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def load_results(path: str) -> dict:
    with open(path) as f:
        raw = json.load(f)
    points = []
    for p in raw["points"]:
        x = float(Fraction(p["x"]))
        y = float(Fraction(p["y"]))
        dists = {}
        for v in "ABCD":
            key = f"d{v}"
            val = p.get(key)
            dists[v] = float(Fraction(val)) if val is not None else None
        missing = [v for v in "ABCD" if dists[v] is None]
        den = p.get("denominator") or max(
            Fraction(p["x"]).denominator, Fraction(p["y"]).denominator
        )
        points.append(
            {
                "x": x,
                "y": y,
                "x_str": p["x"],
                "y_str": p["y"],
                "dA": dists["A"],
                "dB": dists["B"],
                "dC": dists["C"],
                "dD": dists["D"],
                "dA_str": p.get("dA") or "?",
                "dB_str": p.get("dB") or "?",
                "dC_str": p.get("dC") or "?",
                "dD_str": p.get("dD") or "?",
                "missing": missing[0] if missing else "none",
                "rational_count": p.get("rational_count", 3),
                "denominator": den,
                "inside": 0 < x < 1 and 0 < y < 1,
            }
        )
    return {
        "params": raw.get("search_params", {}),
        "elapsed": raw.get("elapsed_seconds", 0),
        "points": points,
    }


# ---------------------------------------------------------------------------
# Analytics
# ---------------------------------------------------------------------------


def compute_stats(points: list[dict]) -> dict:
    total = len(points)
    missing_counts = Counter(p["missing"] for p in points)
    inside = sum(1 for p in points if p["inside"])
    quadrants = Counter()
    for p in points:
        x, y = p["x"], p["y"]
        if x < 0 and y < 0:
            quadrants["Q3 (x<0,y<0)"] += 1
        elif x < 0:
            quadrants["Q2 (x<0,y>0)"] += 1
        elif y < 0:
            quadrants["Q4 (x>0,y<0)"] += 1
        elif x <= 1 and y <= 1:
            quadrants["Unit square region (0≤x≤1,0≤y≤1)"] += 1
        elif x > 1 and y > 1:
            quadrants["Far corner (x>1,y>1)"] += 1
        elif x > 1:
            quadrants["Right strip (x>1)"] += 1
        else:
            quadrants["Top strip (y>1)"] += 1

    # Distance ratio patterns for points with 3 rational distances
    rat3 = [p for p in points if p["rational_count"] == 3]
    rat4 = [p for p in points if p["rational_count"] == 4]

    # Denominator buckets
    dens = [p["denominator"] for p in points]
    den_max = max(dens) if dens else 0
    bucket_size = max(1, den_max // 20)
    den_buckets = defaultdict(int)
    for d in dens:
        den_buckets[(d // bucket_size) * bucket_size] += 1

    return {
        "total": total,
        "missing_counts": dict(missing_counts),
        "inside": inside,
        "quadrants": dict(quadrants),
        "rat3": len(rat3),
        "rat4": len(rat4),
        "den_min": min(dens) if dens else 0,
        "den_max": den_max,
        "den_buckets": dict(den_buckets),
        "bucket_size": bucket_size,
    }


# ---------------------------------------------------------------------------
# HTML generation with Plotly
# ---------------------------------------------------------------------------


def build_html(data: dict, title: str, inside_only: bool = False) -> str:
    points = data["points"]
    if inside_only:
        points = [p for p in points if p["inside"]]

    stats = compute_stats(points)
    params = data["params"]

    # Color map for missing vertex
    color_map = {"A": "#e74c3c", "B": "#3498db", "C": "#2ecc71", "D": "#f39c12", "none": "#9b59b6"}
    label_map = {
        "A": "dA irrational",
        "B": "dB irrational",
        "C": "dC irrational",
        "D": "dD irrational",
        "none": "all rational (4 vertices!)",
    }

    # Build scatter data grouped by missing vertex
    scatter_traces = []
    for mv in ["A", "B", "C", "D", "none"]:
        group = [p for p in points if p["missing"] == mv]
        if not group:
            continue
        scatter_traces.append(
            {
                "type": "scatter",
                "mode": "markers",
                "name": label_map[mv],
                "x": [p["x"] for p in group],
                "y": [p["y"] for p in group],
                "marker": {
                    "color": color_map[mv],
                    "size": 7,
                    "opacity": 0.8,
                    "line": {"width": 1, "color": "white"},
                },
                "text": [
                    f"({p['x_str']}, {p['y_str']})<br>"
                    f"dA={p['dA_str']} dB={p['dB_str']}<br>"
                    f"dC={p['dC_str']} dD={p['dD_str']}<br>"
                    f"den={p['denominator']}"
                    for p in group
                ],
                "hovertemplate": "%{text}<extra>" + label_map[mv] + "</extra>",
            }
        )

    # Unit square corners for annotation
    square_trace = {
        "type": "scatter",
        "mode": "markers+text",
        "name": "Vertices",
        "x": [0, 1, 1, 0],
        "y": [0, 0, 1, 1],
        "text": ["A(0,0)", "B(1,0)", "C(1,1)", "D(0,1)"],
        "textposition": ["bottom left", "bottom right", "top right", "top left"],
        "marker": {"color": "black", "size": 10, "symbol": "square"},
        "hoverinfo": "text",
    }

    # Unit square border
    square_border = {
        "type": "scatter",
        "mode": "lines",
        "name": "Unit square",
        "x": [0, 1, 1, 0, 0],
        "y": [0, 0, 1, 1, 0],
        "line": {"color": "black", "width": 2, "dash": "dot"},
        "hoverinfo": "none",
    }

    # Denominator histogram
    dens = [p["denominator"] for p in points]
    den_hist = {
        "type": "histogram",
        "x": dens,
        "nbinsx": 40,
        "marker": {"color": "#3498db", "opacity": 0.75},
        "name": "Denominator",
    }

    # Missing vertex bar chart
    mv_labels = [
        label_map[k] for k in ["A", "B", "C", "D", "none"] if stats["missing_counts"].get(k, 0) > 0
    ]
    mv_values = [
        stats["missing_counts"].get(k, 0)
        for k in ["A", "B", "C", "D", "none"]
        if stats["missing_counts"].get(k, 0) > 0
    ]
    mv_colors = [
        color_map[k] for k in ["A", "B", "C", "D", "none"] if stats["missing_counts"].get(k, 0) > 0
    ]
    mv_bar = {
        "type": "bar",
        "x": mv_labels,
        "y": mv_values,
        "marker": {"color": mv_colors},
        "text": mv_values,
        "textposition": "auto",
        "name": "Count by missing vertex",
    }

    # Distance scatter: dA vs dB (for points where both are rational)
    ab_pts = [p for p in points if p["dA"] is not None and p["dB"] is not None]
    dA_dB = {
        "type": "scatter",
        "mode": "markers",
        "x": [p["dA"] for p in ab_pts],
        "y": [p["dB"] for p in ab_pts],
        "marker": {"color": [color_map[p["missing"]] for p in ab_pts], "size": 6, "opacity": 0.7},
        "text": [f"({p['x_str']},{p['y_str']})" for p in ab_pts],
        "hovertemplate": "dA=%{x:.4f}, dB=%{y:.4f}<br>%{text}<extra></extra>",
        "name": "dA vs dB",
    }

    # dC vs dD
    cd_pts = [p for p in points if p["dC"] is not None and p["dD"] is not None]
    dC_dD = {
        "type": "scatter",
        "mode": "markers",
        "x": [p["dC"] for p in cd_pts],
        "y": [p["dD"] for p in cd_pts],
        "marker": {"color": [color_map[p["missing"]] for p in cd_pts], "size": 6, "opacity": 0.7},
        "text": [f"({p['x_str']},{p['y_str']})" for p in cd_pts],
        "hovertemplate": "dC=%{x:.4f}, dD=%{y:.4f}<br>%{text}<extra></extra>",
        "name": "dC vs dD",
    }

    # x vs y scatter with den as color
    xy_den = {
        "type": "scatter",
        "mode": "markers",
        "x": [p["x"] for p in points],
        "y": [p["y"] for p in points],
        "marker": {
            "color": [p["denominator"] for p in points],
            "colorscale": "Viridis",
            "size": 7,
            "opacity": 0.8,
            "colorbar": {"title": "Denominator"},
        },
        "text": [f"({p['x_str']},{p['y_str']}) den={p['denominator']}" for p in points],
        "hovertemplate": "%{text}<extra></extra>",
        "name": "Points (colored by den)",
    }

    # Build pattern insights
    insights = []
    mc = stats["missing_counts"]
    b_count = mc.get("B", 0)
    d_count = mc.get("D", 0)
    a_count = mc.get("A", 0)
    c_count = mc.get("C", 0)
    if a_count == 0:
        insights.append(
            "✓ <b>A(0,0) is NEVER irrational</b> — expected: A is the parametric anchor (dA always rational by construction)."
        )
    if abs(b_count - d_count) <= max(1, (b_count + d_count) // 20):
        insights.append(
            f"✓ <b>B and D appear equally often</b> ({b_count} vs {d_count}) — reflects D4 symmetry (reflection about y=x swaps B↔D)."
        )
    if c_count < b_count:
        insights.append(
            f"✓ <b>C(1,1) is hardest to make irrational</b> ({c_count} vs B={b_count}) — the diagonal vertex C is 'easier' to reach with rational distances."
        )
    inside_pct = 100 * stats["inside"] / stats["total"] if stats["total"] else 0
    if inside_only:
        insights.append(
            f"✓ <b>Filtered view:</b> showing only the {stats['inside']} point(s) strictly inside the unit square."
        )
    elif stats["total"] == 0:
        insights.append("✓ No points to summarise in this report.")
    elif stats["inside"] == stats["total"]:
        insights.append(
            f"✓ <b>All {stats['total']} point(s) shown are strictly inside</b> the unit square."
        )
    else:
        insights.append(
            f"✓ Only <b>{stats['inside']}/{stats['total']} ({inside_pct:.0f}%) points are strictly inside</b> the unit square — outside points still dominate this view."
        )
    if stats["rat4"]:
        insights.append(
            f"🌟 <b>{stats['rat4']} point(s) with ALL FOUR rational distances found!</b>"
        )

    # Build stats table rows
    stat_rows = ""
    for k, v in [
        ("Total points", stats["total"]),
        ("With 3 rational", stats["rat3"]),
        ("With 4 rational", stats["rat4"]),
        ("Inside unit square", stats["inside"]),
        ("Min denominator", stats["den_min"]),
        ("Max denominator", stats["den_max"]),
    ]:
        stat_rows += f"<tr><td>{k}</td><td><b>{v}</b></td></tr>\n"

    insights_html = "".join(f"<li>{i}</li>" for i in insights)
    params_str = ", ".join(f"{k}={v}" for k, v in params.items() if k not in ("out", "workers"))

    # Serialize plot data
    import json as _json

    def _js(obj):
        return _json.dumps(obj)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<script src="https://cdn.plot.ly/plotly-2.35.0.min.js"></script>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 0; background: #f4f6f9; color: #222; }}
  .header {{ background: #1a1a2e; color: white; padding: 16px 28px; }}
  .header h1 {{ margin: 0 0 4px; font-size: 1.4em; }}
  .header p {{ margin: 0; font-size: 0.85em; color: #aaa; }}
  .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
  .grid-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }}
  .card {{ background: white; border-radius: 10px; padding: 16px; box-shadow: 0 1px 4px rgba(0,0,0,.1); }}
  .card h3 {{ margin: 0 0 12px; font-size: 1em; color: #444; border-bottom: 1px solid #eee; padding-bottom: 8px; }}
  .insights {{ background: #fffbea; border-left: 4px solid #f39c12; }}
  .insights ul {{ margin: 0; padding-left: 20px; }}
  .insights li {{ margin-bottom: 6px; font-size: 0.92em; line-height: 1.5; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.88em; }}
  th, td {{ padding: 6px 10px; text-align: left; border-bottom: 1px solid #eee; }}
  th {{ background: #f0f0f0; font-weight: 600; }}
  .full {{ grid-column: 1 / -1; }}
  .chart {{ width: 100%; height: 380px; }}
  .chart-tall {{ width: 100%; height: 500px; }}
</style>
</head>
<body>
<div class="header">
  <h1>Rational Distance Search — Visualization</h1>
  <p>File: <code>{title}</code> &nbsp;|&nbsp; Search params: {params_str}</p>
</div>
<div class="container">
  <div class="grid">
    <!-- Summary stats -->
    <div class="card">
      <h3>Summary Statistics</h3>
      <table>
        <thead><tr><th>Metric</th><th>Value</th></tr></thead>
        <tbody>{stat_rows}</tbody>
      </table>
    </div>
    <!-- Insights -->
    <div class="card insights">
      <h3>Pattern Insights</h3>
      <ul>{insights_html}</ul>
    </div>
  </div>

  <!-- Main scatter -->
  <div class="card" style="margin-top:20px">
    <h3>Point Locations (colored by irrational distance vertex)</h3>
    <div id="scatter_main" class="chart-tall"></div>
  </div>

  <div class="grid" style="margin-top:20px">
    <!-- Missing vertex bar -->
    <div class="card">
      <h3>Which vertex has irrational distance?</h3>
      <div id="mv_bar" class="chart"></div>
    </div>
    <!-- Denominator histogram -->
    <div class="card">
      <h3>Denominator Distribution</h3>
      <div id="den_hist" class="chart"></div>
    </div>
  </div>

  <div class="grid" style="margin-top:20px">
    <!-- dA vs dB -->
    <div class="card">
      <h3>dA vs dB distance pairs</h3>
      <div id="dA_dB" class="chart"></div>
    </div>
    <!-- dC vs dD -->
    <div class="card">
      <h3>dC vs dD distance pairs</h3>
      <div id="dC_dD" class="chart"></div>
    </div>
  </div>

  <!-- Den colored scatter -->
  <div class="card" style="margin-top:20px">
    <h3>Points colored by denominator size (larger den = brighter)</h3>
    <div id="xy_den" class="chart-tall"></div>
  </div>

</div>

<script>
var layout_scatter = {{
  xaxis: {{title: "x", zeroline: true, zerolinecolor: "#ccc"}},
  yaxis: {{title: "y", zeroline: true, zerolinecolor: "#ccc", scaleanchor: "x", scaleratio: 1}},
  legend: {{orientation: "h", y: -0.12}},
  margin: {{t: 20, b: 60, l: 60, r: 20}},
  plot_bgcolor: "#fafafa",
  hovermode: "closest",
  shapes: [{{
    type: "rect", x0: 0, y0: 0, x1: 1, y1: 1,
    line: {{color: "black", width: 2, dash: "dot"}},
    fillcolor: "rgba(200,230,255,0.15)",
  }}],
}};

var scatter_data = {_js([*scatter_traces, square_border, square_trace])};
Plotly.newPlot("scatter_main", scatter_data, layout_scatter, {{responsive: true}});

Plotly.newPlot("mv_bar", [{_js(mv_bar)}],
  {{margin: {{t:20,b:80,l:60,r:20}}, plot_bgcolor:"#fafafa", yaxis:{{title:"Count"}}}},
  {{responsive: true}});

Plotly.newPlot("den_hist", [{_js(den_hist)}],
  {{margin: {{t:20,b:60,l:60,r:20}}, plot_bgcolor:"#fafafa",
    xaxis:{{title:"Denominator"}}, yaxis:{{title:"Count"}}}},
  {{responsive: true}});

Plotly.newPlot("dA_dB", [{_js(dA_dB)}],
  {{margin: {{t:20,b:60,l:60,r:20}}, plot_bgcolor:"#fafafa",
    xaxis:{{title:"dA (distance to A)"}}, yaxis:{{title:"dB (distance to B)"}},
    hovermode:"closest"}},
  {{responsive: true}});

Plotly.newPlot("dC_dD", [{_js(dC_dD)}],
  {{margin: {{t:20,b:60,l:60,r:20}}, plot_bgcolor:"#fafafa",
    xaxis:{{title:"dC (distance to C)"}}, yaxis:{{title:"dD (distance to D)"}},
    hovermode:"closest"}},
  {{responsive: true}});

var layout_den = Object.assign({{}}, layout_scatter, {{
  coloraxis: {{colorscale:"Viridis"}},
  margin: {{t:20,b:60,l:60,r:20}},
}});
Plotly.newPlot("xy_den", [{_js(xy_den)}], layout_den, {{responsive: true}});
</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Visualize rational distance results")
    parser.add_argument("input", help="JSON results file (e.g. results.json)")
    parser.add_argument("--out", help="Output HTML file (default: <input>.html)")
    parser.add_argument(
        "--inside", action="store_true", help="Only show points strictly inside the unit square"
    )
    parser.add_argument("--no-open", action="store_true", help="Don't open browser automatically")
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.out) if args.out else in_path.with_suffix(".html")

    print(f"Loading {in_path}...")
    data = load_results(str(in_path))
    print(f"  {len(data['points'])} points loaded")

    if args.inside:
        n_inside = sum(1 for p in data["points"] if p["inside"])
        print(f"  Filtering to {n_inside} points inside unit square (--inside)")

    title = in_path.name
    html = build_html(data, title, inside_only=args.inside)

    out_path.write_text(html, encoding="utf-8")
    print(f"Report written to {out_path}")

    if not args.no_open:
        webbrowser.open(out_path.resolve().as_uri())


if __name__ == "__main__":
    main()
