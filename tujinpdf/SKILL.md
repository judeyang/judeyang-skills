---
name: 土金PDF
description: Convert any existing file or document into a polished A4 土金色系 magazine-style PDF. Use when the user asks for “土金PDF”, “tujinpdf”, “土金色系PDF”, “杂志风PDF”, or wants a document restyled with a specific earthy-gold palette, refined typography, spacing, page rhythm, tables, cover, and print-ready PDF layout. This skill only changes visual style and layout; preserve content unless the user explicitly asks for content edits.
---

# 土金PDF

把任意文档改成土金色系杂志风 PDF。这个 skill 只做三件事：

1. 读取用户给的内容。
2. 重新排版成土金色系 A4 HTML。
3. 用浏览器渲染成 PDF。

不要承担内容编辑、内容筛选、内容判断、事实修正、口径调整。除非用户明确要求，否则不要改原文。

## Operating Contract

每次触发后，先判断当前任务属于哪一类：

1. **新建排版**：用户给内容，需要生成新的 HTML + PDF。
2. **续改旧版**：用户给已有 HTML/PDF，需要在原 HTML 上改版。
3. **样式修复**：用户指出溢出、重叠、分页、表格或封面问题，只修版式。
4. **内容编辑 + 排版**：用户明确要求润色、精简、改口径或重写内容；先把内容编辑范围说清楚，再排版。

默认只做新建排版或续改旧版。任务不清楚时，按“只改呈现，不改内容”处理，并在回复里说明这个边界。

## Input

支持任意可读取内容：

- Markdown / TXT
- HTML
- PDF / DOCX / XLSX 中提取出来的文本或表格
- 项目总结、报告、方案、报价单、记录、归档材料
- 用户直接贴在对话里的内容

## Output

默认输出：

- 一个 `.html` 源文件
- 一个同名 `.pdf`
- 必要时一个预览截图用于检查

HTML 必须保留，因为后续改版要直接在原 HTML 上升级，不要每次新建一版。

文件命名：

- 新建：`文档主题_土金PDF_v01.html`、`文档主题_土金PDF_v01.pdf`
- 续改：沿用原主题并递增版本号，如 `项目总结_土金PDF_v02.html`
- 截图：`文档主题_土金PDF_v01_preview.png`
- 不覆盖旧版本；如果用户明确要求覆盖，先进入 checkpoint。

输出目录优先使用用户指定目录；没有指定时，放在当前任务的 `outputs/` 或项目约定交付目录。

## Core Workflow

1. **读取输入**：确认源文件路径、文本内容、目标读者、是否需要保留全部内容。
2. **提取结构**：识别标题、日期、元信息、章节、表格、列表、关键数字和附件说明。
3. **生成 HTML**：使用 A4 页面、土金色系变量、封面、页眉页脚、章节和表格样式。
4. **渲染 PDF**：运行 `scripts/render-html-pdf.mjs` 输出 PDF 和预览截图。
5. **质量检查**：检查 PDF 可打开、页数合理、文本可提取、截图无明显溢出重叠。
6. **交付说明**：说明生成了哪些文件、是否改动原文、未验证项和下一步可改什么。

## Style

目标风格：土金色系、克制、杂志感、留白充足、中文精致排版。

基础视觉参数：

- 页面：A4，`210mm x 297mm`
- 背景：暖纸色 `#f4ede1`
- 辅助底色：`#efe6d6`
- 主文字：`#1f1a16`
- 次文字：`#4a3f33`
- 注释文字：`#8a7a68`
- 金色线条/强调：`#a8854a`
- 细线：`rgba(31,26,22,0.10~0.18)`

排版规则：

- 首页做封面：品牌/来源、文档类型、主标题、关键元信息。
- 正文使用章节结构：章号、标题、正文、表格、卡片。
- 章节之间留足呼吸感，不要堆满。
- 标题居中或左对齐要根据页面结构决定，不要混乱。
- 表格：短内容居中，长内容左对齐。
- 表格表头必须统一居中。不要为了让正文长内容左对齐，把左对齐类或样式加到 `th` 上。正确做法是：`th { text-align: center; }`，正文短内容单元格居中，正文长内容单元格左对齐。
- 不要卡片套卡片。
- 不要额外添加无意义装饰图、雷达图、六边形图、占位标签或引文。
- 只有当源文档本来有图表/引用/关键数字时，才把它们设计成可视元素。

推荐模板词汇：

