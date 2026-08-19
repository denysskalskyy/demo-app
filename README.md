# Acme Forex Analytics Dashboard

A responsive, single-page CAD vs. USD Spot Rate Analytics Dashboard built with Tailwind CSS and Chart.js, designed as a human-governed sandbox application.

## Overview
- **Data Source**: Historical daily CAD vs USD exchange rate data (FRED DEXCAUS).
- **Core Visualizations**:
  - Weekly Average Bar Chart with bounded Y-axis.
  - Detailed Data Table with on-the-fly inverted calculations (`USD / CAD = 1 / rate`) and Market Status badges.
- **Period Filter**: Interactive Start/End date pickers defaulting to the last active 5-weekday period (`2026-08-10` to `2026-08-14`).
- **Intentional Test Sandbox Flaw**: Unhandled `"ND"` weekend rate parsing trigger with global `window.onerror` red banner interception.
- **Deployment**: Configured for continuous deployment to GitHub Pages via GitHub Actions.

## File Structure
- `rates.json`: 45 consecutive days of CAD vs USD rates, with `"ND"` representing weekends and market holidays.
- `index.html`: Modern dark-themed dashboard frontend.
- `.github/workflows/deploy-pages.yml`: GitHub Actions deployment pipeline for GitHub Pages.
- `tests/test_dashboard.py`: Automated test suite for data validation, DOM structure, calculation math, and crash triggers.

## Testing & Quality Checks
```bash
# Run unit and integration tests
uv run pytest

# Run static linting
uv run ruff check

# Run type checking
uv run mypy tests
```
