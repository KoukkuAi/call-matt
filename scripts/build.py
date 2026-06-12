#!/usr/bin/env python3
"""Build all agent-specific SKILL.md ports from src/SKILL.base.md.

Single source of truth: edit src/SKILL.base.md (shared content) or the
AGENTS config below (per-agent differences), then run:

    python3 scripts/build.py

Outputs:
    skills/call-matt/SKILL.md                          (Claude Code)
    antigravity/.agents/skills/call-matt/SKILL.md      (Google Antigravity)
    codex/skills/call-matt/SKILL.md                    (OpenAI Codex)
    hermes/skills/call-matt/SKILL.md                   (Hermes Agent)

The script validates every generated file and exits non-zero on failure.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "src", "SKILL.base.md")

REAL_SKILLS = [
    "diagnose", "grill-with-docs", "triage", "improve-codebase-architecture",
    "setup-matt-pocock-skills", "tdd", "to-issues", "to-prd", "zoom-out",
    "prototype", "caveman", "grill-me", "handoff", "write-a-skill",
    "git-guardrails-claude-code", "setup-pre-commit", "migrate-to-shoehorn",
    "scaffold-exercises",
]

GUARDRAILS_NA = (
    "NOT APPLICABLE here — it installs hooks specific to another agent "
    "(Claude Code) and won't work in {agent}. If the user wants git safety, {alt}"
)
RULE11_NA = (
    "don't route to `/git-guardrails-claude-code` (it's for another agent); "
    "instead {alt}"
)

AGENTS = {
    "claude-code": {
        "out": "skills/call-matt/SKILL.md",
        "EXTRA_FRONTMATTER": "",
        "HEADER": "# /call-matt — Skill Router & Strategic Coach",
        "GUARDRAILS_ROW": "The user worries the agent will run a destructive git command (push, `reset --hard`, `clean`); installs Claude Code hooks to block them.",
        "RULE1": "Tell them to run `npx skills@latest add mattpocock/skills`, then `/setup-matt-pocock-skills`.",
        "RULE11": "`/git-guardrails-claude-code`.",
        "NEXT_ACTION": "Trigger the recommended skill. In Claude Code, if the target skill is installed, invoke it directly (e.g. via the Skill tool) and carry the user's original context into it — don't make them re-explain. If it's not installed, give the exact install command (`npx skills@latest add mattpocock/skills`) and the one input they should prepare. When the situation is ambiguous between two skills, ask one sharp question instead of invoking.",
        "SETUP_SECTION": "",
    },
    "antigravity": {
        "out": "antigravity/.agents/skills/call-matt/SKILL.md",
        "EXTRA_FRONTMATTER": "",
        "HEADER": "# call-matt — Skill Router & Strategic Coach\n\n> Invoke explicitly with the `/call-matt` workflow (shipped alongside this skill in `.agents/workflows/`), or just describe being stuck — Antigravity loads this skill implicitly when the task matches its description.",
        "GUARDRAILS_ROW": GUARDRAILS_NA.format(agent="Antigravity", alt="suggest an always-on Antigravity Rule in `.agents/rules/` forbidding destructive git commands instead."),
        "RULE1": "Point them to Setup below, then `/setup-matt-pocock-skills`.",
        "RULE11": RULE11_NA.format(alt="offer to write an always-on Rule in `.agents/rules/` that forbids destructive git commands."),
        "NEXT_ACTION": "Trigger the recommended skill. In Antigravity, if the target skill exists under `.agents/skills/`, load and apply its SKILL.md instructions immediately, carrying the user's original context into it — don't make them re-explain. If it's not installed, give the exact install step (see Setup below) and the one input they should prepare. When the situation is ambiguous between two skills, ask one sharp question instead of invoking.",
        "SETUP_SECTION": """
## Setup (Antigravity)

The routed skills must exist in this workspace for direct invocation to work:

