# fetch/raw — manifest

One line per fetched page. Cowork/Desktop appends here after each fetch.

| url | tab | retrieved_at | file |
|---|---|---|---|
| https://www.faros.ai/platform | platform | 2026-06-26T23:57:50Z | platform__overview.json |
| https://www.faros.ai/ | capabilities | 2026-06-26T23:57:50Z | capabilities__home.json |
| https://www.faros.ai/platform/token-intelligence | capabilities | 2026-06-26T23:57:50Z | capabilities__token-intelligence.json |
| https://www.faros.ai/platform/context-engineering | capabilities | 2026-06-26T23:57:50Z | capabilities__context-engineering.json |
| https://www.faros.ai/platform/ai-transformation | capabilities | 2026-06-26T23:57:50Z | capabilities__ai-transformation.json |
| https://www.faros.ai/platform/delivery-excellence | capabilities | 2026-06-26T23:57:50Z | capabilities__delivery-excellence.json |
| https://www.faros.ai/platform/engineering-efficiency | capabilities | 2026-06-26T23:57:50Z | capabilities__engineering-efficiency.json |
| https://www.faros.ai/ai-leaders | solutions | 2026-06-26T23:57:50Z | solutions__ai-leaders.json |
| https://www.faros.ai/company | company | 2026-06-26T23:57:50Z | company__about.json |
| https://www.faros.ai/engineering-executives | solutions | 2026-06-27T00:34:17Z | solutions__engineering-executives.json |
| https://www.faros.ai/platform-engineering-devex-leaders | solutions | 2026-06-27T00:34:17Z | solutions__devex-platform-leaders.json |
| https://www.faros.ai/program-managers | solutions | 2026-06-27T00:34:17Z | solutions__program-managers.json |
| https://www.faros.ai/platform/ai-transformation/gains | capabilities | 2026-06-27T00:34:17Z | capabilities__gains.json |
| https://www.faros.ai/ai-impact | solutions | 2026-06-27T00:34:17Z | solutions__ai-impact-roi.json |
| https://www.faros.ai/dora-metrics | solutions | 2026-06-27T00:34:17Z | solutions__dora-metrics.json |
| https://www.faros.ai/initiative-tracking | solutions | 2026-06-27T00:34:17Z | solutions__initiative-tracking.json |
| https://www.faros.ai/software-capitalization | solutions | 2026-06-27T00:34:17Z | solutions__software-capitalization.json |
| https://www.faros.ai/developer-experience | solutions | 2026-06-27T00:34:17Z | solutions__developer-experience.json |

## Notes
- Batch 1 fetched via Cowork (`mcp__workspace__web_fetch`) on 2026-06-26. 9 pages.
- Batch 2 fetched via **Claude-in-Chrome** (`navigate` + `get_page_text`) on 2026-06-27. 9 pages — the remaining Solutions surfaces: 3 role pages (engineering-executives, devex/platform-engineering, program-managers), the GAINS framework page, and 5 use-case pages (ai-impact, dora-metrics, initiative-tracking, software-capitalization, developer-experience). These are client-rendered for some sections, so Chrome (JS-rendered DOM) was used per the request. 18 pages total.
- `https://www.faros.ai/solutions` returned **empty** — the site has no `/solutions` index page. Solutions are reachable only via role pages (`/ai-leaders`, `/engineering-executives`, `/platform-engineering-devex-leaders`, `/program-managers`) and use-case pages (`/dora-metrics`, `/initiative-tracking`, `/software-capitalization`, etc.). `/ai-leaders` fetched as the representative solution surface (best match to persona:maya). **needs Chrome:** none — all targeted pages rendered server-side and returned full content via WebFetch.
- `_example.json` removed — real fetches have landed (per its own note).
- Page FAQ/LLM-optimization blocks (last updated 12/12/2025 per pages) are SEO content; competitor comparisons and the "$29/contributor/module/month" price are marketing claims captured as-stated, not endorsed.
