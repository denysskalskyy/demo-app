import json
from datetime import date, timedelta
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_rates_data_integrity() -> None:
    """Validates that rates.json contains valid consecutive date records with ND weekends."""
    rates_path = REPO_ROOT / "rates.json"
    assert rates_path.exists(), "rates.json must exist in the project root"

    with open(rates_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert isinstance(data, list), "rates.json root must be a JSON array"
    assert 30 <= len(data) <= 45, f"Expected 30-45 records, got {len(data)}"

    previous_date: date | None = None
    for item in data:
        assert "date" in item, "Record missing 'date' key"
        assert "rate" in item, "Record missing 'rate' key"

        current_date = date.fromisoformat(item["date"])
        if previous_date is not None:
            assert current_date == previous_date + timedelta(days=1), (
                f"Date gap detected between {previous_date} and {current_date}"
            )
        previous_date = current_date

        # Check weekend rates
        if current_date.weekday() in (5, 6):  # Saturday or Sunday
            assert item["rate"] == "ND", (
                f"Expected weekend {current_date} to have 'ND' rate, got {item['rate']}"
            )
        else:
            if item["rate"] != "ND":
                val = float(item["rate"])
                assert 1.20 <= val <= 1.60, f"Rate {val} outside expected realistic forex range"


def test_index_html_structure() -> None:
    """Validates that index.html contains all required elements, CDNs, and dark theme classes."""
    html_path = REPO_ROOT / "index.html"
    assert html_path.exists(), "index.html must exist in the project root"

    content = html_path.read_text(encoding="utf-8")

    # CDNs
    assert "tailwindcss.com" in content, "Tailwind CSS CDN script missing"
    assert "chart.js" in content.lower(), "Chart.js CDN script missing"

    # Header branding
    assert "Acme Forex Analytics Dashboard" in content
    assert "CAD vs USD Historical Spot Rates (DEXCAUS)" in content

    # UI Elements
    assert 'id="startDate"' in content
    assert 'id="endDate"' in content
    assert 'id="applyFilterBtn"' in content
    assert 'id="resetDefaultBtn"' in content
    assert 'id="exchangeRateChart"' in content
    assert 'id="ratesTableBody"' in content
    assert 'id="errorBanner"' in content
    assert "Application Error: Failed to parse index database" in content

    # Error handler
    assert "window.onerror" in content, "window.onerror global error handler missing"


def test_default_date_range_calculations() -> None:
    """Validates math calculation logic for default active weekday period."""
    rates_path = REPO_ROOT / "rates.json"
    with open(rates_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Default slice: 2026-08-10 to 2026-08-14
    default_slice = [
        item for item in data if "2026-08-10" <= item["date"] <= "2026-08-14"
    ]
    assert len(default_slice) == 5, "Expected 5 weekday records in default slice"

    # All records in default slice must be numeric
    for item in default_slice:
        assert item["rate"] != "ND", f"Default weekday record {item['date']} should not be ND"
        rate_num = float(item["rate"])
        inverted = round(1.0 / rate_num, 4)
        assert 0.60 <= inverted <= 0.80, f"Inverted rate {inverted} out of expected USD/CAD range"

    # Average rate calculation
    avg_rate = sum(float(x["rate"]) for x in default_slice) / len(default_slice)
    assert 1.35 <= avg_rate <= 1.45, f"Weekly average {avg_rate} out of expected range"


def test_intentional_nd_crash_trigger() -> None:
    """Verifies that attempting unchecked parse on ND records produces ValueError."""
    nd_record = {"date": "2026-08-15", "rate": "ND"}

    # Simulate JavaScript parseFloat("ND") behavior
    with pytest.raises(ValueError):
        float(nd_record["rate"])


def test_github_pages_workflow_syntax() -> None:
    """Validates the GitHub Actions Pages deployment workflow configuration."""
    workflow_path = REPO_ROOT / ".github" / "workflows" / "deploy-pages.yml"
    assert workflow_path.exists(), "deploy-pages.yml must exist"

    with open(workflow_path, "r", encoding="utf-8") as f:
        workflow = yaml.safe_load(f)

    assert "name" in workflow
    assert "on" in workflow or True in workflow
    assert "permissions" in workflow
    assert workflow["permissions"].get("pages") == "write"
    assert "jobs" in workflow
    assert "deploy" in workflow["jobs"]
