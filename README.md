# 跨界数字游民财富导航

> 成为你所在交叉赛道的“数字游民首富”：不是预测财富，而是找到最值得复利的全球优势。

这是一个面向 WorkBuddy / SkillHub 及兼容 Agent Skills 客户端的中文技能。它帮助知识工作者把专业、兴趣、作品、网络与地点自由组合成三类可验证机会：近期现金引擎、可重复出售的证据资产、长期选择权。

## 它解决什么问题

普通职业规划往往只回答“适合什么岗位”，数字游民攻略往往只回答“去哪里”。本技能把两者之间缺失的决策层补上：

| 输入 | 决策 | 输出 |
|---|---|---|
| 专业、兴趣、作品、网络与约束 | 跨界稀缺性、全球可携带性、买方价值与风险 | 一句话定位、机会组合、90天实验与证据资产清单 |

适合科研人员、教育者、创作者、顾问、产品经理、自由职业者和准备跨界/出海的高技能职场人。不适合纯旅游行程、移民或税务结论、投资交易和任何“保证赚钱”的请求。

## 试着这样问

- “我做经济学研究，也会数据可视化和AI工具，怎样形成可远程交付的全球业务？”
- “比较学术研究、独立咨询和知识产品三条路线，给我一个90天低成本验证计划。”
- “用我的简历和作品集找出最稀缺的两个交叉优势，不要泛泛建议。”
- “我想边旅行边工作，但不想只靠一个雇主，帮我设计收入组合和风险边界。”
- “把本季度的新客户、作品和反馈加入画像，判断该继续、调整还是停止。”

## 使用

### WorkBuddy 本地试用

下载本仓库 ZIP，在 WorkBuddy 的“技能”页面选择“上传技能”，导入包含根目录 `SKILL.md` 的技能包。导入前可审查全部文件；本版本不需要 API Key，也不会自行上传数据。

### 透明评分

```bash
python3 scripts/score_profile.py examples/sample-input.json
python3 -m unittest discover -s tests -v
```

评分只用于比较和发现瓶颈，不预测未来收入。完整锚点见 [评估框架](references/assessment-framework.md)。

### 发布到 SkillHub

本仓库的 `main` 分支保持通用 Agent Skills 兼容；`skillhub` 分支按腾讯 CLI 要求展开发布字段。完成 SkillHub 实名认证与 CLI 登录后：

```bash
git switch skillhub
skillhub publish . --dry-run
skillhub publish . --changelog "首次发布"
```

官方发布流程见 [SkillHub 使用指南](https://skillhub.cloud.tencent.com/tutorials#publish-via-cli)。

## 产品与市场

- [WorkBuddy 用户需求与竞争扫描](docs/USER_RESEARCH.md)
- [SkillPay 商业化路线](docs/MONETIZATION.md)
- [发布检查表](docs/RELEASE_CHECKLIST.md)
- [示例输出](examples/sample-output.md)

## 隐私与边界

本技能默认最小化收集信息，不需要身份证件、账户凭证、精确住址或雇主机密。涉及签证、税务、法律、生活成本或当前市场数据时，应以对应司法辖区的官方信息和持牌专业意见为准。

## License

MIT © 2026 Luyao (Sunshine) Zhang
