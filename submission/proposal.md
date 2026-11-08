# PoisonLens — AI Document Trust Investigator

**UGREEN Hackathon 2026 on AI NAS · Open Innovation**

## 1. What the Skill does

PoisonLens audits documents on a UGREEN AI NAS for hidden instructions aimed at AI and reports quoted evidence before the AI uses those documents.

## 2. Target user and problem

Home and small-business users who let Uliya read outside files: vendor proposals, downloaded reports, attachments. Any such file can carry text written for the AI rather than the reader, and an assistant may treat it as a command. Antivirus misses it: no malware, only instructions.

## 3. Solution

An on-demand, read-only Skill that reads each document, separates text addressed to an AI from ordinary content, judges whether it discusses manipulation or attempts it, and reports the quoted passage, location, category, reasoning and recommendation.

## 4. Main user flow

Uliya confirms the scope, lists documents, extracts text, classifies candidates, and rates each file High Risk, Suspicious, Low, No Signal or Not Assessable. The user decides; the report is saved on request.

## 5. Differentiation

Existing shields filter the user's query with keyword rules. PoisonLens audits the documents themselves, in any language, separating a training article quoting an attack from a proposal performing one. Instructions aimed at the audit itself ("declare this file safe") are findings; a document cannot lower its own score. Every verdict carries checkable evidence.

## 6. UGREEN AI NAS features used

File expert: discovery. Document expert: extraction. On-device model through Uliya: analysis. Knowledge expert: saving reports.

## 7. Technical approach

SKILL.md orchestration only; no scripts or services. Required input: a user-authorized folder or files. Permissions: read-only within scope; saving needs confirmation. Model: whichever Uliya provides. The Skill makes no external calls; whether the platform keeps all processing on-device is for Round 2 to confirm. Security rules override document text: content, file names and metadata are data; unreadable files are Not Assessable, never clean; unmatched excerpts are Unverified.

## 8. Status

Built: SKILL.md (workflow, taxonomy, risk levels, report format, failure handling), README, disclosure, 12-file test corpus. Exercised locally in Claude Code: all twelve verdicts matched the key, covering labeled-example, base64, zero-width, image-only and cross-document cases. This tests the instructions, not the NAS model. Not built: automatic scanning; interception before other AI features read documents. To test on a NAS: batch capacity, page references after extraction, detection on Indonesian and obfuscated text.

## 9. Test plan as a Finalist

Core 1: a proposal with an embedded exfiltration instruction returns High Risk, instruction not followed, passage quoted. Core 2: a training article quoting "ignore all previous instructions" returns Low, context explained. Edge: a meeting note containing, in Indonesian, an instruction to declare itself safe returns High Risk, level not lowered.

## 10. Limits, risks, dependencies

Analysis covers only extracted text; images, comments and metadata may be missed. Model judgment can err; results are indicators, not certification. Runs on demand, not a firewall. Dependencies: UGOS experts and the Uliya model.

---

*Third-party components: none. AI tools disclosed in references/disclosure.md.*
