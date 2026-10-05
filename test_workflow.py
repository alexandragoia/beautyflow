"""Offline tests: no API key and no internet needed.   python test_workflow.py"""
import copy
from datetime import date

from beautyflow import KB, decide, lead_score, validate
from dates import resolve_date

MON = date(2026, 10, 5)  # a Monday


def d(expr, today=MON):
    r = resolve_date(expr, today)
    return r.isoformat() if r else None


def wd(day, week="unspecified"):
    return {"kind": "weekday", "weekday": day, "week": week}


def test_dates():
    assert d(wd("thursday")) == "2026-10-08"
    assert d(wd("monday")) == "2026-10-12"                      # same weekday => in 7 days
    assert d(wd("thursday", "next")) == "2026-10-15"            # following week
    assert d({"kind": "offset", "days": 0}) == "2026-10-05"
    assert d({"kind": "offset", "days": 1}) == "2026-10-06"
    assert d({"kind": "offset", "days": 2}) == "2026-10-07"
    assert d({"kind": "offset", "days": -1}) is None            # past dates rejected
    assert d({"kind": "absolute", "day": 15, "month": 10, "year": None}) == "2026-10-15"
    assert d({"kind": "absolute", "day": 3, "month": 10, "year": None}) == "2027-10-03"  # rolls over
    assert d({"kind": "absolute", "day": 31, "month": 2, "year": None}) is None          # invalid
    assert d({"kind": "absolute", "day": 29, "month": 2, "year": 2028}) == "2028-02-29"
    assert d({"kind": "weekday", "weekday": "blursday"}) is None
    assert d(None) is None and d("tomorrow") is None


def mk(**kw):
    x = dict(language="de", primary_intent="booking_request", service=None, service_text=None,
             service_ambiguous=False, risk={}, booking={"preferred_date": None})
    x.update(kw)
    return validate(x)


BOOK = {"requested": True, "preferred_date": "2026-10-08"}


def act(x, msg="", kb=KB):
    return decide(x, msg, kb)["action"]


def test_decisions():
    assert act(mk(service="powder_brows", booking=BOOK)) == "check_calendar"
    assert act(mk(service="haircut", booking=BOOK)) == "check_calendar"          # offered, no price: fine
    assert act(mk(service="powder_brows")) == "request_missing_information"       # no date
    assert act(mk(service_ambiguous=True, service_text="facial")) == "request_missing_information"
    assert act(mk(primary_intent="product_or_service_information", service_text="laser removal")) == "escalate_to_human"
    assert act(mk(primary_intent="pricing_request", service="microblading")) == "provide_pricing_information"
    assert act(mk(primary_intent="pricing_request", service="botox_treatment")) == "escalate_to_human"  # no price in KB
    assert act(mk(primary_intent="pricing_request")) == "request_missing_information"
    assert act(mk(primary_intent="cancellation_request")) == "handle_cancellation_workflow"
    assert act(mk(primary_intent="rescheduling_request")) == "handle_rescheduling_workflow"
    assert act(mk(primary_intent="general_information")) == "answer_information_request"
    assert act(mk(primary_intent="other")) == "request_missing_information"


def test_safety():
    assert act(mk(risk={"allergy_or_reaction": True})) == "escalate_to_human"
    assert act(mk(service="lash_lift", booking=BOOK), "ich bin schwanger") == "escalate_to_human"
    assert act(mk(service="lash_lift", booking=BOOK), "I take medication") == "escalate_to_human"
    assert act(mk(service="micropigmentation_correction", booking=BOOK)) == "escalate_to_human"
    assert act(mk(primary_intent="complaint")) == "escalate_to_human"
    assert act(mk(primary_intent="correction_request")) == "escalate_to_human"


def test_unsupported_service():
    kb = copy.deepcopy(KB)
    kb["services"]["haircut"]["offered"] = False
    assert act(mk(service="haircut", booking=BOOK), kb=kb) == "unsupported_service"
    kb2 = copy.deepcopy(KB)
    del kb2["services"]["haircut"]                                                # recognised, absent from KB
    assert act(mk(service="haircut", booking=BOOK), kb=kb2) == "unsupported_service"


def test_lead_score():
    full = mk(service="powder_brows", customer={"phone": "123"}, urgency=True,
              booking={"requested": True, "preferred_date": "2026-10-08", "time": "17:00"})
    assert lead_score(full) == 100                                                # capped
    assert lead_score(mk(primary_intent="general_information")) == 0
    assert lead_score(mk(primary_intent="pricing_request", service="manicure")) == 30


def test_knowledge_base():
    assert len(KB["services"]) == 32
    assert sum(1 for s in KB["services"].values() if s.get("price_eur") is not None) == 12
    assert KB["opening_hours"]["sunday"] == "closed"


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("OK  ", t.__name__)
    print(f"\nAll {len(tests)} test groups passed.")
