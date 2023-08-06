# pandas-parallel-apply

`df.apply(fn)`, `df[col].apply(fn)` and `series.apply(fn)` wrappers with tqdm included

## Installation

`pip install pandas-parallel-apply`

## Examples
See `examples/` for usage on some dummy dataframe and series.

## Usage

## 1. Procedural

### Apply on each row of a dataframe

`df.apply(fn)` -> `apply_on_df_parallel(df: pd.DataFrame, fn: Callable, n_cores: int, pbar: bool = True)`

### Apply on a column of a dataframe and return the Series

`df[col].apply(fn, axis=1)` -> `apply_on_df_col_parallel(df: pd.DataFrame, col_name: str, fn: Callable, n_cores: int, pbar: bool = True)`

### Apply on a series and return the modified Series
`series.apply(fn)` -> `apply_on_seris_parallel(series: pd.Series, fn: Callable, n_cores: int, pbar: bool = True)

### Switches for boolean parallel/non-parallel

`apply_on_df/df_col/series_maybe_parallel(*, parallel: bool, n_cores: int, pbar: bool = True)`

## 2. Object Oriented Programming

### Apply on each row of a dataframe

`df.apply(fn)` -> `DataFrameParallel(df, n_cores: int, pbar: bool = True).apply(fn)`

### Apply on a column of a dataframe and return the Series
`df[col].apply(fn, axis=1)` -> `DataFrameParallel(df, n_cores: int, pbar: bool=True)[col].apply(fn, axis=1)`

### Apply on a series
`series.apply(fn)` -> `SeriesParallel(series, n_cores: int, pbar: bool=True).apply(fn)`

That's all.
