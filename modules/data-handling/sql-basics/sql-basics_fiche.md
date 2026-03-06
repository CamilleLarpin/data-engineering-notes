
## 2026-02-24
- Date formatting: `FORMAT_DATE('%m-%y', date_column)` for custom string representations (%Y=2023, %y=23, %m=07, %B=July, %b=Jul)
- Date filtering: direct comparisons (`date >= '2023-01-01'`) more efficient than `EXTRACT`/`FORMAT_DATE` on partitioned tables (enables partition pruning)
- Number formatting: `FORMAT('$%.2f', TRUNC(amount, 2))` for currency display; `TRUNC` cuts without rounding vs `ROUND` which rounds
- `FORMAT()` returns string (not numeric), use `ROUND()` for continued calculations
- No built-in season function - seasons are hemisphere-dependent, requiring custom `CASE WHEN` logic
- `CASE WHEN` in SQL equivalent to dictionary mapping pattern in Python for discrete value transformations

---

## Session — 2026-02-24
BigQuery date functions, formatting, and CASE WHEN for derived categorical columns.

### Extracting Date Components
`FORMAT_DATE('%m-%y', date_col)` returns a formatted string from a date. `EXTRACT(MONTH FROM date_col)` and `EXTRACT(YEAR FROM date_col)` return numeric components. Format codes: `%Y` = 4-digit year, `%y` = 2-digit year, `%m` = month number, `%b` = abbreviated month name, `%B` = full month name.

### Filtering on Dates — Performance Consideration
Filtering with direct range comparisons (`WHERE date_col >= '2023-01-01' AND date_col < '2023-02-01'`) allows BigQuery to use partition pruning — skipping entire partitions not in range. Wrapping the column in `EXTRACT()` or `FORMAT_DATE()` forces a full scan and prevents pruning.

### Numeric Formatting
`TRUNC(x, 2)` truncates to 2 decimal places without rounding. `ROUND(x, 2)` rounds to 2 decimal places. `FORMAT('$%.2f', x)` returns a formatted string with a dollar sign and 2 decimal places — the result is a string, not a number, so it cannot be used in further calculations.

### CASE WHEN for Derived Categories
BigQuery has no built-in function for season extraction. A `CASE WHEN` block mapping month ranges to season labels is the standard approach. `CASE WHEN` is structurally equivalent to if/elif/else in Python, or the dict-as-switch pattern for discrete value mapping.
