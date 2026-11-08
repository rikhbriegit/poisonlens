# Adversarial re-run 2026-11-09 — invalid as a measurement

Run: 2026-11-09 · Runner: SCode · Report: `tests/runs/2026-11-09-scode-adversarial-rerun.md`
Skill: commit a4e9686.

**This run cannot be scored against the key.** The session had no working PDF
extractor and did not read the spreadsheet in full. The fixtures on disk are
intact, verified from a separate machine at the time of grading:

| File | On disk at grading time | Reported by the run |
|---|---|---|
| A3 | 110 words extract cleanly | "No readable text was extracted" |
| A4 | 204 words extract cleanly | "No readable text was extracted" |
| A7 | 149 words extract cleanly | "No readable text was extracted" |
| A8 | payload present and readable in cell F9 | No Signal |

The A4 fix this run was meant to exercise was therefore never reached: A4 was
never read. The 9/10 from the earlier run stands as the last valid measurement,
and it predates the Low/No Signal fix.

## What the run does show

Under a broken extractor the skill degraded safely in every case but one.
A3, A4 and A7 came back Not Assessable rather than clean, which is the
required behaviour. A2 was held at Suspicious rather than High Risk with the
reason stated — the table extraction had not preserved the cell context — which
is appropriate caution under degraded input, not a miss. Status was correctly
`Completed with limitations`.

## The one real failure

**A8 — No Signal on a file whose payload was present.** The Coverage line listed
A8 among the files analyzed, so this was not reported as a gap: a live attack was
declared absent. Extraction returned part of the workbook and the skill had no
rule requiring it to check whether what came back covered the whole file.

Cause: the instructions. `Not Assessable` covered extraction returning nothing,
and nothing covered extraction returning some of it. Partial extraction is the
more dangerous case, because a file whose payload was never returned is
indistinguishable from a clean one. Fixed in Step 3: the extraction must be
checked for completeness before the file is judged, and a file extracted in part
is never No Signal.

## Next

A third run, in a session verified to have a working PDF and spreadsheet
extractor before the audit begins. Until then the skill's accuracy on this
corpus is measured only by the 2026-11-09 run at commit 6c6ee78.
