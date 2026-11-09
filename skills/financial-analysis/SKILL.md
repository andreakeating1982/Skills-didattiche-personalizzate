---
name: financial-analysis
description: Analyze stocks, ETFs, crypto, currencies, commodities and the economy with live market data. Use for stock research and comparisons, earnings, valuation, portfolio or watchlist reviews, market recaps and macro questions.
---

# Financial analysis

## Data sources

The `search` tool has structured, live market data types. Use them instead of a web search for prices and figures:

| Need                                                          | `search` type                      | Query                                                                                      |
| ------------------------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------ |
| Price, market cap, P/E, EPS, 52-week range, company overview  | `stock_quote`                      | Tickers: `["AAPL", "MSFT"]`                                                                |
| Income statement, balance sheet, cash flow (last 4 quarters)  | `stock_financials`                 | Tickers                                                                                    |
| Reported vs expected EPS, upcoming earnings, IPO calendar     | `earnings`                         | A ticker, or `"ipo"`                                                                       |
| News with sentiment                                           | `market_news`                      | Tickers (`"AAPL"`, `"CRYPTO:BTC"`, `"FOREX:USD"`) or topics (`"technology"`, `"earnings"`) |
| Top gainers, losers, most active today                        | `market_movers`                    | (none)                                                                                     |
| ETF profile, holdings, expense ratio, sectors                 | `etf`                              | ETF tickers                                                                                |
| Exchange rates                                                | `forex`                            | Pairs: `"EUR/USD"`                                                                         |
| Crypto prices                                                 | `crypto`                           | Symbols: `"BTC"`, `"ETH"`                                                                  |
| Commodities                                                   | `commodities`                      | `"gold"`, `"oil"`, `"natural gas"`                                                         |
| US macro (GDP, CPI, unemployment, fed funds, treasury yields) | `economic`                         | The indicator name                                                                         |
| Filings, analyst commentary, industry context                 | `financial`, `pdf`, `news`, `info` | Text queries                                                                               |

Note the date of every figure. Quotes may be delayed and statements are quarterly. Use `fetch_url_content` on investor-relations pages and filings when you need detail beyond these feeds.

## Workflows

- **Single stock overview:**
  1. Get the price and key metrics with `stock_quote`.
  2. Get the trend in revenue, margins and cash flow with `stock_financials`.
  3. Get the last surprises and the next report date with `earnings`.
  4. Get recent catalysts with `market_news`.
  5. Write a balanced view: the business, the numbers, valuation in context (versus history and peers), risks.
- **Comparison:** pull the same metrics for every ticker in one call per type, build a table (price, market cap, P/E, revenue growth, margin, debt), and chart 1-2 metrics that separate them (see `data-analysis`).
- **Portfolio or watchlist review:**
  - Read the holdings (from an uploaded file or the user's message) and fetch quotes for all of them.
  - Compute the weights, the gains and losses and the concentration by sector or asset.
  - Flag concentration and upcoming earnings dates.
  - Deliver a table (and an XLSX when the list is long).
- **Market recap:** combine `market_movers`, `market_news` for the main topics and the key `economic` releases. Keep it short and dated ("as of ...").
- **Calculations** (returns, CAGR, ratios, DCF, scenarios): do them in Python, never mentally, and show the inputs and assumptions so they can be checked.

## How to present it

- Lead with the answer and the 3-5 numbers that support it, then the detail.
- Separate facts (reported numbers, prices with dates) from interpretation (what they may mean).
- Give the risks and the counter-arguments alongside the positives.
- Never promise returns. Never present a buy, sell or hold call as personal advice. When the user asks what they should do, explain the factors and the trade-offs for their situation and note that this is general information, not personal financial advice.
- Never place, simulate or arrange trades. Marky cannot transact.
