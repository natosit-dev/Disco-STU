"""Pure display formatting for the local, single-user STU interface.

Labels are derived from existing provenance; never replace identity fields.
No Streamlit, storage writes, model calls, or semantic interpretations.
"""
from __future__ import annotations

import os
from datetime import datetime
from zoneinfo import ZoneInfo

MODEL_NAMES = {
    "gemma-4-31b-it": "Gemma 4 31B",
    "qwen3.5-397b": "Qwen 3.5 397B",
    "glm-5.2": "GLM 5.2",
    "fixture": "Synthetic fixture",
}
COMPARISON_NAMES = {
    "original_vs_neutral": "Original → Neutral",
    "original_vs_commercial": "Original → Commercial",
    "oracle_vs_neutral": "Authorial intention → Neutral",
    "oracle_vs_commercial": "Authorial intention → Commercial",
    "oracle_vs_original": "Authorial intention → Original",
    "original_vs_decomposition": "Original → Decomposition",
    "oracle_vs_decomposition": "Authorial intention → Decomposition",
    "decomposition_vs_neutral": "Decomposition → Neutral",
    "decomposition_vs_commercial": "Decomposition → Commercial",
    "neutral_vs_commercial": "Neutral → Commercial",
}

# WSL may be configured in UTC. This is an explicit presentation setting, not
# a modification to any recorded UTC timestamp or the source writing date.
DEFAULT_TIMEZONE = "America/New_York"


def display_datetime(value: str | None, *, tzname: str | None = None) -> str:
    if not value:
        return "Time unavailable"
    tzname = tzname or os.environ.get("STU_UI_TIMEZONE", DEFAULT_TIMEZONE)
    try:
        tz = ZoneInfo(tzname)
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if stamp.tzinfo is None:
            return "Time zone unspecified"
        return stamp.astimezone(tz).strftime("%b %-d, %Y, %-I:%M %p %Z")
    except (ValueError, KeyError, OSError, OverflowError):
        return "Time unavailable"


def model_name(model_id: str | None) -> str:
    if not model_id:
        return "Model unavailable"
    return MODEL_NAMES.get(model_id, model_id)


def sample_name(source: dict) -> str:
    return source.get("title", "").strip() or "Untitled source"


def study_name(study: dict, source: dict) -> str:
    return (f"{sample_name(source)} · {display_datetime(study.get('created_at'))}"
            f" · {study['study_id'][:8]}")


def run_name(run: dict) -> str:
    return (f"{model_name(run.get('model_profile'))} · "
            f"{display_datetime(run.get('started_at'))} · {run['run_id'][:8]}")


def comparison_name(comp: dict, *, run: dict | None = None,
                    include_status: bool = True) -> str:
    name = COMPARISON_NAMES.get(comp["kind"], comp["kind"].replace("_", " ").title())
    if run:
        name += " · " + model_name(run.get("model_profile"))
    if include_status:
        state = comp.get("review", {})
        label = state.get("status", "not_started").replace("_", " ").title()
        name += " · " + label
    return name
