# Live Research and Learning Protocol / 实时研究与学习协议

Use this reference for current opportunity scans, competitor comparisons, location-dependent claims, and learning reviews. The protocol makes recommendations fresher and more competitive without pretending that any search covers the entire web or that the model retrains itself.

在实时机会扫描、竞品比较、地点相关判断和学习复盘中使用本协议。目标是提升建议的新鲜度与竞争力，同时不虚构“搜索了全网”或“模型已自我训练”。

## 1. Freshness gate / 新鲜度门

Live verification is required when a claim concerns current compensation, demand, hiring, customers, competitors, product features, pricing, platform rules, visas, tax, regulation, exchange or payment conditions, living costs, grants, deadlines, events, or named decision-makers.

| Claim type / 信息类型 | Minimum treatment / 最低处理 |
|---|---|
| Rule, price, deadline, product capability | Check the authoritative source during this run and record the exact as-of date |
| Visa, tax, regulation, professional license | Use the responsible government or regulator; convert advice into questions for a qualified local professional |
| Market demand, compensation, buyer behavior | Use recent direct observations or datasets plus an independent source; state geography and sample limits |
| Competitor positioning or pricing | Check the competitor’s current official page, then seek independent evidence about actual adoption or buyer response |
| Evergreen method | Prefer the latest authoritative version; live search is optional unless the version matters |

If no live tool is available, explicitly say that freshness was not verified. Provide precise queries and target source types so the user can verify; do not fill the gap from memory.

## 2. Bilingual search ladder / 双语检索阶梯

For a global or cross-border request, search both the user’s language and English when useful. Run only the steps necessary to reach decision-sufficient evidence.

1. **Define the decision.** Write the buyer, outcome, geography, time horizon, and what evidence could change the recommendation.
2. **Discover vocabulary.** Search the user’s phrase, buyer-language wording, outcome terms, and two realistic synonyms. Include local-language terms for a target jurisdiction.
3. **Verify primary facts.** Open official product, government, regulator, company, dataset, or program pages. Search snippets are leads, not evidence.
4. **Challenge the leading view.** Search for limitations, failure cases, price changes, closures, complaints, or contrary data. Distinguish criticism from verified failure.
5. **Confirm consequential claims.** Seek an independent source with a different incentive or method. If unavailable, mark the conclusion single-source.
6. **Stop deliberately.** Stop when the key decision claims are supported, remaining uncertainty is explicit, and another query is unlikely to change the next reversible action.

When results are weak, rewrite at least twice: switch from solution language to buyer-problem language, vary geography, expand acronyms, use exact phrases, or search a primary domain directly.

## 3. Source grading / 来源分级

Grade each source on four dimensions rather than using a single prestige label.

| Dimension / 维度 | Strong / 强 | Weak / 弱 |
|---|---|---|
| Authority | Responsible agency, first-party product owner, original dataset, direct buyer evidence | Aggregator, repost, anonymous summary |
| Directness | Directly establishes the claim | Mentions a related topic only |
| Freshness | Current enough for the decision and visibly dated | Undated or superseded |
| Independence | Different owner, incentive, or method from the first source | Copies or depends on the same upstream source |

Do not add scores across unrelated dimensions to create false precision. A first-party price page may be authoritative but not independent; a user review may be independent but not authoritative.

## 4. Competitive opportunity scan / 竞争机会扫描

Compare three to seven credible alternatives when the market is mature enough. “Competitor” includes direct tools, substitutes, manual services, and the buyer doing nothing.

| Field / 字段 | Question / 问题 |
|---|---|
| Buyer | Who chooses or pays? |
| Promise | What costly outcome is offered? |
| Proof | What demo, case, review, or measurable result exists? |
| Freshness | When was the claim or product state checked? |
| Model | Free, paid, subscription, service, referral, or institutional? |
| Strength | What does this alternative already do credibly? |
| Gap | Which important buyer need remains poorly served? |
| Implication | Differentiate, partner, narrow the niche, or stop? |

Never infer an “empty market” from zero search results. It may indicate weak vocabulary, poor indexing, low demand, or inaccessible sources. Never claim “unique,” “best,” or “first” without a documented search scope.

## 5. Decision-ready research snapshot / 可决策研究快照

Return the minimum evidence that changes action:

- **As of / 截至：** exact date and relevant geography;
- **Decision / 决策：** what choice this research informs;
- **Verified signals / 已核验信号：** claim with nearby source and evidence status;
- **Competitive pattern / 竞争格局：** credible strengths and gaps;
- **Conflicts / 冲突：** incompatible claims and likely reason;
- **Inference / 推断：** conclusion derived from named facts;
- **Unknowns / 未知：** what remains unverified;
- **Next test / 下一验证：** smallest action that resolves the highest-value uncertainty.

## 6. Explicit learning ledger / 显式学习账本

The ledger is optional, user-owned state. Read or write it only when the user provides it or explicitly authorizes persistence. Use `scripts/learning_ledger.py` when local execution is available; otherwise return an event matching the schema below.

```json
{
  "date": "2026-09-13",
  "experiment": "Publish a one-page bilingual research audit offer",
  "hypothesis": "Early-stage global teams will value an evidence audit before a strategy engagement",
  "expected_signal": "At least 3 qualified replies from 20 consent-respecting introductions",
  "observed_signal": 1,
  "evidence": "4 qualified replies and 2 paid discovery calls",
  "decision": "continue",
  "lesson": "The audit framing outperformed generic strategy consulting",
  "tags": ["research-audit", "bilingual", "founder"]
}
```

`observed_signal` is an integer from -2 to 2: strong negative, negative, inconclusive, positive, strong positive. This directional signal supports comparison; it does not replace raw evidence.

### Update logic / 更新逻辑

1. Preserve each raw event and its date; do not edit an old outcome to fit the current story.
2. Compare expected and observed signals. State which assumption was supported, contradicted, or left unresolved.
3. Treat one event as a clue. Treat two compatible events as an emerging pattern. Promote a durable preference only after three or more relevant events with no serious contradictory evidence.
4. Weight direct buyer behavior and completed delivery above compliments, impressions, or model-generated opinions.
5. Apply the lesson only to a sufficiently similar buyer, offer, channel, geography, and constraint set.
6. Show recommendation changes as: previous view → new evidence → updated view → next falsifiable test.
7. Keep contradictory and minority evidence visible. Do not delete failed experiments; they reduce repeated waste.

## 7. Privacy and stopping rules / 隐私与停止规则

- Prefer ranges, roles, and pseudonyms. Exclude credentials, identity documents, exact addresses, health details, private client lists, and confidential employer or research data.
- Never upload or share the ledger without a separate explicit instruction.
- Do not conduct background monitoring. A future refresh requires the user to return or deliberately schedule an approved task in a system that supports it.
- Stop searching when the decision can proceed with a reversible experiment, or when access, paywalls, permissions, identity checks, or professional judgment are required.
