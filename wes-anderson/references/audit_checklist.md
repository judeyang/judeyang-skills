# Script Audit Checklist

Use this checklist when producing `脚本审核确认表.xlsx`.

## Client Decision Checks

Confirm these before execution:
- Is the script required to be followed 100%?
- Is professional adjustment allowed if the script is not video-friendly?
- Which items are non-negotiable: product name, slogan, dialogue, runtime, character, scene, style?
- Is runtime expansion allowed?
- Are product images, logo, font authorization, brand guidelines, music, sound effects, or voiceover references available?

## Runtime And Dialogue Rules

Use these as practical production thresholds:

- 1 second: only reaction, gesture, blink, short impact, or one very short sound.
- 2 seconds: 6-8 Chinese characters max if lip sync is needed.
- 3 seconds: 10-12 Chinese characters max, with simple action.
- 4 seconds: one short complete line or short product claim.
- 5+ seconds: explanatory line is possible, but the shot should not also carry too many effects/actions.

High risk by default:
- dialogue + acting + complex VFX + product exposure in the same short shot
- multiple characters speaking or reacting in a 2-3 second shot
- major environment transformation in under 4 seconds
- product/logo visible while the prompt also demands heavy motion or smoke

## Story And Brand Checks

Look for:
- forced product entrance
- protagonist becoming passive
- conflict solved too easily
- character action not motivated
- repetitive explanation
- hard ad-speak inside dramatic scenes
- product claim stronger than visual/story evidence
- jokes that damage brand tone

Typical fix:
- add a character attempt/failure before product solution
- convert product entrance into world-appropriate logic, such as magic object -> product
- shorten dialogue and move information into action/visuals
- move brand statement to the clean closing shot

## AI Generation Feasibility Checks

High-risk prompt patterns:
- too many simultaneous transformations
- smoke, sand, water, leaves, character motion, and product detail all in one short shot
- exact text/logo on moving product without official reference
- many characters in a single shot with face consistency required
- horse/animal motion without reference

Fix by:
- simplifying each shot to one visual priority
- splitting transformations into stages
- using official product reference
- generating/confirming character and scene assets first

## Asset Extraction Categories

Always extract:

| Category | Examples |
|---|---|
| Characters | 孙悟空、唐三藏、猪八戒、沙僧、黄风怪、灵吉菩萨 |
| Animals/Mounts | 白龙马 |
| Scenes | 黄风岭、花果山、雨林、落版背景 |
| Product/Brand | 空调、Logo、机身、屏幕字、卖点、落版 |
| Props/Magic | 金箍棒、净风宝瓶、定风珠 |
| Effects | 黄沙、黑烟、水幕、祥光、绿叶花瓣 |
| Typography/Packaging | 标题字、字幕、口播字、落版 |

## Suggested Issue Types

Use stable issue labels:
- 客户权限确认
- 返工风险确认
- 边界确认
- 时长不合理
- 台词超时
- 剧情推进生硬
- 产品登场生硬
- 角色主动性不足
- 视觉执行风险
- 图像表达确认
- 媒体资产确认
- 版权资产确认
- 建议增加时长
