---
name: jude-project-operator
description: Auto-use for JudeYang project work: entering a project, continuing prior work, modifying code/docs/config, fixing bugs, building tools/products, organizing knowledge projects, migrating files, checking Git status, updating ROADMAP/docs, validating delivery, or avoiding project/path mix-ups and red-line actions. Trigger on Chinese prompts such as 继续, 修一下, 做完, 迁移项目, 整理项目, 更新文档, 跑验证, 看看这个项目.
---

# Jude Project Operator

## Core Rule

Treat the user as product owner. Deliver a verified project outcome, not just code or advice.

## Entry Checklist

1. Read `/Users/yanglin/.codex/PROJECTS.md` first if it exists.
2. Identify the current project, real path, project status, and anti-mix-up warning.
3. Read project `AGENTS.md`, `CLAUDE.md`, `codex.md`, `README.md`, `ROADMAP.md`, and relevant `docs/` files.
4. Run `git status --short --branch` if inside a Git repository. If not, state that this is not a Git repository.
5. Identify entry files, run/build/test commands, and files or systems that must not be touched.

## Red Lines

Stop and ask before:

- deleting files or directories
- git reset, restore, checkout overwrite, rebase, merge, push, force push
- editing `.env`, secrets, tokens, CI/CD, system config, global dependencies
- database schema changes, migrations, destructive data changes
- production deploy, public release, npm publish, posting articles
- disabling auth, permission checks, payment callbacks, signatures, CSRF, or validation

## Change Workflow

1. Convert the request into a verifiable goal.
2. Search existing implementation and references before editing.
3. Keep changes scoped to the request.
4. Match local style and naming.
5. Avoid opportunistic refactors and unrelated formatting.
6. Run the project verification commands.
7. Update docs and `ROADMAP.md` when behavior, interfaces, data, deployment, directories, or business rules changed.
8. Run `git status --short --branch` again.

## Final Response

For substantial project work, answer with:

```md
## 完成内容
- ...

## 验证结果
- ...

## 影响范围
- ...

## 未验证 / 风险
- ...
```

If there are uncommitted changes, include:

- current uncommitted scope
- whether a commit is recommended
- suggested English commit message
- copyable `git add -A` and `git commit -m "..."` commands
