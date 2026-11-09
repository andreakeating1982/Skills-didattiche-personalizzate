# Charts that read at a glance

## Pick the chart

| Question                                              | Chart                                          |
| ----------------------------------------------------- | ---------------------------------------------- |
| How does a value change over time?                    | Line (bars for few periods or discrete counts) |
| Which categories are biggest?                         | Horizontal bar, sorted                         |
| How is a total split?                                 | Stacked bar, or a pie only for 2-5 slices      |
| How do two measures relate?                           | Scatter, with a trend line when it helps       |
| How are values distributed?                           | Histogram or box plot                          |
| How do many categories compare across two dimensions? | Heatmap                                        |
| Did something change between two points?              | Slope chart or a dumbbell plot                 |

Avoid 3D charts, dual y-axes (use two small charts instead), and pies with many slices.

## Make it readable

- **Title.** It states the takeaway ("Online sales passed in-store in March"), not just the variable names. Add a subtitle with the units and the period.
- **Axes and labels.** Label the axes with units, and format the ticks: thousands separators, %, currency.
- **Focus.** Sort the bars. Highlight the bar or line that matters in a strong colour and keep the rest grey.
- **Annotate.** Label key points directly (the last value, the maximum, the event that explains a jump) instead of making readers use a legend.
- **Consistency.** Use one colour per category across all charts in a deliverable, and the same scales when charts are compared side by side.
- **Source.** Add a small source line at the bottom.

## matplotlib template

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

plt.style.use("default")
plt.rcParams.update({
    "figure.dpi": 100, "savefig.dpi": 200, "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
})
ACCENT, MUTED = "#4f46e5", "#c7c9d1"

df = df.sort_values("revenue")  # barh draws the first row at the bottom
fig, ax = plt.subplots(figsize=(10, 5.6))
colors = [ACCENT if c == "Online" else MUTED for c in df["channel"]]
ax.barh(df["channel"], df["revenue"], color=colors)
ax.xaxis.set_major_formatter(mtick.StrMethodFormatter("${x:,.0f}"))
ax.set_title("Online is now the largest channel", pad=30)
ax.text(0, 1.015, "Revenue by channel, Q3 2026, USD", transform=ax.transAxes, color="#555", va="bottom")
for y, v in enumerate(df["revenue"]):
    ax.text(v, y, f"  ${v:,.0f}", va="center", fontsize=10)
fig.text(0.01, 0.01, "Source: company sales export", fontsize=8, color="#777")
fig.tight_layout()
fig.savefig("/home/user/analysis/revenue_by_channel.png", bbox_inches="tight")
```

- Set the style before any custom fonts; a style applied afterwards overrides them.
- Non-Latin text (Chinese, Japanese, Korean, Arabic, Hindi, Thai) needs a font that covers it, or it renders as boxes. The Noto fonts are installed (`fc-list | grep -i "noto sans cjk"`; in an older sandbox `sudo apt-get install -y -qq fonts-noto-cjk fonts-noto-core`). Register the file with matplotlib:
  ```python
  from matplotlib import font_manager
  font_manager.fontManager.addfont(path)
  plt.rcParams["font.family"] = font_manager.FontProperties(fname=path).get_name()
  ```
- Look at every chart once with `file_view` before delivering. Check for overlapping labels, clipped titles and unreadable ticks, fix what's wrong and re-render once. Don't keep polishing a chart that is already correct and readable.

## Interactive charts

```python
import plotly.express as px
fig = px.line(df, x="date", y="users", color="plan", title="Weekly active users by plan")
fig.update_layout(template="plotly_white", hovermode="x unified")
fig.write_html("/home/user/analysis/users.html", include_plotlyjs="cdn")
```

Deliver the HTML file. Use matplotlib PNGs for anything that must appear inline in the chat or in a document.
