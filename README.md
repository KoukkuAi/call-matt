# /call-matt

**An unofficial orchestrator skill for [Matt Pocock's agent skills](https://github.com/mattpocock/skills).**

> ⚠️ **Not affiliated with or endorsed by Matt Pocock.** This is a community-built router for his MIT-licensed skill toolkit. All credit for the underlying skills goes to [@mattpocockuk](https://x.com/mattpocockuk) — check out [Total TypeScript](https://www.totaltypescript.com), [AI Hero](https://www.aihero.dev), and [mattpocock.com](https://www.mattpocock.com).

## The problem

Matt's toolkit has ~18 excellent skills — `/grill-with-docs`, `/tdd`, `/to-issues`, `/diagnose`, `/caveman` and more. They're small and composable by design. But that means *you* have to know which one fits your current situation.

## The fix

`/call-matt` is a meta-skill that acts as a **router and strategic coach**. Describe where you are ("I have a vague idea", "my backlog is chaos", "this bug makes no sense", "my context window is melting") and it:

1. **Reads** your situation in 1–3 punchy sentences
2. **Picks the playbook** — the exact skill (or sequence) to run right now, and why
3. **Gives you the next action** — triggers the skill or hands you the command

It knows the healthy lifecycle (*grill → PRD → issues → prototype → tdd → improve-architecture*) and will tell you when you're skipping a stage.

## Install

```bash
# 1. Install Matt's actual skills (the things being routed to)
npx skills@latest add mattpocock/skills

# 2. Add this router
npx skills@latest add KoukkuAi/call-matt
# or copy skills/call-matt/ into .claude/skills/ (per project)
# or into ~/.claude/skills/ (available in every project)

# 3. In a new repo, run his setup first
/setup-matt-pocock-skills
```

## Usage

```
/call-matt I have a rough idea for a CLI tool but no real plan yet
```

> **Read:** You're at step zero — an idea without resolved decisions. Building now means rebuilding later.
> **The Playbook:** `/grill-with-docs`. It interviews you until the plan holds up, and writes the decisions into CONTEXT.md so every future session benefits.
> **Next Action:** Run `/grill-with-docs` and bring your one-paragraph pitch. Expect to get grilled.

## What it routes to

| Situation | Skill |
|---|---|
| Vague idea or plan | `/grill-with-docs` · `/grill-me` |
| Plan → roadmap | `/to-prd` → `/to-issues` |
| Messy backlog | `/triage` |
| Design uncertainty | `/prototype` |
| Building / fixing | `/tdd` |
| Mystery bug | `/diagnose` |
| Ball of mud | `/improve-codebase-architecture` |
| Lost in code | `/zoom-out` |
| Bloated context | `/handoff` · `/caveman` |
| New skill needed | `/write-a-skill` |
| Git safety | `/git-guardrails-claude-code` |
| Commit-time checks | `/setup-pre-commit` |

## A note on identity

This router deliberately does **not** impersonate Matt Pocock. It coaches in the spirit of the engineering values his skills document — small steps, fast feedback, no fluff — but it never speaks as him or claims his endorsement.

## License

MIT — see [LICENSE](./LICENSE). The skills it routes to live in [mattpocock/skills](https://github.com/mattpocock/skills), also MIT.
