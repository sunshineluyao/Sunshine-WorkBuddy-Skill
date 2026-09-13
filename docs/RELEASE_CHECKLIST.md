# SkillHub 发布检查表

## 已完成

- 仓库只保留唯一的 `main` 分支；
- 可发现技能包位于 `.agents/skills/sunshineluyao-digital-nomad-wealth`；
- `SKILL.md` 顶层只使用 Agent Skills 支持的字段；SkillHub 展示信息保存在 `metadata` 和 `docs/SKILLHUB_LISTING.md`；
- SkillHub `slug` 使用带作者前缀、更不易冲突的 `sunshineluyao-digital-nomad-wealth`；
- 无 API Key、账号凭证、用户数据或隐藏外发；
- 评分脚本仅使用 Python 标准库；
- 单元测试覆盖满分、风险扣分、边界值、缺失值与包结构；
- README、示例、市场研究、商业化和安全边界齐全。
- 英文 `README.md` 与中文 `README.zh-CN.md` 双向链接，核心用户体验完整对齐；
- 用户旅程 SVG 与 Mermaid 软件架构图仅使用 GitHub 可渲染的安全元素；
- 对时效性事实执行实时检索、双语查询、来源分级、反证检查和截至日期；
- 显式学习账本仅在用户授权后本地保存，不声称模型自训练或隐藏记忆；
- 学习账本脚本只追加事件、拒绝重复记录并保留原始证据；
- 512×512 商城图标与 128×128 UI 图标已加入并通过尺寸测试；
- 隐私、权限、支持方式、版本记录与可粘贴上架文案已补齐；
- 八个 WorkBuddy 对话验收场景和可观察通过标准已写入 `docs/ACCEPTANCE_TESTS.md`；

## 发布前

1. 在 WorkBuddy 本地上传 ZIP，逐项运行 `docs/ACCEPTANCE_TESTS.md` 的八个场景并记录结果。
2. 运行标准包校验和测试：

   ```bash
   python3 -m unittest discover -s tests -v
   python3 /path/to/skill-creator/scripts/quick_validate.py .agents/skills/sunshineluyao-digital-nomad-wealth
   ```

3. 确保 GitHub 导入器拥有本仓库读取权限；若不支持 Private 仓库，需要先由仓库所有者改为 Public。
4. 在 GitHub 导入第一页选择 `sunshineluyao-digital-nomad-wealth`，第二步检查名称、摘要、版本、许可证、图标、双语说明和免责声明。
5. 从 `docs/SKILLHUB_LISTING.md` 复制开发者简介、推荐提示词、权限披露、标签与发布说明。
6. 完成个人实名认证或企业认证；任何 API Token 都不要提交到 GitHub。
7. 确认作者 GitHub 主页至少有一个愿意公开的有效联系渠道；SkillHub 详情页上线后把 `SUPPORT.md` 更新为详情页直达链接。

## 正式发布

通过 SkillHub 的 GitHub 导入页面提交 `main` 分支中自动发现的 Skill，并在最终提交前确认 slug 为 `sunshineluyao-digital-nomad-wealth`。

预期状态为 `pending_review`。审核通过前详情页可能不可见。

## Pay Skill 升级前

- 已有至少10份真实深度交付和明确重复流程；
- 用户明确愿意为结果而不是篇幅付费；
- 后端能保护付费逻辑、最小化数据并返回证据状态；
- 支付前展示价格、交付范围、数据用途与退款路径；
- 对签证、税务、法律和投资请求设置强制转介与核验。