- `.page`
- `.cover`
- `.cover-frame`
- `.pg-hd`
- `.pg-ft`
- `.ch`
- `.ch-head`
- `.ch-num`
- `.ch-title`
- `.ch-body`
- `.fact-grid`
- `.prod`
- 细线表格

可参考 FatePaw 模板的视觉语言，但不要继承其命理业务内容：

- `/Users/jude/同步空间/作品集/APP/bazi/fatepaw/src/templates/pet-reading-pdf-zh.html`
- `/Users/jude/同步空间/作品集/APP/bazi/fatepaw/src/templates/human-reading-pdf-zh.html`

## Content Rules

- 保留原文信息、数字、日期、人名、标题、原因、结论。
- 只改变呈现方式，不擅自删改内容。
- 可以把原文分成更清晰的章节、表格、信息块，但不得改变意思。
- 如果源文档很乱，先按现有内容排版；只有用户要求“润色/精简/删掉/改口径”时才改内容。

如果用户要求内容编辑，必须在输出中区分：

- `内容编辑`：改了哪些文字、删了哪些重复、合并了哪些段落。
- `版式设计`：改了哪些视觉结构、表格、封面、分页。
- `未改动`：保留了哪些原始数字、日期、人名、结论。

## Failure Branches

- 如果输入文件无法读取，先说明失败路径和原因，再请求用户提供可读文件或粘贴文本；不要凭文件名猜内容。
- 如果 PDF/DOCX/XLSX 提取文本为空，判断是否为扫描件或图片型内容；需要 OCR 时调用合适的 PDF/OCR 流程后再排版。
- 如果源内容缺少标题，使用文件名或首段生成临时标题，并标注为可改标题。
- 如果源表格过宽，优先横向压缩列宽、拆表或分页，不把字号压到不可读。
- 如果浏览器渲染失败，保留 HTML，检查 Chrome/Puppeteer 可用性、资源路径、CSS 语法和输出目录权限。
- 如果预览截图发现文字溢出、重叠、截断或异常空白，先修 HTML/CSS，再重新渲染 PDF。
- 如果用户只给 PDF 且要求“保持原样但换风格”，先提取文本和表格；不能保证像素级复刻时要说明限制。

## 🔴 CHECKPOINT

以下情况必须暂停并等待用户确认：

- 用户要求删除、合并、改写、降调、隐藏或重新解释原文中的重要事实、数字、责任、价格、日期、客户意见或结论。
- 用户要求覆盖旧版 HTML/PDF，而不是递增版本号。
- 源内容包含合同、报价、发票、财务、法律、医疗、隐私、账号、支付或客户敏感数据。
- 需要使用外部在线服务上传源文件、图片、PDF 或客户资料。
- 需要把 PDF 发布到公开链接、发送给客户、提交到线上系统或写入生产目录。
- 用户要求模仿第三方品牌、商业模板或受版权保护的版式到高度相似。

## Rendering

使用真实浏览器渲染，不用 ReportLab 手搓 PDF。

```bash
node /Users/jude/.codex/skills/tujinpdf/scripts/render-html-pdf.mjs input.html output.pdf --screenshot preview.png
```

脚本会优先使用可用的 Puppeteer；如果 Puppeteer 自带 Chrome 缺失，会尝试本机 Chrome：

`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`

## QA

生成后必须检查：

- PDF 能打开；
- 页面是 A4；
- 首页无多余外框和无关装饰；
- 标题、正文、表格层级清楚；
- 没有文字溢出、重叠、截断；
- 没有大段异常空白；
- 表格短内容居中、长内容左对齐；
- 原文内容没有被静默改写。
- 生成的 PDF 和 HTML 文件名版本一致；
- 如果生成了截图，截图中首页标题、正文和表格没有明显裁切。

可用文本检查：

```bash
python3 - <<'PY'
from pypdf import PdfReader
p = 'output.pdf'
r = PdfReader(p)
print('pages', len(r.pages))
print('\\n'.join((page.extract_text() or '') for page in r.pages)[:1200])
PY
```

## Anti-Patterns And Blacklist

- 不要用 ReportLab 手搓复杂 PDF；必须先生成可维护 HTML，再用真实浏览器渲染。
- 不要为了“更好看”静默删掉原文、数字、日期、责任边界或客户反馈。
- 不要卡片套卡片、堆装饰图、堆图标、堆雷达图、堆无意义引文。
- 不要把命理、FatePaw 或其他业务内容带进普通文档。
- 不要只交 PDF 不交 HTML。
- 不要在未检查 PDF 的情况下说完成。
- 不要把本地绝对路径、客户隐私、token、cookie 或未脱敏敏感信息写进交付正文。
