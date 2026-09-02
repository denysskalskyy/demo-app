# Frequently Asked Questions (FAQ)

Find answers to common questions about using and troubleshooting the Forex Analytics Dashboard.

---

### Q1: Why do some dates show "Market Closed" instead of a rate?
**A**: The spot rates database contains `"ND"` (No Data) values for weekends and market holidays.
*   **Classification**: Before any calculations run, the dashboard classifies each record as either market-open (a valid numeric rate) or market-closed (`"ND"`).
*   **Table display**: Market-closed records are still shown in the detailed table with a gray "Market Closed" badge, and no inverted calculation is attempted for them.
*   **Chart aggregation**: Daily, weekly, monthly, and quarterly chart aggregations only use market-open numeric rates, so a filter range spanning a weekend or holiday (e.g. `2026-08-03` to `2026-08-14`) renders correctly without errors.

---

### Q2: What does the "Reset to Last Week" button do?
**A**: Click the **"Reset to Last Week"** button in the filter panel to restore the Start and End date pickers to the default active weekday range (`2026-08-10` to `2026-08-14`) and clear any prior error state.

---

### Q3: Why do weekend records show "Market Closed"?
**A**: Weekend dates (Saturdays and Sundays) do not have active forex transactions. In our raw database (`rates.json`), these dates are represented with a rate value of `"ND"`. The detailed rates table dynamically parses these records and marks them with a gray "Market Closed" status badge.

---

### Q4: How is the "Inverted Calculation" computed?
**A**: The database records rates as *CAD per 1 USD*. The table dynamically calculates the inverse value, representing *USD per 1 CAD*, by evaluating `1 / rate` on-the-fly and rounding the result to 4 decimal places.
