# PoisonLens demo

An interactive walkthrough of a recorded PoisonLens blind audit, with the option to
re-run any document live against a model on Ollama Cloud.

## What is real here

- **The documents** are the ten fixtures in `../tests/adversarial/`. Their text is
  extracted at build time by `build_data.py` — nothing is retyped or paraphrased.
- **The recorded verdicts** come from `../tests/runs/2026-11-09-scode-adversarial-run3.md`,
  a blind run: the session that produced them had no access to the expected answers.
  Ten of ten levels matched the key.
- **The live audit** sends the document and the submitted `SKILL.md` to Ollama Cloud
  and shows what comes back, including when it disagrees with the recorded run.

Nothing on the page is a mock-up of a verdict that was never produced.

## Running it

```bash
npm install
cp .env.example .env.local      # then add your Ollama Cloud key
npm run dev                     # http://localhost:3000
```

The key is read server-side in `app/api/audit/route.js` and never reaches the browser.
Without a key the page still works; only the "Run it now" panel reports that the key
is missing.

## Choosing a model

Uliya runs **on the NAS**. The iDX6011 Pro has 96 TOPS and 64 GB, so the model it
serves is a small one. None of the Ollama Cloud models is that model, but they are not
equally far from it:

| Model | Why |
|---|---|
| `gpt-oss:20b-cloud` | Default. Smallest in the cloud catalogue, and the only one in a size class a NAS could plausibly host. The honest proxy. |
| `gemma4:31b-cloud` | Still device-plausible at 31B. |
| `deepseek-v4-flash:cloud` | Frontier scale. A pass here says little about the NAS. |
| `glm-5.1:cloud` | Frontier scale, same caveat. (`glm-4.6` was retired in June 2026.) |

A verdict from a frontier model proves the instructions are unambiguous. A verdict from
a 20B model is the one that suggests the skill will hold up on the device — and that is
still a proxy, not the device.

## Rebuilding the data

```bash
python3 build_data.py           # regenerates data/audit.json from the corpus and the run report
cp ../SKILL.md data/SKILL.md    # keep the live audit on the submitted skill
```

## Layout

```
app/
  page.jsx              document picker, text pane, verdict pane
  api/audit/route.js    server-side call to Ollama Cloud
components/
  DocumentText.jsx      highlights the quoted passages and scrolls to the first
  Finding.jsx           the recorded verdict
  LiveAudit.jsx         run-it-now panel
data/
  audit.json            generated — do not edit by hand
  SKILL.md              copy of the submitted skill
```

## A note on what this page does

It feeds attacker-written documents to a language model on purpose. The route wraps
each document in explicit markers and states that nothing inside carries authority,
which is the same discipline the skill itself requires. The model is asked only to
classify; it is given no tools, no file access and no network.
