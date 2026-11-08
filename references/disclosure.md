# PoisonLens — Development Disclosure

Prepared for the UGREEN Hackathon 2026 on AI NAS, Open Innovation track, in line with the Round 1 disclosure requirements.

## Principal functionality developed for this Hackathon

- The document trust investigation workflow: scope confirmation, discovery, extraction, candidate identification, contextual classification, risk assignment, and evidence-based reporting.
- The six-category threat taxonomy (Role Spoofing, Instruction Override, Data Exfiltration, Tool Hijacking, Answer Contamination, Authority Forgery).
- The context check that separates documents that discuss manipulation from documents that attempt it, including the rule that labels, quotation marks, and code fences never lower risk on their own.
- Obfuscation checks for encoded or hidden instructions, and per-file isolation so that one document can never lower another's risk level.
- Detection of instructions aimed at the audit itself, so that a document cannot lower its own risk level.
- Evidence rules: minimal quotation, credential redaction, the Unverified status, and the prohibition on fabricated excerpts, locations, or tool results.
- Batched extraction that carries findings rather than document text between batches, so a large scope cannot silently drop files.
- The validation scenarios in SKILL.md and the calibration pairs in references/calibration.md.

All of the above was newly developed during the Hackathon period.

## Third-party components and open source libraries

None. The package contains only Markdown files. It bundles no scripts, executables, libraries, datasets, or model weights.

## Platform dependencies

The skill relies solely on the expert agents and CLI capabilities provided by UGOS and Uliya on UGREEN AI NAS (file, document, and knowledge), as documented in the official UGOS Skill Creation Tool. The language model used for analysis is whichever model the user's Uliya environment provides; the skill does not assume or require a specific model and makes no external network requests.

## AI tools used and their principal uses

- OpenAI ChatGPT: drafting and reviewing the initial concept, threat taxonomy, and validation scenarios; competitor analysis.
- Anthropic Claude: drafting, consolidating, and reviewing the SKILL.md instructions, README, and this disclosure; checking the package against the published submission requirements.

Design decisions, scope, and final wording were made by the entrant.
