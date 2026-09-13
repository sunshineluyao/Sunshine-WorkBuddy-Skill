# Privacy and permissions / 隐私与权限

[English](#english) · [简体中文](#简体中文)

This notice describes the behavior of Sunshine Digital Nomad Wealth Navigator version 1.1.0. Host applications and search providers may have additional policies.

本文说明 Sunshine 跨界数字游民财富导航 1.1.0 的数据行为。宿主应用和检索服务可能另有隐私政策。

## English

### Plain-language promise

The skill uses only the information the user voluntarily supplies for the current task. It does not request passwords, API keys, identity documents, exact home addresses, private client lists, or employer secrets. It has no independent server, analytics service, advertising tracker, or hidden database.

“Explicit learning” means improving later recommendations from experiment outcomes saved with explicit permission. It does not train the underlying model, create hidden memory, or monitor anything in the background.

### Data and permissions

| Capability | Data involved | Destination | Default | User control |
|---|---|---|---|---|
| Profile and strategy | Goals, skills, evidence, interests, and constraints supplied in the conversation | The current WorkBuddy or host session | Used only when provided | Omit, generalize, or correct any field |
| Current research | Minimal search terms derived from the question; never the full CV or ledger by default | The search capability configured by the host | Used only when current facts are decision-critical and a search tool is available | Ask for offline-only analysis or review each query |
| Transparent scoring | A local JSON profile selected by the user | Local Python process | Optional | Inspect the input and output; delete the file |
| Learning ledger | Sanitized experiment hypothesis, expected signal, observed signal, decision, lesson, and tags | A user-chosen local JSON file | Off until explicit permission | Inspect, export, decline, or delete the ledger at any time |

Current research may consume additional WorkBuddy credits. The skill should say when live research is unavailable and provide verification queries instead of pretending that recalled information is current.

### Retention and deletion

- Conversation retention is controlled by the host application, not this repository.
- The optional ledger remains at the local path chosen by the user. The helper appends records and never uploads them.
- To remove local learning, delete the ledger file. The skill must continue without persistent learning.
- Removing a local file does not erase host conversation history; use the host application controls for that history.

### Safe use

Use ranges, pseudonyms, and redacted examples where possible. Do not place credentials, government identifiers, health records, confidential contracts, unpublished client information, or employer-confidential material in prompts or ledgers.

## 简体中文

### 简明承诺

本 Skill 只使用用户为当前任务主动提供的信息；不索取密码、API Key、身份证件、精确住址、私有客户名单或雇主秘密。它没有独立服务器、分析服务、广告追踪器或隐藏数据库。

“显式学习”是指根据用户明确授权保存的实验结果改进后续建议；它不训练底层模型，不创建隐藏记忆，也不在后台持续监控。

### 数据与权限

| 能力 | 涉及数据 | 去向 | 默认状态 | 用户控制 |
|---|---|---|---|---|
| 画像与策略 | 用户在对话中提供的目标、能力、证据、兴趣和约束 | 当前 WorkBuddy 或宿主会话 | 仅在用户提供时使用 | 可省略、模糊化或纠正任何字段 |
| 实时研究 | 从问题提炼出的最少检索词；默认不发送完整简历或学习账本 | 宿主配置的检索能力 | 仅在时效性事实影响决策且工具可用时使用 | 可要求只做离线分析或先查看检索词 |
| 透明评分 | 用户选择的本地 JSON 画像 | 本地 Python 进程 | 可选 | 可检查输入输出并删除文件 |
| 学习账本 | 经脱敏的实验假设、预期信号、观察结果、决策、经验和标签 | 用户选择的本地 JSON 文件 | 未明确授权时关闭 | 可随时检查、导出、拒绝或删除 |

实时研究可能消耗额外 WorkBuddy 积分。若实时检索不可用，Skill 应明确说明并给出核验查询，而不是把模型记忆假装成最新信息。

### 保留与删除

- 对话保留由宿主应用控制，不由本仓库控制；
- 可选学习账本保存在用户选择的本地路径；辅助脚本只追加记录，不会上传；
- 如需删除本地学习记录，删除账本文件即可；Skill 必须能够在无持久化学习时继续工作；
- 删除本地文件不会清除宿主会话历史；会话历史需使用宿主应用提供的控制项处理。

### 安全使用

尽量使用区间、化名和脱敏案例。不要在提示词或账本中放入账号凭证、政府证件号、健康记录、保密合同、未公开客户信息或雇主机密。
