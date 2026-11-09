---
name: research-report
description: 'Research a topic across many sources and write a cited long-form document: report, article, white paper, literature review, market or competitor overview, guide. Not needed for a quick answer one or two searches settle.'
---

# Research report

## Research

1. **Scope.**
   - Write down the 3-7 questions the document must answer, plus its audience, depth, time frame and region.
   - Follow any scope or length the user gave.
   - Ask only when a choice would change the whole document (which market, which product line) and you cannot infer it.
2. **Search wide, then narrow.** Start with broad queries to learn the landscape and the vocabulary, then target the gaps. Pick the right `search` type:
   - `news` with a time filter for recent events;
   - `research` for papers;
   - `company` and `people` for organisations and profiles;
   - `pdf` for reports and filings;
   - the financial and economic types for market data;
   - `chat_history` when the user refers to earlier work.
3. **Read sources, not snippets.**
   - Open the pages that matter with `fetch_url_content` (articles, PDFs, YouTube transcripts).
   - Use `browser_navigate` for pages that need a browser, and always for Reddit, LinkedIn and Facebook.
4. **Weigh sources.**
   - Prefer primary and authoritative sources: official statistics, filings, papers, company pages and established outlets.
   - Note the date of every number.
   - Confirm key figures in a second independent source, and record disagreements instead of hiding them.
5. **Keep notes on disk.** Append findings to `/home/user/research/notes.md` as you go, each claim with its source URL. Long research outlives the context window, and notes survive it.
6. **Many similar items** (10 or more companies, products, people or papers that each need their own lookup): read the `wide-research` skill and fan out with `parallel_map` instead of researching them one by one.
7. **Stop when the questions are answered.** Search again only for a gap or a contradiction that could change a conclusion.

## Write

- **Open with the answer.** Start with the substance: no preamble, no "this report will", no research-method section unless asked.
- **Headings** that name the topic or finding and help a reader navigate. Short paragraphs, each making one point, in plain direct language. Explain technical terms the first time they matter.
- **Concrete details.** Numbers with units, dates and sources; named examples. Put the limits of the evidence next to the claim they affect.
- **Prose first.** Use lists for real sets or steps, and tables when comparing several items on the same attributes.
- **Length.** As long as the questions need, without padding or repetition. Follow the user's length when given.
- **Citations.** Cite every sourced fact or figure inline as `[1]`, `[2]`, and end with a **References** list: `[1] Title of the page, Publisher, date. https://...`. Reuse a number for the same source. Attribute direct quotes and keep them short.
- **Visuals.** Add a chart when numbers are easier to see (the `data-analysis` skill), or real photos found with `search` type `image` when they help. Embed them as markdown images.
- **Long documents.** Write section by section into files (`/home/user/research/report/01-....md`, ...), then join them into one `report.md`. Write in final form from the start, never as rough notes to rewrite later.

## Deliver

Deliver `report.md` (plus charts or data files) with `send_attachment`, the main document first. Charts the report shows by sandbox path are stored with it, and the user can open the report in the chat and download it as Markdown, PDF or Word, so don't convert it unless asked for a designed PDF or an editable .docx (see the `documents` skill). If the result lists `missing_images`, fix those image paths and deliver again. In the chat, give a short summary of the key findings in a few sentences, not the whole document.
