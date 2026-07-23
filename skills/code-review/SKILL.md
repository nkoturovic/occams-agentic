---
name: code-review
description: Adversarial code-review loop; an independent fresh-context reviewer (sub-agent, second model, or human) tries to refute a change's correctness, classifies findings as MUST-FIX / SHOULD-FIX / NIT, all findings go back to the original author to address, and review repeats until an explicit clean verdict — only then commit or merge. Use when the user says "review this", "code review", "check this diff/PR/branch", when you or a sub-agent have just finished implementing a change, or before committing/merging any non-trivial work. Do not use for architecture or design consultation with no concrete diff to judge, nor for pure formatting/lint passes.
---

# Code Review

Adversarial author/reviewer loop. The reviewer's job is to **refute** the change — hunt
for reasons it is wrong — not to annotate style. The author's job is to answer every
finding. Nothing merges before an explicit clean verdict. You may orchestrate the whole
loop or sit in one seat; the invariants below hold either way.

## Roles

- **Author** — whoever produced the change (often a sub-agent). Owns every fix; only the
  author edits the code under review.
- **Reviewer** — a fresh, independent context: spawn a sub-agent, use a second model, or
  ask a human. Must not share the author's conversation state — anchoring on the
  author's reasoning defeats the review.

## The loop

For multi-round reviews, seed the rounds as todos and end with a re-orientation todo
(re-orient, plan follow-up).

1. **Pin the diff.** Establish exactly what is under review — uncommitted work
   (`git diff`), last commit (`git diff HEAD~1`), or branch (`git diff <base>...HEAD`) —
   plus the stated intent / acceptance criteria.
2. **Spawn the reviewer** with the diff, the intent, and read access to the codebase for
   surrounding context. Do not pass the author's reasoning or self-assessment.
3. **Reviewer reviews adversarially** (attack surface and severity below) and ends the
   round with an explicit verdict.
4. **Route ALL findings back to the same author.** The reviewer never fixes code;
   whoever orchestrates never fixes silently or drops a finding. The author answers each
   one: fix it, or rebut it in writing.
5. **Re-review.** Send the updated diff plus the author's rebuttals back to the reviewer
   — same reviewer context where possible, so rebuttals are judged against the original
   findings. New findings enter the same loop.
6. **Iterate until the verdict is clean.** Only then commit/merge, following the
   project's commit policy; no AI-attribution trailers.

## Attack surface (reviewer)

Try to construct a concrete failure, not a vague concern:

- **Correctness:** logic errors, off-by-one, null/None handling, unhandled edge cases
  and error paths, races/ordering, wrong assumptions about inputs or state.
- **Claims vs reality:** does the change do what the task or commit message says? Do the
  tests exercise the new behavior, or only happy paths?
- **Security:** injection, missing auth checks, secrets in code or logs, unsafe
  defaults, data exposure.
- **Performance:** N+1 access, unbounded loops or allocation, blocking calls on hot
  paths.
- **Maintainability:** duplication, misleading names, dead code — usually SHOULD-FIX or
  NIT.

Report only findings you can defend with evidence (`file:line` plus how it fails).
Phrase genuine uncertainty as a question to the author instead of inflating severity.

## Severity and verdict

Classify every finding:

- **MUST-FIX** — correctness, security, or data-loss defects. Blocks approval.
- **SHOULD-FIX** — real problems that won't break behavior now. Fix, or record
  explicitly why deferred.
- **NIT** — polish. Author's discretion; never blocks.

Each finding: severity, `file:line`, what is wrong, the failure scenario, suggested
direction. End every round with severity counts and exactly one verdict:

- **REVISE** — any MUST-FIX remains, or a SHOULD-FIX is neither fixed nor explicitly
  accepted.
- **APPROVE** — no MUST-FIX; remaining SHOULD-FIX recorded as accepted; NITs optional.

## Single-pass mode

If the user explicitly asks for a "quick review", run steps 1–3 once, report MUST-FIX
and SHOULD-FIX only, and state plainly it was a single pass without the fix/re-review
loop.

## Composing with project conventions

Projects may define their own review rituals, gates, and verdict vocabularies in their
project instructions or skills; by AGENTS.md precedence (project layer over framework
layer), those win. Run this loop inside them and keep its invariants regardless:
independent reviewer, all findings back to the author, re-review until clean, no
commit/merge before a clean verdict.
