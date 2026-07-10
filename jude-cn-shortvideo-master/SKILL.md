---
name: jude-cn-shortvideo-master
description: Use when JudeYang turns Chinese fuxi knowledge bases, transcripts, drafts, or reference videos into doctor-IP short-video deliverables for Douyin, Xiaohongshu, Vlog, medical-beauty review, role-specific handoff, manual approval, or final execution files.
---

# Jude 中文短视频主控

## Core Contract

After platform and quantity confirmation, produce exactly three human-facing files under `outputs/final/`:

| File | Reader | Must contain |
|---|---|---|
| `01-<project>-主编操盘手全局总控.md` | 主编/操盘手 | source lock, selection logic, counts, schedule, source evidence, platform decisions, risks, final go/no-go |
| `02-<project>-执行团队拍摄发布脚本.md` | 拍摄/剪辑/运营 | production specs, item-specific shots, props, subtitles, covers, publish-ready platform copy, pre/post-publish checks |
| `03-<project>-余教授本人提词表演稿.md` | 出镜人 | exact spoken lines, performance cues, forbidden wording, professional blockers |

No fourth human entry file. Process logs are created only when the user asks and stay under `outputs/review/` or `outputs/editor/`.

## Role Purity

### 01 主编只看

Keep strategy, source choices, heat evidence, editorial tradeoffs, compliance summary, publishing rhythm, and cross-role approval here.

### 02 执行团队只看

Keep camera, action, props, subtitles, cover, platform fields, naming, delivery, publishing, and data collection here.

Every final `02` must include:

- `## 拍摄与交付规范`
- `## 发布前检查`
- `## 发布后回收`

### 03 余教授只看

Keep only:

- what to say
- how to say it
- what not to say
- what professional wording needs his confirmation

Every final `03` must include `## 不能说`.

Never put these in `03`:

- source links or local paths
- heat numbers
- source-fit or replication scores
- rewrite rationale
- shooting, editing, or publishing instructions
- `结构模型 / 改写口径 / 参考原视频 / 热度依据`

## Statuses

| Status | Meaning |
|---|---|
| `待平台确认` | source read, platform/form not confirmed; do not write final files |
| `待生成数量确认` | platform confirmed, main-video/Vlog counts missing; do not write final files |
| `待人工审查` | three draft files exist; human blockers remain |
| `待修改` | human feedback returned and must be applied |
| `修改完成待确认` | feedback applied; reviewers have not all confirmed |
| `待最终数量确认` | reviewers clear; final counts not reconfirmed |
| `最终执行稿` | blockers clear and final counts explicitly confirmed |

## Required Workflow

### 1. Source Lock

Read project rules and source material. Record:

`来源 / 可用内容 / 待确认事实 / 不可使用内容 / 合规风险`.

Stop when the target person, account, source identity, business goal, or source reliability is unclear. Mark broken machine transcripts `机器转写不可用`; do not invent missing facts.

### 2. Platform Checkpoint

Recommend:

`平台 / 是否建议 / 内容形式 / 理由 / 不建议做什么 / 人工确认点`.

Do not create the three files until the user confirms platforms and formats. Default priority is Douyin and Xiaohongshu; Weibo and WeChat are secondary only when requested.

### 3. Quantity Checkpoint

Ask for exact counts after platform confirmation:

- 主视频脚本多少条？
- Vlog 多少条？

Recommendation is not confirmation. Never infer counts or silently reduce a real project to a sample. Write confirmed counts into all three files.

### 4. Source Relationship Before Drafting

Classify every reference as one of:

- `内容参考`: source subject and claims materially match the new item
- `结构参考`: only hook, rhythm, scene, or CTA mechanism is reused
- `场景参考`: only Vlog setting or visual action is reused

Every item in `02` must include `来源关系`, explicitly separating `内容参考` and `结构参考`.

Do not call a structure-only reference `内容贴合`. Do not claim `100% 贴合/覆盖` unless every item has inspectable evidence. Report content fit and structure coverage separately.

### 5. Draft The Three Files

Create exactly the three canonical role files and mark them `待人工审查`.

Read before drafting:

- `references/transcript-replication-rules.md`
- `references/platform-tone.md`
- `references/compliance-cn-medical-beauty.md` for doctor/medical/beauty content
- `references/delivery-quality-gate.md`

The chief editor should only need `01`, the execution team only `02`, and the speaker only `03`.

### 6. Platform Copy

Douyin and Xiaohongshu are separate finished outputs, not one caption copied twice.

For medical explanatory main videos, Xiaohongshu uses:

`适合谁 / 先看什么 / 面诊前准备 / 避坑 / 收藏点 / 评论引导`.

For non-medical main videos such as content review, filming methods, or data analysis, Xiaohongshu uses:

`适合谁 / 先看什么 / 执行要点 / 避坑 / 收藏点 / 评论引导`.

