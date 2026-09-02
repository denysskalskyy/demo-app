# Frequently Asked Questions (FAQ)

Find answers to common questions about using and troubleshooting the Forex Analytics Dashboard.

---

### Q1: Why do weekend or holiday dates show "Market Closed" instead of a rate?
**A**: The spot rates database contains `"ND"` (No Data) values for weekends and market holidays.
*   **Classification**: Each loaded record is classified once as either a market-open numeric record or a market-closed record. Market-closed records are excluded from chart aggregation and the inverted-rate calculation.
*   **Display**: Market-closed records remain visible in the detailed table with a gray "Market Closed" badge and no inverted value. Filtering a range that spans a weekend or holiday (e.g. `2026-08-03` to `2026-08-14`) no longer triggers the application error banner.

---

### Q2: What happens if a filtered range has no market-open records?
**A**: The chart shows an empty-state message instead of a bar chart, and the table still lists the market-closed rows. Click the **"Reset to Last Week"** button in the filter panel to return to the default active weekday range (`2026-08-10` to `2026-08-14`).

---

### Q3: Why do weekend records show "Market Closed"?
**A**: Weekend dates (Saturdays and Sundays) do not have active forex transactions. In our raw database (`rates.json`), these dates are represented with a rate value of `"ND"`. The detailed rates table dynamically parses these records and marks them with a gray "Market Closed" status badge.

---

### Q4: How is the "Inverted Calculation" computed?
**A**: The database records rates as *CAD per 1 USD*. The table dynamically calculates the inverse value, representing *USD per 1 CAD*, by evaluating `1 / rate` on-the-fly and rounding the result to 4 decimal places.
