# Quick Start Guide

Welcome to the **Forex Analytics Dashboard**! This interactive proof-of-concept application is designed to analyze CAD vs. USD exchange rates (matching the FRED DEXCAUS spot rate format).

Follow these quick steps to get up and running:

## 1. Opening the Application
Since this is a fully client-side, zero-dependency application, you can run it directly:
- Simply open the `index.html` file in any modern web browser (Chrome, Firefox, Safari, Edge, etc.).
- Or view the live deployed version hosted on GitHub Pages.

## 2. Interface Overview
Once opened, the dashboard displays:
- **Daily Exchange Rate Bar Chart**: Displays daily spot exchange rates (CAD per 1 USD) for the filtered date range.
- **Detailed Spot Rate Records**: A searchable, sortable list of daily rates with automatic inversion calculations (`USD per 1 CAD`).
- **Date Filter Panel**: Standard date pickers allowing you to restrict records to custom start/end dates, alongside an aggregation picker (Daily, Weekly, Monthly, Quarterly).

## 3. Restoring Defaults
If you change parameters and want to return to the original state:
- Click the **"Reset to Last Week"** button in the filter panel. This instantly restores the view to the last active 5-weekday market period (`2026-08-10` to `2026-08-14`).
