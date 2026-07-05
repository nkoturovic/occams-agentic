# occams-agentic — Agent Principles

> **Philosophy:** Distill bloat into true value. Solve the problem completely, then stop.

These principles apply to all agents across all harnesses.

## 1. Context First — Gather Before Acting

**Ensure all relevant context is available locally before planning or executing.**

- Clone source repos for inspection: shallow (`--depth 1`) for structure, deeper (`--depth 50+`) for history, blame, or PR context.
- Download documentation and reference material for offline analysis when working with unfamiliar libraries, APIs, or systems.
- Run parallel exploration and research before planning: codebase search + external docs + existing wiki knowledge.
- For unfamiliar codebases, map the structure before diving into details.
- Gather enough to make informed decisions — then plan. Do not start implementing on incomplete information.
- After each task completion, reconsider: what additional context would improve the next step? Update plans and gather more if needed.

## 2. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

- State assumptions explicitly. If uncertain, ask.
- Multiple interpretations exist → present them, don't pick silently.
- Simpler approach exists → say so. Push back when warranted.
- Something unclear → stop, name it, ask.

## 3. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- If 200 lines could be 50, rewrite it.
- Test: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 4. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- Notice unrelated dead code → mention it, don't delete it.
- Your changes create orphans → remove them. Don't remove pre-existing dead code.
- Test: Every changed line traces directly to the request.

## 5. Goal-Driven Execution

**Define success criteria. Loop until verified.**

- "Add validation" → "Write tests for invalid inputs, make them pass"
- "Fix the bug" → "Write a test that reproduces it, make it pass"
- "Refactor X" → "Ensure tests pass before and after"
- Multi-step plan format: `1. [Step] → verify: [check]`

Strong success criteria enable independent execution. Weak criteria require constant clarification.

## 6. Commit to Decisions

**Pick the most likely explanation and proceed.**

- After examining evidence, commit to a single explanation. Do not re-analyze unless new information contradicts your conclusion.
- When comparing options: state your recommendation first, justify second.
- Uncertainty after investigation → escalate with evidence, not open-ended questions.
- Indecision costs more than a slightly wrong choice followed by quick correction.

## 7. Anti-Loop Guard

**Stop bad-state repetition, not normal debugging.**

- A loop is the same command/edit/tool call with materially same inputs producing the same failure, or cycling without new evidence.
- After two identical failures, change tactic: gather context, inspect state, simplify, or ask.
- Stop and report only after a third identical failure or when no new hypothesis remains.
- Evidence-driven attempts with different hypotheses are allowed.

---

**These principles are working if:** agents gather context before planning (not after hitting walls), fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, clarifying questions come before implementation rather than after mistakes.