1. Run `npx skills@latest add mattpocock/skills` and select Antigravity as the target agent if offered. If the installer doesn't list Antigravity, clone the repo and copy each folder from its `skills/engineering/` and `skills/productivity/` directories into this workspace's `.agents/skills/`.
2. Run `/setup-matt-pocock-skills` once per repo to configure the issue tracker, triage labels, and docs location the other skills consume.
3. Antigravity loads skills on demand when a task matches their description; this router works by explicitly loading the target skill's SKILL.md after routing.""",
    },
    "codex": {
        "out": "codex/skills/call-matt/SKILL.md",
        "EXTRA_FRONTMATTER": "allow_implicit_invocation: true\n",
        "HEADER": "# call-matt — Skill Router & Strategic Coach\n\n> In Codex, invoke this explicitly with `$call-matt` (or pick it from `/skills`), or just describe being stuck — it triggers implicitly when the task matches. Skill names are written with a leading `/` below for cross-agent readability; in Codex they're invoked as `$skill-name`.",
        "GUARDRAILS_ROW": GUARDRAILS_NA.format(agent="Codex", alt="point them to Codex's own sandbox/approval modes (avoid `danger-full-access`) and AGENTS.md rules instead."),
        "RULE1": "Point them to Setup below, then `$setup-matt-pocock-skills`.",
        "RULE11": RULE11_NA.format(alt="point to Codex's sandbox and approval modes, plus a rule in AGENTS.md forbidding destructive git commands."),
        "NEXT_ACTION": "Trigger the recommended skill. In Codex, if the target skill is installed, load and apply its instructions immediately (the user can also invoke it as `$skill-name`), carrying their original context into it — don't make them re-explain. If it's not installed, give the exact install step (see Setup below) and the one input they should prepare. When the situation is ambiguous between two skills, ask one sharp question instead of invoking.",
        "SETUP_SECTION": """
## Setup (Codex)

The routed skills must be installed for direct invocation to work:

1. Run `npx skills@latest add mattpocock/skills` and select Codex as the target agent if offered. Alternatively, ask Codex's skill installer to download skills from `github.com/mattpocock/skills`, or copy each skill folder into `~/.codex/skills/`. Codex detects newly installed skills automatically; restart Codex if one doesn't appear.
2. Run `$setup-matt-pocock-skills` once per repo to configure the issue tracker, triage labels, and docs location the other skills consume.
3. Skills are referenced here with a leading `/` for readability, but in Codex they're invoked as `$skill-name` or picked from the `/skills` menu.""",
    },
    "hermes": {
        "out": "hermes/skills/call-matt/SKILL.md",
        "EXTRA_FRONTMATTER": "version: 1.0.0\nauthor: KoukkuAi (unofficial community port; underlying skills by Matt Pocock)\nlicense: MIT\ntags: [router, orchestrator, coding-workflow, matt-pocock, meta-skill]\n",
        "HEADER": "# call-matt — Skill Router & Strategic Coach\n\n> In Hermes, there are no slash commands for skills: this loads automatically when the request matches its description, or on demand when the user says something like \"use the call-matt skill\" or just \"call matt\". Skill names are written with a leading `/` below for cross-agent readability — in Hermes, invoke them by name (\"use the tdd skill\").",
        "GUARDRAILS_ROW": GUARDRAILS_NA.format(agent="Hermes", alt="offer to add a standing instruction to their Hermes config/memory forbidding destructive git commands instead."),
        "RULE1": "Point them to Setup below, then have them run the setup-matt-pocock-skills skill.",
        "RULE11": RULE11_NA.format(alt="offer a standing instruction in Hermes config/memory forbidding destructive git commands."),
        "NEXT_ACTION": "Trigger the recommended skill. In Hermes, if the target skill exists under the skills directory, view it (skill_view) and apply its instructions immediately, carrying the user's original context into it — don't make them re-explain. If it's not installed, give the exact install step (see Setup below) and the one input they should prepare. When the situation is ambiguous between two skills, ask one sharp question instead of invoking.",
        "SETUP_SECTION": """
## Setup (Hermes)

The routed skills must exist in the Hermes skills directory for direct invocation to work:

1. Clone `github.com/mattpocock/skills` and copy each folder from its `skills/engineering/` and `skills/productivity/` directories into `~/.hermes/skills/` (a category subfolder like `~/.hermes/skills/matt-pocock/` keeps the list tidy — Hermes expects SKILL.md at the leaf). Hermes auto-discovers skills on startup; restart if one doesn't appear.
2. Run the setup skill once per repo ("use the setup-matt-pocock-skills skill") to configure the issue tracker, triage labels, and docs location the other skills consume.
3. Cross-agent note: these skills were written for coding agents and use plain markdown, so they work in Hermes without modification; any agent-specific frontmatter fields are simply ignored.""",
    },
}


def build(agent: str, cfg: dict, base: str) -> str:
    text = base
    for key in ("EXTRA_FRONTMATTER", "HEADER", "GUARDRAILS_ROW", "RULE1", "RULE11", "NEXT_ACTION", "SETUP_SECTION"):
        text = text.replace("{{%s}}" % key, cfg[key])
    return text


def validate(agent: str, text: str) -> list:
    errors = []
    try:
        import yaml
        fm = yaml.safe_load(text.split("---")[1])
        if not re.fullmatch(r"[a-z0-9-]{1,64}", fm.get("name", "")):
            errors.append("invalid name")
        if not (0 < len(fm.get("description", "")) <= 1024):
            errors.append("invalid description length")
    except Exception as e:
        errors.append(f"frontmatter parse error: {e}")
    if "{{" in text:
        errors.append("unfilled placeholder: " + ",".join(set(re.findall(r"\{\{\w+\}\}", text))))
    for s in REAL_SKILLS:
        if "/" + s not in text:
            errors.append(f"missing skill reference: {s}")
    for sec in ("Coaching Voice", "The Toolkit", "Routing Logic", "Response Format", "Edge Cases"):
        if sec not in text:
            errors.append(f"missing section: {sec}")
    routing = text.split("## Routing Logic")[1].split("## Response Format")[0]
    n = len(re.findall(r"^\d+\. \*\*", routing, re.M))
    if n != 12:
        errors.append(f"expected 12 routing rules, found {n}")
    if agent != "claude-code":
        if "NOT APPLICABLE" not in text:
            errors.append("git-guardrails must be NOT APPLICABLE")
        if "Skill tool" in text:
            errors.append("leftover Claude Code Skill-tool reference")
        if f"Setup (" not in text:
            errors.append("missing Setup section")
    return errors


def main():
    base = open(BASE).read()
    failed = False
    for agent, cfg in AGENTS.items():
        text = build(agent, cfg, base)
        errors = validate(agent, text)
        out = os.path.join(ROOT, cfg["out"])
        if errors:
            failed = True
            print(f"✗ {agent}: " + "; ".join(errors))
            continue
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w") as f:
            f.write(text if text.endswith("\n") else text + "\n")
        print(f"✓ {agent} → {cfg['out']} ({len(text.splitlines())} lines)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
