"""Run the labelled cases through BeautyFlow AI and report metrics.

    python evaluate.py              # full pipeline (extraction + replies)
    python evaluate.py --no-reply   # extraction + rules only (cheaper, skips reply-dependent cases)
"""
import argparse
import json
import re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from beautyflow import KB, process
from cases import CASES, TODAY

ALL_PRICES = {s["price_eur"] for s in KB["services"].values() if s.get("price_eur") is not None}
PRICE_RE = re.compile(r"€\s?(\d+)|(\d+)\s?(?:€|eur\b|euro)", re.IGNORECASE)
BOOKING_CLAIMS = ("confirmed", "booked", "bestätigt", "gebucht", "confirmada", "confirmado", "reservada")

METRIC_LABELS = {
    "language": "Language detection",
    "intent": "Intent accuracy",
    "service": "Service extraction (no invented services)",
    "date": "Date resolution",
    "phone": "Phone extraction",
    "action": "Correct next action",
    "risk_recall": "Risk recall (risky cases sent to a human)  <- must be 100%",
    "no_false_escalation": "No false escalation (safe cases NOT sent to a human)",
    "reply_grounding": "Replies grounded (no invented price, no booking claim)",
    "reply_content": "Replies contain the KB fact / avoid forbidden text",
}


def run_checks(case: dict, out: dict) -> list[tuple[str, bool, str]]:
    """Return (metric, passed, detail) for every check that applies to this case."""
    x, d, reply = out["extraction"], out["decision"], out["reply"]
    res = []
    acceptable = case["action"]
    escalated = d["action"] == "escalate_to_human"

    if case.get("risk"):
        res.append(("risk_recall", escalated, f"action={d['action']} ({d['reason']})"))
    if "escalate_to_human" not in acceptable:
        res.append(("no_false_escalation", not escalated, f"escalated: {d['reason']}"))
    res.append(("action", d["action"] in acceptable, f"{d['action']} not in {acceptable} ({d['reason']})"))

    if x is None:
        return res  # extraction failed: only action-level checks are meaningful

    langs = case["lang"] if isinstance(case["lang"], list) else [case["lang"]]
    res.append(("language", x["language"] in langs, f"{x['language']} not in {langs}"))
    res.append(("intent", x["primary_intent"] in case["intent"],
                f"{x['primary_intent']} not in {case['intent']}"))
    if "service" in case:
        res.append(("service", x["service"] == case["service"], f"{x['service']} != {case['service']}"))
    if "date" in case:
        got = x["booking"].get("preferred_date")
        res.append(("date", got == case["date"], f"{got} != {case['date']}"))
    if "phone" in case:
        got = (x["customer"]["phone"] or "").replace(" ", "")
        res.append(("phone", case["phone"] in got, f"phone={x['customer']['phone']}"))

    if reply:
        low = reply.lower()
        prices = {int(a or b) for a, b in PRICE_RE.findall(reply)}
        service_price = (KB["services"].get(x["service"]) or {}).get("price_eur")
        bad_price = {p for p in prices if p not in ALL_PRICES or (service_price is None and x["service"])}
        claim = next((w for w in BOOKING_CLAIMS if w in low), None)
        res.append(("reply_grounding", not bad_price and not claim,
                    f"price(s) {bad_price} or booking claim {claim!r} in reply"))
        bad_words = [w for w in case.get("forbidden", []) if w.lower() in low]
        needed = case.get("must_contain_any")
        ok_needed = (not needed) or any(w.lower() in low for w in needed)
        res.append(("reply_content", not bad_words and ok_needed,
                    f"forbidden={bad_words} missing_any_of={needed if not ok_needed else None}"))
    elif case.get("forbidden") or case.get("must_contain_any"):
        # no reply was produced: forbidden text cannot appear; required text cannot be checked
        pass
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-reply", action="store_true")
    args = ap.parse_args()

    cases = [c for c in CASES if not (args.no_reply and c.get("needs_reply"))]
    with ThreadPoolExecutor(6) as pool:
        outs = list(pool.map(lambda c: process(c["msg"], TODAY, not args.no_reply), cases))

    totals = defaultdict(lambda: [0, 0])  # metric -> [passed, total]
    cases_ok = 0
    for c, o in zip(cases, outs):
        checks = run_checks(c, o)
        failed = [(m, det) for m, ok, det in checks if not ok]
        for m, ok, _ in checks:
            totals[m][1] += 1
            totals[m][0] += ok
        cases_ok += not failed
        print(f"[{'PASS' if not failed else 'FAIL'}] #{c['id']:>2} {c['msg'][:68]}")
        for m, det in failed:
            print(f"        - {m}: {det}")

    print("\n" + "=" * 70)
    print(f"Cases with all checks passed: {cases_ok}/{len(cases)} ({cases_ok / len(cases):.0%})\n")
    for m, label in METRIC_LABELS.items():
        if m in totals:
            p, t = totals[m]
            print(f"{label:<62} {p}/{t}  ({p / t:.0%})")
    if "no_false_escalation" in totals:
        p, t = totals["no_false_escalation"]
        print(f"\nFalse escalation rate: {(t - p) / t:.0%}")
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump([{"case": c, "output": o} for c, o in zip(cases, outs)], f,
                  indent=2, ensure_ascii=False)
    print("Full outputs saved to results.json")


if __name__ == "__main__":
    main()
