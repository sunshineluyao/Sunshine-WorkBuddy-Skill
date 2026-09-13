#!/usr/bin/env python3
"""Score a cross-border compound-advantage profile with transparent weights."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


AXES = {
    "expertise_evidence": (0.20, "专业证据", "Expertise evidence"),
    "portable_delivery": (0.15, "远程可交付性", "Portable delivery"),
    "global_demand": (0.15, "全球需求", "Global demand"),
    "cross_domain_scarcity": (0.15, "跨界稀缺性", "Cross-domain scarcity"),
    "distribution_network": (0.10, "分发与网络", "Distribution and network"),
    "revenue_durability": (0.15, "收入耐久性", "Revenue durability"),
    "location_resilience": (0.10, "地点韧性", "Location resilience"),
}

RISKS = {
    "compliance_data": (8.0, "合规与数据风险", "Compliance and data risk"),
    "income_concentration": (7.0, "收入集中风险", "Income concentration risk"),
    "capacity_burnout": (5.0, "容量与倦怠风险", "Capacity and burnout risk"),
}


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a number from 0 to 5")
    number = float(value)
    if not 0 <= number <= 5:
        raise ValueError(f"{label} must be between 0 and 5")
    return number


def _stage(score: float) -> str:
    if score >= 90:
        return "复利"
    if score >= 75:
        return "扩张"
    if score >= 60:
        return "证明"
    if score >= 40:
        return "验证"
    return "打底"


def _stage_en(score: float) -> str:
    if score >= 90:
        return "Compound"
    if score >= 75:
        return "Scale"
    if score >= 60:
        return "Prove"
    if score >= 40:
        return "Validate"
    return "Foundation"


def score_profile(payload: dict[str, Any]) -> dict[str, Any]:
    axes = payload.get("axes")
    risks = payload.get("risks")
    if not isinstance(axes, dict) or not isinstance(risks, dict):
        raise ValueError("input must contain object fields: axes and risks")

    missing_axes = sorted(set(AXES) - set(axes))
    missing_risks = sorted(set(RISKS) - set(risks))
    if missing_axes or missing_risks:
        missing = missing_axes + missing_risks
        raise ValueError("missing required fields: " + ", ".join(missing))

    axis_points: dict[str, float] = {}
    risk_points: dict[str, float] = {}
    raw_axes: dict[str, float] = {}

    for key, (weight, _label_zh, _label_en) in AXES.items():
        value = _number(axes[key], key)
        raw_axes[key] = value
        axis_points[key] = round((value / 5.0) * weight * 100.0, 2)

    for key, (maximum, _label_zh, _label_en) in RISKS.items():
        value = _number(risks[key], key)
        risk_points[key] = round((value / 5.0) * maximum, 2)

    base_score = round(sum(axis_points.values()), 2)
    risk_deduction = round(sum(risk_points.values()), 2)
    final_score = round(max(0.0, min(100.0, base_score - risk_deduction)), 1)

    ranked = sorted(raw_axes, key=lambda key: (-raw_axes[key], key))
    bottleneck_keys = sorted(raw_axes, key=lambda key: (raw_axes[key], key))[:2]
    strengths = [AXES[key][1] for key in ranked[:2]]
    strengths_en = [AXES[key][2] for key in ranked[:2]]
    bottlenecks = [AXES[key][1] for key in bottleneck_keys]
    bottlenecks_en = [AXES[key][2] for key in bottleneck_keys]

    return {
        "score": final_score,
        "stage": _stage(final_score),
        "stage_en": _stage_en(final_score),
        "base_score": base_score,
        "risk_deduction": risk_deduction,
        "axis_points": axis_points,
        "risk_points": risk_points,
        "strengths": strengths,
        "strengths_en": strengths_en,
        "bottlenecks": bottlenecks,
        "bottlenecks_en": bottlenecks_en,
        "notice": "This score compares options and bottlenecks; it does not predict income.",
        "notice_zh": "本分数仅用于比较选项与发现瓶颈，不预测收入。",
    }


def _load(path: str) -> dict[str, Any]:
    if path == "-":
        data = json.load(sys.stdin)
    else:
        with Path(path).open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("input JSON must be an object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="profile JSON path, or - for stdin")
    parser.add_argument("--compact", action="store_true", help="emit compact JSON")
    args = parser.parse_args()

    try:
        result = score_profile(_load(args.input))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    indent = None if args.compact else 2
    print(json.dumps(result, ensure_ascii=False, indent=indent, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
