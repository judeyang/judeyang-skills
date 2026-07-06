---
name: jude-workflow-to-skill-factory
description: Convert JudeYang's repeated prompts, delivery procedures, rubrics, and project workflows into concise reusable Codex Skills. Use when the user asks to create/update Skills, extract workflows from history, reduce repeated prompting, formalize a process, build test prompts, run blind evaluations, or improve self-authored skills.
---

# Jude Workflow To Skill Factory

## When To Create A Skill

Create or update a Skill when a workflow has:

- repeated prompts or rubrics
- fixed file formats or output schemas
- fragile steps that Codex often forgets
- reusable domain rules
- validation commands or blind-test examples
- multiple handoff roles or sub-agent prompts

Do not create a Skill for one-off advice.

## Source Of Truth

For JudeYang self-authored skills, develop in:

`/Users/yanglin/同步空间/Codex/Skills进化/judeyang-skills`

Do not treat `~/.codex/skills` installed copies as the primary development source.

## Skill Design Workflow

1. Collect 3-5 real user prompts from history or current examples.
2. Identify repeated constraints, output formats, and failure modes.
3. Decide what belongs in `SKILL.md`, `references/`, `scripts/`, and `assets/`.
4. Keep `SKILL.md` short and trigger-focused.
5. Put long domain rules in one-level `references/`.
6. Put deterministic repeated operations in `scripts/`.
7. Add `test-prompts.json` or clear regression prompts when useful.
8. Validate with a no-skill baseline and a skill-guided blind test.
9. Remove generated caches such as `__pycache__` before committing.

## SKILL.md Shape

Use only:

```yaml
---
name: short-hyphen-name
description: What it does and exact trigger contexts.
---
```

The body should contain:

- core principles
- workflow steps
- resource routing
- validation expectations
- refusal/stop conditions if relevant

Avoid README-style installation notes inside the Skill unless the Skill itself needs them at runtime.

## Quality Gate

Before calling a Skill ready:

- trigger description is specific
- body is under 500 lines
- no duplicated long reference material
- examples cover common and edge cases
- validation command or evaluation rubric exists
- no secrets, user private data, or generated caches are included
