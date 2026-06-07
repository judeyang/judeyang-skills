# 镜头设计师

`镜头设计师` 是一个面向 AI 视频生产的 Agent Skill，用于把已确认脚本、设定资产和参考图转成可执行的视频生成 Prompt。

它专注于：

- Seedance / LibTV 等视频生成工具的逐镜 Prompt
- 首帧、结尾帧、中间关键帧规划
- 角色、场景、产品、道具、特效参考素材绑定
- 禁用 BGM，只保留对白、同期声、动作音效和产品音效
- 三段式视频 Prompt：`【基础设定】`、`【氛围与画质】`、`【画面内容】`
- 逐秒镜头控制：景别、机位、构图、运镜手法、画面内容、特效、声音、结束状态、衔接要求

## 输出合同

最终视频 Prompt 必须使用以下三大标题，不能改名：

```text
【基础设定】
【氛围与画质】
【画面内容】
```

每个时间段必须包含：

```text
景别：
机位：
构图：
运镜手法：
画面内容：
特效：
声音：
结束状态：
衔接要求：
```

## 脚本

创建设定资产制作表：

```bash
python scripts/build_asset_prompt_table.py \
  --input "/path/to/项目名_脚本与资产确认表_v01.xlsx" \
  --project-dir "/path/to/项目交付文件夹"
```

创建内部执行脚本与 Prompt 空表：

```bash
python scripts/build_prompt_table.py \
  --input "/path/to/项目名_脚本与资产确认表_v01.xlsx" \
  --project-dir "/path/to/项目交付文件夹"
```

校验最终 Prompt 表：

```bash
python scripts/validate_prompt_detail.py --input "/path/to/内部执行脚本与Prompt表_v01.xlsx"
```

## 质量边界

- 不生成 BGM。
- 不把 `核心主题`、`运镜规则`、`关键帧调用`、`声音/台词`、`负面要求` 作为视频 Prompt 独立标题。
- 不把风格词写进 `景别`。
- 不把机位词写进 `构图`。
- 产品 Logo、官方屏显、人物脸、手和关键道具优先于装饰性特效。
