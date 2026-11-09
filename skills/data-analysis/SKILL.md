---
name: data-analysis
description: Analyze data and make charts. Use when the user shares a CSV, Excel, JSON or database export, asks for statistics, trends, comparisons, forecasts, dashboards or charts, or needs numbers found, cleaned, combined or summarized from data files.
---

# Data analysis

Work in Python in the sandbox (pandas, numpy, scipy, matplotlib, seaborn, plotly, DuckDB and openpyxl are installed; install anything else with `pip install -q`). Work in one folder for the task (for example `/home/user/analysis/`): save every script there before running it, and keep one `analysis.py` (or a few numbered scripts) so the work can be rerun and adjusted. Don't leave scripts loose in `/home/user`.

## Workflow

1. **Locate the data.**
   - Uploads are listed under Sandbox Files (usually `/home/user/uploads/`).
   - Download files at URLs with `file_upload` or `curl`.
   - When the user needs public data they don't have, find an authoritative source (official statistics, filings, the `search` tool's financial and economic types) and cite it.
   - Never invent, simulate or randomly generate data for an analysis. If the real data can't be found, say so and ask.
2. **Profile before analyzing.**
   - Print the shape, column types, missing values, duplicates, value ranges, a few sample rows and the distinct values of categorical columns.
   - Check the units, currencies, date formats, time zones and what one row represents.
   - Read Excel files with every sheet listed (`pd.ExcelFile(path).sheet_names`).
3. **Clean deliberately.** Record each cleaning step (dropped rows, parsed dates, unit conversions) so you can report it.
4. **Answer the actual question.**
   - Compute the specific numbers the user asked for first, then add only the analysis that changes the conclusion: breakdowns, trends, outliers, comparisons against a baseline.
   - State the assumptions behind any forecast or estimate.
5. **Visualize** where a chart says it faster than a sentence. Chart rules are in `references/charts.md`.
6. **Check your numbers.**
   - Totals match the source.
   - Percentages use the right base.
   - Joins neither duplicated nor dropped rows (compare row counts before and after).
   - Dates cover the intended period.
7. **Report.**
   - Lead with the answer in plain language, with the key figures.
   - Then the supporting detail and charts embedded inline (`![Revenue by month](/home/user/analysis/revenue_by_month.png)`).
   - Note any caveat in the data where it affects a conclusion.

## Choosing outputs

| The user needs                    | Deliver                                                                                                                      |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| An answer or insight              | The reply itself, with the key numbers and 1-3 inline charts                                                                 |
| A spreadsheet to keep working in  | An `.xlsx` with formatted tables and live formulas (see `../documents/references/xlsx.md`)                                   |
| A shareable report                | A markdown or PDF report with charts (see the `documents` skill)                                                             |
| An interactive chart or dashboard | A plotly HTML file (`fig.write_html("dashboard.html", include_plotlyjs="cdn")`). For a hosted dashboard app, build a web app |
| Cleaned or combined data          | CSV or XLSX of the result, plus the script when they may rerun it                                                            |

Deliver the files with `send_attachment`, the main deliverable first. Charts shown inline are already visible. Attach them as well only when the user will reuse them.

## Large or many files

- **Files over ~200 MB, or many files:** read in chunks (`chunksize=`), load only the needed columns (`usecols=`), or use DuckDB (installed) to run SQL straight on the CSV or Parquet files.
- **Long computations:** run them with `shell` `background: true, notify: true` instead of waiting in the foreground.
- **Never print a whole large DataFrame.** Print `head()`, `describe()` and the aggregates you need.
