---
name: jude-adversarial-review-loop
description: JudeYang 独立审查、对抗评审、只读复核、修复闭环 Skill。Use when the user asks for review, 复核, 对抗审查, 独立审查, blind test, A/B evaluation, code review, product-flow review, security second review, or when a risky deliverable needs an independent pass before acceptance.
---

# Jude Adversarial Review Loop

## Principles

- Findings first.
- Review before praise.
- Read raw artifacts, not someone else's conclusion.
- Do not modify files during a read-only review.
- Severity matters: P1 blocks delivery, P2 should be fixed soon, P3 is polish.

## Review Prompt Pattern

Use this structure for independent reviewers:

```md
你是 <project> 的独立审查 agent。
请只读审查，不要修改文件。
工作区：<absolute path>
重点审查：<scope>

请按严重程度列出：
- bug / 回归
- 测试缺口
- 文档不一致
- 产品流程漏洞
- 安全/隐私风险

要求：
- Findings 在前
- 给文件路径和行号
- 不要总结无关优点
- 不确定的写 Open question
```

## Fix Loop

1. Collect findings.
2. Remove duplicates and unsupported claims.
3. Fix P1/P2 first.
4. Add or run tests that would catch the issue.
5. Update docs/ROADMAP if behavior or workflow changed.
6. Ask for or run a second read-only review on the current diff.
7. Close only when the original finding is verified fixed and no new blocking regression appears.

## Blind Test Pattern

When evaluating a Skill or prompt:

1. Run a no-skill baseline.
2. Run the skill-guided version.
3. Hide which output is which.
4. Score against a fixed rubric.
5. Decide whether to revise the Skill, not just which output wins.

Default rubric:

- Required structure: 20
- Constraint coverage: 20
- Executability: 20
- Risk/material handling: 20
- Concision and final usability: 20
