# SkillHub 发布检查表

## 已完成

- `main` 分支根目录 `SKILL.md` 使用通用 Agent Skills 字段；
- `skillhub` 分支在同一内容上展开腾讯 CLI 要求的 `slug`、`displayName`、`version`、`summary` 和 `license`；
- SkillHub `slug` 使用全网更不易冲突的 `sunshine-digital-nomad-wealth`；
- 无 API Key、账号凭证、用户数据或隐藏外发；
- 评分脚本仅使用 Python 标准库；
- 单元测试覆盖满分、风险扣分、边界值、缺失值与包结构；
- README、示例、市场研究、商业化和安全边界齐全。

## 发布前

1. 在 WorkBuddy 本地上传 ZIP，至少测试五个提示：模糊目标、路径比较、90天计划、纯旅游请求、保证收入请求。
2. 运行：

   ```bash
   python3 -m unittest discover -s tests -v
   git switch skillhub
   skillhub publish . --dry-run
   ```

3. 检查名称、摘要、触发词和免责声明在移动端是否完整。
4. 准备512×512 PNG头像、20–120字开发者简介和至少一个公开联系方式。
5. 完成个人实名认证或企业认证；创建 API Token 时不要提交到 GitHub。

## 正式发布

```bash
git switch skillhub
skillhub publish . --changelog "首次发布：跨界画像、机会组合与90天验证计划"
```

预期状态为 `pending_review`。审核通过前详情页可能不可见。

## Pay Skill 升级前

- 已有至少10份真实深度交付和明确重复流程；
- 用户明确愿意为结果而不是篇幅付费；
- 后端能保护付费逻辑、最小化数据并返回证据状态；
- 支付前展示价格、交付范围、数据用途与退款路径；
- 对签证、税务、法律和投资请求设置强制转介与核验。
