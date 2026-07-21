# 3x3 Punishment Strength Results

This folder contains Aya's full 3x3 comparison runs for regular learning and punishment strengths `1.0`, `0.5`, and `0.25`.

## Run Setup

All four conditions used the same 3x3 maze setup:

| Setting | Value |
|---|---:|
| Batches per condition | 50 |
| Trials per batch | 150 |
| Total trials per condition | 7500 |
| Max steps per trial | 150 |

## Main Summary

| Condition | First 5 avg | Last 5 avg | Improvement | Max-step failures | Failure rate |
|---|---:|---:|---:|---:|---:|
| regular | 29.56 | 85.01 | -187.6% | 1929 | 25.7% |
| punishment_1.0 | 108.69 | 99.60 | 8.4% | 3270 | 43.6% |
| punishment_0.5 | 81.04 | 71.99 | 11.2% | 2003 | 26.7% |
| punishment_0.25 | 64.19 | 62.97 | 1.9% | 1759 | 23.5% |

## B Values

The `b` values use the linearized form of:

```text
y = a * e^(-bt)
```

with `a = 150`, matching `maxStepsPerTrial`.

| Condition | Avg b value | Min b value | Max b value |
|---|---:|---:|---:|
| regular | 0.01622751 | -0.00000000 | 0.02382839 |
| punishment_1.0 | 0.00562302 | 0.00235304 | 0.01207558 |
| punishment_0.5 | 0.01097389 | 0.00429131 | 0.02144000 |
| punishment_0.25 | 0.01519213 | 0.00430853 | 0.02280475 |

Higher `b` means a steeper downward fitted curve within the batches. Because the regular 3x3 baseline is unstable across batches, the `b` values should be read together with the learning curves and failure rates.

## Interpretation

Punishment strength `1.0` looks too strong because it has the highest failure rate. Strength `0.5` shows the clearest improvement over time in the batch summaries. Strength `0.25` has the lowest failure rate but only a small improvement. The regular baseline starts low but becomes unstable, so this 3x3 maze is probably not a clean final baseline.

Best next step: try a simplified 5x5 maze with a few walls and compare regular vs punishment strength `0.5`.

## Files

| File | Description |
|---|---|
| `condition_summary.csv` | One row per condition with aggregate learning/failure statistics. |
| `batch_summary.csv` | One row per batch per condition. |
| `b_values.csv` | One `b` value per batch per condition. |
| `b_value_summary.csv` | Average/min/max `b` values by condition. |
| `raw_learning_curve.svg` | Raw average steps per batch graph. |
| `smoothed_learning_curve.svg` | 5-batch rolling average graph. |
| `raw_data/` | The original `batch0.txt` through `batch49.txt` files for each condition. |
| `calculate_b_values.py` | Script to regenerate `b_values.csv` and `b_value_summary.csv` from `raw_data/`. |

To recalculate the `b` values:

```bash
python3 calculate_b_values.py
```
