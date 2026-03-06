# Fiche — sql-advanced

---

## Session — 2026-02-25
Deep dive into window functions: ROW_NUMBER/RANK/DENSE_RANK distinctions, moving averages, FIRST_VALUE/LAST_VALUE, and the anti-join pattern.

### ROW_NUMBER vs RANK vs DENSE_RANK
All three assign a rank within a window partition, but differ in tie handling. ROW_NUMBER assigns a unique integer to every row with no tie logic — arbitrary among equals. RANK respects ties but skips subsequent positions (1, 1, 3). DENSE_RANK respects ties without skipping (1, 1, 2). When the ordering column has no duplicates, all three produce identical results.

### First-event-per-user pattern
To retrieve the first row per group, apply ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...) in a CTE, then filter WHERE order_rank = 1 in the outer query. Filtering cannot happen in the same query level because window functions are evaluated after WHERE.

### Window functions and GROUP BY cannot coexist in the same query level
Window functions are computed after GROUP BY in SQL's logical execution order (FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY). To combine aggregation with a window function, the aggregation must be done first in a CTE or subquery.

### ROWS vs RANGE frame specification
ROWS counts a fixed number of physical rows relative to the current row. RANGE operates on logical value boundaries — rows with equal ordering values are treated as a group. For time-series moving averages, ROWS BETWEEN N PRECEDING AND CURRENT ROW is almost always preferable because it gives a predictable, fixed-size window.

### LAST_VALUE requires explicit frame extension
The default window frame is UNBOUNDED PRECEDING to CURRENT ROW. With this default, LAST_VALUE returns the current row's value, not the last row in the partition. To get the true last value, the frame must be explicitly set to ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING. FIRST_VALUE is unaffected because the first row is always already within the default frame.

### FIRST_VALUE and LAST_VALUE for column-preserving lookups
When an exercise requires all rows to carry a reference value (e.g., first and last order amount per customer), FIRST_VALUE and LAST_VALUE with a full frame are the correct tool. A RANK + filter approach removes rows instead of adding columns, producing a different and incorrect result shape.

### Anti-join pattern with LEFT JOIN + IS NULL
To find rows in table A with no match in table B, use a LEFT JOIN from A to B, then filter WHERE b.key IS NULL. This is more readable and performant than HAVING COUNT(...) < 1. The NULL appears because unmatched left-side rows have no value from the right side.

### COUNT(*) vs COUNT(DISTINCT col)
COUNT(*) counts every row — use it when each row represents a distinct event. COUNT(DISTINCT col) deduplicates a column before counting — use it when the goal is to count unique entities rather than total occurrences. Concatenating two columns to create a synthetic distinct key is fragile due to collision risk and should be avoided.

### QUALIFY clause
QUALIFY filters rows after window functions are evaluated, analogous to how HAVING filters after GROUP BY. It allows filtering on window function results without a wrapping CTE. When using RANK or DENSE_RANK to select a top-N, the condition must use <= N, not < N, to include the Nth rank.

### LAG and LEAD
LAG retrieves the value from a preceding row within the partition; LEAD retrieves from a following row. The direction is controlled by the ORDER BY clause inside the window, not by switching between LAG and LEAD. Using LAG with ORDER BY DESC is equivalent to LEAD with ORDER BY ASC — duplicating both is redundant and produces duplicate column alias errors in BigQuery.
