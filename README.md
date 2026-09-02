# Forex Analytics Dashboard

A responsive, single-page CAD vs. USD Spot Rate Analytics Dashboard built with Tailwind CSS and Chart.js, designed as a human-governed sandbox application.

## Overview
- **Data Source**: Historical daily CAD vs USD exchange rate data (FRED DEXCAUS).
- **Core Visualizations**:
  - Weekly Average Bar Chart with bounded Y-axis.
  - Detailed Data Table with on-the-fly inverted calculations (`USD / CAD = 1 / rate`) and Market Status badges.
- **Period Filter**: Interactive Start/End date pickers defaulting to the last active 5-weekday period (`2026-08-10` to `2026-08-14`).
- **Market-Closed Handling**: Weekend/holiday `"ND"` records are classified as market-closed, shown in the table with a "Market Closed" badge, and excluded from chart aggregation. A global `window.onerror` handler remains in place for unexpected errors.
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

## Coding agent workflow

The `Coding Agent` GitHub Actions workflow implements issues after a maintainer applies
the `state:triage-in-progress` label. It requires a repository Actions secret named
`CLAUDE_CODE_OAUTH_TOKEN`.

Each run creates a branch named `issue-<number>-<title-slug>`. The title slug contains
the first five words of the issue title. The agent makes one Conventional Commit in this
format:

```text
<type>: <concise imperative summary> (Issue #<number>)
```

The type must be `feat`, `fix`, `test`, `docs`, or `chore`. The workflow runs the test,
lint, and type-check commands above after the agent finishes. When all checks pass, it
opens a ready pull request against `main` with `Closes #<number>` in the body. Repeated
runs reuse an existing open pull request for the same branch. The workflow does not
change issue labels.
