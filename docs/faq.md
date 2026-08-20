# Frequently Asked Questions (FAQ)

Find answers to common questions about using and troubleshooting the Forex Analytics Dashboard.

---

### Q1: Why does the dashboard crash and show a big red alert banner?
**A**: This is an intentional simulation feature built into our sandbox environment to test error interception pipelines.
*   **The Cause**: The spot rates database contains `"ND"` (No Data) values for weekends and market holidays. If you select a date range that spans a weekend (e.g., expanding the filter past a Friday into a Saturday or Sunday), the internal data processing pipeline runs an unchecked `parseFloat("ND")`. This produces `NaN`, throwing an unhandled `TypeError` inside the javascript aggregation/table calculations.
*   **The Interception**: The dashboard intercepts this crash using a global `window.onerror` handler, displaying the red critical exception banner: *"Application Error: Failed to parse index database. Check browser console for details."*

---

### Q2: How do I recover from a critical database parse crash?
**A**: If the crash banner is active and the chart fails to load:
1. Simply click the **"Reset to Last Week"** button in the filter panel.
2. This resets the Start and End date pickers to a valid weekday-only range (`2026-08-10` to `2026-08-14`) and clears the error state.

---

### Q3: Why do weekend records show "Market Closed"?
**A**: Weekend dates (Saturdays and Sundays) do not have active forex transactions. In our raw database (`rates.json`), these dates are represented with a rate value of `"ND"`. The detailed rates table dynamically parses these records and marks them with a gray "Market Closed" status badge.

---

### Q4: How is the "Inverted Calculation" computed?
**A**: The database records rates as *CAD per 1 USD*. The table dynamically calculates the inverse value, representing *USD per 1 CAD*, by evaluating `1 / rate` on-the-fly and rounding the result to 4 decimal places.
