---
name: wide-research
description: MUST read before researching, enriching or comparing many similar items (10+ companies, people, products, websites or papers that each need their own lookup; 5+ when the user asks for thorough coverage). Fans out sub-agents with parallel_map.
---

# Wide research with parallel_map

`parallel_map` runs one sub-agent per item, up to 50 at a time, each with the same prompt template and the same output fields. It is how you research 40 companies in the time one takes.

## When to fan out

Fan out when every item needs its own searching or reading and the items are comparable. For example:

- contact details for 60 agencies;
- pricing pages of 25 competitors;
- a profile of each of 30 speakers;
- a summary of 20 papers.

Do not fan out when:

- **One search or one page has it all.** A list on a single page, or an API that returns everything at once.
- **Few items or tightly linked questions.** Fewer than about 5 items, or questions that depend on each other: research them directly.
- **The same deterministic operation per item.** Resizing 200 images or calling an API per row is a single script with a loop in the sandbox, not sub-agents.

## Steps

1. **Get the full item list first.** Use the user's list, or build it with `search` and `fetch_url_content` (one page often lists them all). Deduplicate, then make each input specific enough to identify the item ("Acme Robotics (acmerobotics.com), Austin TX" rather than "Acme").
2. **Write the prompt template.** It must stand alone, because each sub-agent sees only it and its input:

   - what to find and where to look first (official site, LinkedIn, Crunchbase, the paper's abstract page);
   - what counts as an acceptable source;
   - "leave a field empty rather than guess" for anything not found.

   Example:
   `Research the company {{input}}. From its official website (and LinkedIn if needed), find its main product, pricing model, headquarters city, employee range and a contact email. Use only information you actually read on a page; leave a field empty if you can't confirm it. Include the URL you used.`

3. **Design the output fields.** Make them flat and typed (`string`, `number`, `boolean`), with snake_case names and a one-line description each. Always include a `source_url` field. Avoid fields that need judgment across items (ranking): do those after merging.
4. **Call once with all inputs** (at most 100 per call; for more, call again with the next 100). Keep the default concurrency of 20 unless the sites rate-limit.
5. **Read the results file.** The tool saves all results as JSON at `/home/user/<name>.json`. Read it with `file_read`, or load it with pandas.
6. **Merge and check.**
   - Count the empty fields and the errors.
   - Re-run only the failed or empty items with a sharper prompt when they matter.
   - Normalise formats (countries, currencies, dates), deduplicate, and spot-check a few rows against their `source_url`.
7. **Deliver.**
   - Show the table in the reply when it is short (up to about 20 rows), with the key takeaways above it.
   - For longer tables, write CSV or XLSX in the sandbox and deliver it with `send_attachment`, summarising in the chat.

## Limits

Sub-agents can only search and read web pages, with about 10 steps each. They cannot browse with clicks, log in, use the sandbox or generate media. Give them tasks that fit those limits, and do anything else yourself after merging.