Do not invent `面诊前准备` merely because the item ID starts with `T`.

For doctor-life or production Vlogs, Xiaohongshu uses:

`适合谁 / 观众能看到什么 / 拍摄观察点 / 隐私边界 / 收藏点 / 评论引导`.

Never force `面诊前准备` into content-review, filming, props, script-writing, or data-review Vlogs.

### 7. Natural Voice Gate

When the user asks for `去 AI 味 / 说人话 / 真人口播`, use `qu-ai-wei` after drafting and then review the raw output again.

Reject the pack when:

- more than half the items use the same CTA opener such as `评论写：`
- Xiaohongshu bodies repeat the same opening or preparation sentence across most items
- Vlog length is padded with repeated conclusions
- every item uses the same sentence rhythm

Category-only comments remain required for medical safety, but wording and interaction mechanism must vary naturally.

### 8. Shootability Gate

Each main video and Vlog needs topic-specific visual actions. A generic menu such as `白板/模型/资料夹/手势任选` is a scaffold, not a final shot.

Reject the pack when a generic visual placeholder appears in more than 25% of items. Closing shots may repeat; explanatory shots may not.

`sync_teleprompter_to_shooting.py` can create a scaffold only. Never deliver its raw generic output as final `02`.

### 9. Mandatory Automated Gates

Run all commands on the actual canonical files:

```bash
python3 scripts/audit_duration.py "outputs/final/03-<project>-余教授本人提词表演稿.md" --format teleprompter
python3 scripts/audit_sensitive_claims.py "outputs/final/01-<project>-主编操盘手全局总控.md" "outputs/final/02-<project>-执行团队拍摄发布脚本.md" "outputs/final/03-<project>-余教授本人提词表演稿.md"
python3 scripts/audit_delivery_quality.py --chief "outputs/final/01-<project>-主编操盘手全局总控.md" --execution "outputs/final/02-<project>-执行团队拍摄发布脚本.md" --speaker "outputs/final/03-<project>-余教授本人提词表演稿.md" --expected-main <N> --expected-vlog <M>
```

Any nonzero exit means the pack is not deliverable. Fix the files and rerun. Do not hide failures in process notes.

### 10. Manual Review Routing

For each blocker include:

`审查项 / 为什么必须人工看 / 谁确认 / 没确认时怎么处理`.

| Owner | File | Typical blockers |
|---|---|---|
| 主编 | `01` | platform choice, source relationship, editorial risk, schedule, final release |
| 执行团队 | `02` | location, props, privacy-safe material, shot feasibility, cover/subtitle/publish operations |
| 余教授 | `03` | professional accuracy, personal wording, oral boundary, forbidden claims |

Medical content stays `待人工审查` until the speaker confirms professional accuracy.

### 11. Adversarial Review

Score the current files, not prior summaries:

- hook
- platform fit
- source fidelity
- compliance
- shootability
- manual-review clarity
- non-AI voice

Below 85/100 means revise and rerun all gates. A score never overrides a deterministic audit failure.

### 12. Feedback And Finalization

When human feedback arrives:

1. mark affected files `待修改`
2. update all dependent sections across `01/02/03`
3. mark them `修改完成待确认`
4. wait for role confirmation
5. ask the user to reconfirm final main-video and Vlog counts
6. rerun all gates
7. only then mark `最终执行稿`

Never publish, upload, delete old files, or mark a human blocker resolved without explicit user confirmation.

## File Write Gate

Do not write files when the task is a benchmark, dry run, blind test, score, review-only request, prompt demonstration, or process rehearsal.

Do not write files when platform or counts are unconfirmed.

Do not overwrite original sources or write outside the current project's `outputs/`.

## Failure Conditions

Stop delivery and keep `待人工审查` when any of these remain:

- credentials, patient authorization, treatment result, price, booking, case data, or policy interpretation is unverified
- `01/02/03` counts or spoken lines diverge
- `03` contains source/heat/production metadata
- `03` lacks `不能说`
- Vlog Xiaohongshu copy uses a medical consultation template
- source relationship is not classified
- generic shot placeholders dominate `02`
- automated gates fail
- any role-specific human blocker is open

## Bundled Resources

- `scripts/audit_delivery_quality.py`: hard quality gate for role purity, counts, sync, platform schemas, CTA repetition, source evidence, and shot specificity
- `scripts/audit_duration.py`: spoken-duration audit
- `scripts/audit_sensitive_claims.py`: obvious medical-risk scan
- `scripts/sync_teleprompter_to_shooting.py`: scaffold helper only, not a final-delivery generator
- `scripts/make_prepublish_checklist.py`: platform checklist generator
- `scripts/build_editor_source_trace.py`: optional chief-editor trace backup after explicit request
- `test-prompts.json`: regression prompts from real failures
