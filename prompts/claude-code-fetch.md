# Prompt — Claude Code · fetch faros.ai pages

Use your WebFetch tool. Goal: pull the pages in `fetch/targets.json` and write normalized JSON.

For each target (do the `primary` list first, then `secondary`):
1. Fetch the URL. Follow obvious in-page nav under Platform / Capabilities / Solutions to find real
   sub-pages, and add any you discover.
2. Write `fetch/raw/<tab>__<slug>.json` conforming to `schemas/faros-page.schema.json`: hero
   headline/subhead/CTA, ordered sections (heading + paraphrased body + bullets), `named_capabilities`,
   `named_solutions`, `stats` (e.g. "10x", "100+"), customer logos, links worth following.
3. Keep verbatim quotes UNDER 15 words; paraphrase everything else. Record honest `notes` (gated,
   ambiguous, judgment calls). Set `retrieved_at` to the real fetch time.
4. Append one line per page to `fetch/raw/_manifest.md`.

Then validate shapes:
`python3 -c "import json,glob,jsonschema; s=json.load(open('schemas/faros-page.schema.json')); [jsonschema.validate(json.load(open(f)),s) for f in glob.glob('fetch/raw/*.json') if not f.endswith('_example.json')]; print('all fetch/raw JSON valid')"`

Do NOT edit the knowledge tree — that's the curator's job. Commit the raw JSON when done.
