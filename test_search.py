"""Offline tests for free-text search extraction validation."""
from datetime import date

from search_logic import normalize_filters, parse_model_output


TODAY = date(2026, 10, 8)


def test_normalize_filters():
    assert normalize_filters({
        "zip": "10115", "service": "french", "budget_eur": 50, "date": "2026-10-09"
    }, TODAY) == {
        "zip": "10115", "service": "french", "budget_eur": 50, "date": "2026-10-09"
    }


def test_reject_invalid_filters():
    assert normalize_filters({
        "zip": "90210", "service": "invented", "budget_eur": True, "date": "2026-01-01"
    }, TODAY) == {"zip": None, "service": None, "budget_eur": None, "date": None}
    assert normalize_filters({"budget_eur": 1001, "date": "not-a-date"}, TODAY) == {
        "zip": None, "service": None, "budget_eur": None, "date": None
    }


def test_parse_model_output():
    result = parse_model_output(
        '{"reply":"Ich suche passende Beispielstudios.","filters":{"zip":"10115","service":"french","budget_eur":50,"date":"2026-10-09"}}',
        TODAY,
    )
    assert result["reply"].startswith("Ich suche")
    assert result["filters"]["service"] == "french"


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
        print("OK  ", test.__name__)
    print(f"\nAll {len(tests)} search test groups passed.")
