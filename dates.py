"""Deterministic date resolution. The LLM only describes WHAT the customer said
(e.g. "Thursday", "tomorrow", "15 October"); this code computes the actual date.

Conventions (documented on purpose, they can be tested):
- a bare weekday ("Thursday", "am Donnerstag", "el jueves", "next Thursday") means the
  next upcoming one; if today is that weekday it means the one in 7 days
- week="next" is used only for "next week" phrasing and means that weekday of the
  following Monday-Sunday week
- a date without year means the next occurrence on or after today
"""
from datetime import date, timedelta

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def resolve_date(expr, today: date) -> date | None:
    """expr examples:
    {"kind": "weekday", "weekday": "thursday", "week": "unspecified|next"}
    {"kind": "offset", "days": 1}                     # 0 = today, 1 = tomorrow
    {"kind": "absolute", "day": 15, "month": 10, "year": null}
    Returns None when the expression cannot be resolved to a valid future date."""
    if not isinstance(expr, dict):
        return None
    try:
        kind = expr.get("kind")
        if kind == "offset":
            result = today + timedelta(days=int(expr["days"]))
        elif kind == "weekday":
            idx = WEEKDAYS.index(str(expr["weekday"]).lower())
            if expr.get("week") == "next":
                monday_next_week = today + timedelta(days=7 - today.weekday())
                result = monday_next_week + timedelta(days=idx)
            else:
                result = today + timedelta(days=(idx - today.weekday()) % 7 or 7)
        elif kind == "absolute":
            day, month, year = int(expr["day"]), int(expr["month"]), expr.get("year")
            if year:
                result = date(int(year), month, day)
            else:
                result = date(today.year, month, day)
                if result < today:
                    result = date(today.year + 1, month, day)
        else:
            return None
    except (KeyError, ValueError, TypeError):
        return None
    return result if result >= today else None
