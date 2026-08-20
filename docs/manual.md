# User Manual

This manual provides detailed instructions on how to leverage the core functionalities of the **Forex Analytics Dashboard** to perform daily, weekly, monthly, or quarterly CAD vs. USD currency analyses.

---

## 1. Filter Controls & Configuration
The filter panel at the top of the dashboard allows customizing the active dataset range:
*   **Start Date / End Date**: Controls the start and end of the analytics historical window. The database contains daily forex spot records from `2026-07-01` to `2026-08-14`.
*   **Aggregation Selection**:
    *   **Daily**: Plot raw daily spot exchange rates on the chart.
    *   **Weekly Average**: Aggregates filtered dates into weekly buckets and plots their average exchange rates.
    *   **Monthly Average**: Groups records by calendar month and calculates monthly exchange rate averages.
    *   **Quarterly Average**: Groups records by calendar quarter and calculates quarterly exchange rate averages.
*   **Apply Filter Button**: Commits and applies selected filters to both the bar chart and the detailed data table below.

---

## 2. Interactive Bar Chart
The Chart.js-powered visualization panel highlights trends within the filtered date range:
*   **Dynamic Labels**: The legend dynamically updates according to the active aggregation selection (e.g., "Daily Rate", "Weekly Average", etc.).
*   **Tooltips**: Hovering over any individual bar displays a precise popup listing the exact date/bucket and its exchange rate value in CAD per 1 USD.

---

## 3. Detailed Data Table
The data grid provides deep visibility into each individual record within the filtered range:
*   **Date**: Format is `YYYY-MM-DD`.
*   **Exchange Rate**: Direct exchange rate in CAD per 1 USD (matching the FRED DEXCAUS representation).
*   **Inverted Calculation**: Dynamically computed on-the-fly as `1 / rate` representing `USD per 1 CAD` (rounded to 4 decimal places).
*   **Market Status Badge**: Displays a green **"Market Open"** badge for active weekdays containing transaction rates, or a gray **"Market Closed"** badge for weekends or holidays where no active spot data exists.
