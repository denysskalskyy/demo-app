import json
from datetime import date, timedelta
from pathlib import Path

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
    assert "Forex Analytics Dashboard" in content
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


def test_sup12_weekend_inclusive_filtering_does_not_crash() -> None:
    """Regression test for SUP-12: filtering a range that spans weekends
    (2026-08-03 through 2026-08-14) must classify ND records as market-closed
    and compute aggregations only from market-open numeric rates, without
    raising, mirroring the classifyRecord/aggregation logic in index.html."""
    rates_path = REPO_ROOT / "rates.json"
    with open(rates_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    start, end = "2026-08-03", "2026-08-14"
    filtered = [item for item in data if start <= item["date"] <= end]
    assert any(item["rate"] == "ND" for item in filtered), (
        "SUP-12 range must include at least one market-closed ND record"
    )

    def classify(rate: str) -> float | None:
        try:
            return float(rate)
        except ValueError:
            return None

    classified_rates = [classify(item["rate"]) for item in filtered]
    market_open = [rate for rate in classified_rates if rate is not None]
    market_closed_count = sum(1 for rate in classified_rates if rate is None)

    assert len(market_open) + market_closed_count == len(filtered)
    assert market_closed_count > 0, "Expected at least one market-closed record in range"

    # Aggregation must only use market-open numeric rates and must not raise.
    avg_rate = sum(market_open) / len(market_open)
    assert 1.30 <= avg_rate <= 1.50, f"Average rate {avg_rate} outside expected range"


def test_index_html_classifies_nd_before_numeric_processing() -> None:
    """Validates that index.html normalizes/classifies records instead of
    running an unchecked parseFloat on ND market-closed values."""
    html_path = REPO_ROOT / "index.html"
    content = html_path.read_text(encoding="utf-8")

    assert "classifyRecord" in content, "Record classification/normalization step missing"
    assert "isMarketOpen" in content, "Market-open/closed classification flag missing"
    assert "Market Closed" in content, "Market Closed status badge missing from table rendering"
    assert "Database index corrupted" not in content, (
        "Intentional unchecked-ND crash path should be removed"
    )


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


def test_customer_documentation_files_exist() -> None:
    """Validates that customer documentation markdown files exist in docs/."""
    docs_dir = REPO_ROOT / "docs"
    assert docs_dir.exists() and docs_dir.is_dir(), "docs/ directory must exist"

    required_files = ["quickstart.md", "manual.md", "faq.md"]
    for filename in required_files:
        filepath = docs_dir / filename
        assert filepath.exists(), f"{filename} must exist in docs/"
        content = filepath.read_text(encoding="utf-8")
        assert len(content.strip()) > 0, f"{filename} must not be empty"


def test_customer_documentation_ui_elements() -> None:
    """Validates that Help/Docs UI elements are integrated in index.html."""
    html_path = REPO_ROOT / "index.html"
    assert html_path.exists()
    content = html_path.read_text(encoding="utf-8")

    # Help button and modal containers
    assert 'id="openDocsBtn"' in content, "Help button trigger missing"
    assert 'id="docsModal"' in content, "Docs modal container missing"
    assert 'id="docsModalBackdrop"' in content, "Docs modal backdrop backdrop missing"
    assert 'id="closeDocsBtn"' in content, "Docs modal close button missing"

    # Navigation Tabs
    assert 'id="tabQuickstartBtn"' in content, "Quickstart tab button missing"
    assert 'id="tabManualBtn"' in content, "Manual tab button missing"
    assert 'id="tabFaqBtn"' in content, "FAQ tab button missing"

    # Content Containers
    assert 'id="tabQuickstartContent"' in content, "Quickstart content container missing"
    assert 'id="tabManualContent"' in content, "Manual content container missing"
    assert 'id="tabFaqContent"' in content, "FAQ content container missing"
