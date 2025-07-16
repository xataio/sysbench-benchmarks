#!/usr/bin/env python3
"""
plot_sysbench.py  –  quick visualiser for “report-per-second” lines in sysbench
-------------------------------------------------------------------------

Example usage
-------------

  # read from a file
  python plot_sysbench.py results.log

  # or pipe / redirect
  cat results.log | python plot_sysbench.py
  sysbench ... run | python plot_sysbench.py

What it does
------------

• Extracts, per second:
      – tps         (transactions-per-second)
      – qps         (queries-per-second)
      – p99 latency (lat (ms,99%))
• Builds a Pandas DataFrame.
• Plots three line charts (one window each) with y-axes starting at 0.
"""

import re
import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ─── 1.  read stdin or a filename argument ───────────────────────────────────────
if len(sys.argv) > 1:
    raw_text = Path(sys.argv[1]).read_text()
else:
    raw_text = sys.stdin.read()

if not raw_text.strip():
    sys.exit("No input detected.  Pipe a sysbench log or pass a file path.")

# ─── 2.  regex-parse the interesting bits ───────────────────────────────────────
PATTERN = re.compile(
    r"\[\s*(\d+)s\s*]"          # [ 42s ]
    r".*?tps:\s*([0-9.]+)"      # tps: 602.03
    r".*?qps:\s*([0-9.]+)"      # qps: 18076.88
    r".*?lat \(ms,99%\):\s*([0-9.]+)",  # lat (ms,99%): 331.91
    re.I,
)

records = []
for line in raw_text.splitlines():
    m = PATTERN.search(line)
    if m:
        sec, tps, qps, p99 = m.groups()
        records.append(
            {
                "second": int(sec),
                "tps":    float(tps),
                "qps":    float(qps),
                "p99":    float(p99),
            }
        )

if not records:
    sys.exit("No matching sysbench lines found – check that you enabled "
             "`--report-interval=1` or similar.")

df = (
    pd.DataFrame(records)
      .sort_values("second")
      .reset_index(drop=True)
)

# ─── 3.  draw the charts ────────────────────────────────────────────────────────
plots = [
    ("tps", "Transactions / sec", "TPS over time"),
    ("qps", "Queries / sec",      "QPS over time"),
    ("p99", "Latency p99 (ms)",   "p99 latency over time"),
]

for column, ylabel, title in plots:
    fig, ax = plt.subplots()
    ax.plot(df["second"], df[column])
    ax.set_title(title)
    ax.set_xlabel("Seconds since start")
    ax.set_ylabel(ylabel)
    ax.grid(True)

    # Force y-axis to start at zero
    ax.set_ylim(bottom=0)

plt.show()

