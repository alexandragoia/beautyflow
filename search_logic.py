"""Validation helpers for free-text beauty search extraction."""
from __future__ import annotations

import json
import re
from datetime import date
from typing import Any

SERVICES = {"french", "gel", "balayage", "keratin", "massage", "microblading", "brows"}


def normalize_filters(value: Any, today: date | None = None) -> dict[str, Any]:
    """Keep only small, valid search filters returned by the language model."""
    if not isinstance(value, dict):
        value = {}
    today = today or date.today()
    zip_code = value.get("zip")
    if not isinstance(zip_code, str) or not re.fullmatch(r"10\d{3}", zip_code):
        zip_code = None

    service = value.get("service")
    if not isinstance(service, str) or service not in SERVICES:
        service = None

    budget = value.get("budget_eur")
    if isinstance(budget, bool) or not isinstance(budget, int) or not 1 <= budget <= 1000:
        budget = None

    chosen_date = value.get("date")
    if isinstance(chosen_date, str):
        try:
            parsed = date.fromisoformat(chosen_date)
            if parsed < today:
                chosen_date = None
            else:
                chosen_date = parsed.isoformat()
        except ValueError:
            chosen_date = None
    else:
        chosen_date = None

    return {"zip": zip_code, "service": service, "budget_eur": budget, "date": chosen_date}


def parse_model_output(text: str, today: date | None = None) -> dict[str, Any]:
    """Parse the assistant's JSON response and validate its user-facing fields."""
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("Model response must be a JSON object")
    reply = data.get("reply")
    if not isinstance(reply, str):
        raise ValueError("Model response has no reply")
    reply = reply.strip()
    if not reply or len(reply) > 900:
        raise ValueError("Model response reply is empty or too long")
    return {"reply": reply, "filters": normalize_filters(data.get("filters"), today)}
