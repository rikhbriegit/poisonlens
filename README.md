# PoisonLens — AI Document Trust Investigator

*Don't let your files become your AI's instructions.*

## Who it is for

Anyone who lets the AI on their UGREEN NAS read documents that came from somewhere else: vendor proposals, downloaded reports, shared contracts, email attachments. Some of those files may carry hidden text written for the AI rather than for you, telling it to ignore its task, leak information, or reach into other folders. PoisonLens finds that text, shows you the evidence, and lets you decide.

## How to use it

Ask Uliya in plain language, for example:

- "PoisonLens, audit the Project Documents folder before I summarize it."
- "Check this PDF for prompt injection."
- "Is the Vendor Proposals folder safe to use with AI?"

PoisonLens will confirm the scope, read the documents, and return a report. Each flagged file shows the quoted passage, where it was found, what kind of manipulation it looks like, why, and the strongest innocent explanation. Files are rated High Risk, Suspicious, Low, No Signal, or Not Assessable.

You can ask for the report in another language, or ask PoisonLens to save it. It will confirm where before saving.

## What it does not do

- It does not detect malware or ransomware.
- It does not block, move, quarantine, or delete files. It is read-only.
- It does not run automatically on new files or intercept other AI features. It runs when you ask.
- It cannot read what the NAS cannot extract: scanned images without text, encrypted files, or content hidden in images and metadata. Those files are reported as Not Assessable, never as clean.
- It does not certify a file as safe. "No Signal" means nothing was found in the text that was analyzed.

## Package contents

The uploadable skill package contains only what the UGOS checker allows:

```
poisonlens/
├── SKILL.md                  Skill instructions
└── references/
    ├── calibration.md        Calibration pairs for classification judgment
    └── disclosure.md         Original work, third-party components, AI tools used
```

Build it with `sh scripts/build-package.sh` (or `powershell -File scripts/build-package.ps1` on Windows, where `sh` is absent), which copies the two allowed
items into `dist/poisonlens/` and zips them as `dist/poisonlens.zip`.
Validate with the official UGOS checker before upload.

This README, `submission/`, and `scripts/` stay in the repository but are
not part of the uploaded skill package.

Developed for the UGREEN Hackathon 2026 on AI NAS, Open Innovation track. See `references/disclosure.md` for the full disclosure.
