# Fiche — productionizing-ml-code

---

## Session — 2026-03-09
Data pipeline design and stateful vs stateless transformations in an ML codebase

### Stateless vs stateful transforms
Stateless transforms are deterministic and require no learned parameters (e.g. dropping rows with impossible values, casting dtypes). Stateful transforms learn parameters from training data (e.g. imputation fills missing values with the training mean; scaling computes min/max from training data; OHE records the set of categories seen during training) and must apply those same learned parameters at prediction time.

### Imputation
Replaces missing values with a statistic derived from the training set (e.g. column mean). Applying it independently at prediction time would use different statistics, producing inconsistent features.

### Scaling
Rescales numerical features to a common range using parameters (min, max, mean, std) computed on training data. Recomputing on new data at prediction time would shift the feature distribution.

### One-Hot Encoding (OHE)
Converts a categorical column into binary indicator columns, one per category observed in training. The category set must be fixed at training time.

### Why stateful transforms belong in model.py
Sklearn Pipelines bundle the ColumnTransformer (preprocessing) and the estimator into a single object. Fitting, saving, and loading that single object guarantees that the same learned parameters are applied at both train and predict time. Splitting stateful transforms across multiple files requires saving multiple objects in sync, increasing the risk of inconsistency.

### Logging configuration requirement
Python's `logging` module only emits messages if a handler is configured. Calling `logging.basicConfig(level=logging.INFO)` before running a module ensures log output appears. Without it, `python -m module` produces no visible output even when logger calls exist in the code.

### if __name__ == '__main__' block
Code under this guard runs only when the file is executed directly (e.g. `python -m package.module`), not when imported. It is the correct place to add `logging.basicConfig` for smoke-testing a module from the command line.

### DataFrame mutability
Pandas functions like `drop_duplicates()` return a new DataFrame by default; they do not modify the original in place. The result must be assigned to a variable to observe the effect.
