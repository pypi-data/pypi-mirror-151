"""General module for parallelizing a dataframe apply function on a column (series) or entire row"""

import logging
from tokenize import group
from tqdm import tqdm
from multiprocessing import Pool
import numpy as np
import pandas as pd
from pandas.core.groupby.generic import DataFrameGroupBy
from typing import Callable
from functools import partial

tqdm.pandas()


def parallelize_dataframe(df: pd.DataFrame, func: Callable, n_cores: int) -> pd.DataFrame:
    """Function used to split a dataframe in n sub dataframes, based on the number of cores we want to use."""
    n_cores = min(len(df), n_cores)
    logging.debug(f"Parallelizing apply on df (rows: {len(df)}) with {n_cores} cores")
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df

def parallelize_groupby(df_grouped: DataFrameGroupBy, func: Callable, n_cores: int) -> pd.DataFrame:
    with Pool(n_cores) as p:
        ret_list = p.map(func, [group for _, group in df_grouped])
    return pd.concat(ret_list)


"""
Apply on series
Usage:
    standard => series.apply(f)
    serial   => apply_on_series(series, f)
    parallel => parallelize_dataframe(df, partial(apply_on_series, f=f), n_cores)
             => apply_on_series_parallel(series, f, n_cores)
    switch   => apply_on_series_maybe_parallel(series, f, true/false, n_cores)
"""

def apply_on_series(series: pd.Series, f: Callable, pbar: bool = True) -> pd.Series:
    if pbar:
        return series.progress_apply(f)
    else:
        return series.apply(f)


def apply_on_series_parallel(series: pd.Series, f: Callable, n_cores: int, pbar: bool = True) -> pd.Series:
    return parallelize_dataframe(series, partial(apply_on_series, f=f, pbar=pbar), n_cores)


def apply_on_series_maybe_parallel(series: pd.Series, f: Callable, parallel: bool,
                                   n_cores: int, pbar: bool = True) -> pd.Series:
    if parallel:
        return apply_on_series_parallel(series, f, n_cores, pbar)
    else:
        return apply_on_series(series, f, pbar)


"""
Apply on column
Usage:
    standard => df[col_name].apply(f)
    serial   => apply_on_df_col(df, col_name, f)
    parallel => parallelize_dataframe(df, partial(apply_on_df_col, col_name=col_name, f=f), n_cores)
             => apply_on_df_col_parallel(df, col_name, f, n_cores)
    switch   => apply_on_df_col_maybe_parallel(df, col_name, f, true/false, n_cores)
"""

def apply_on_df_col(df: pd.DataFrame, col_name: str, f: Callable, pbar: bool = True) -> pd.Series:
    """Simple wrapper on top of df[col].apply(x) using tqdm. Used by the parallel version of this process."""
    return apply_on_series(df[col_name], f, pbar)


def apply_on_df_col_parallel(df: pd.DataFrame, col_name: str, f: Callable,
                             n_cores: int, pbar: bool = True) -> pd.Series:
    """Function call the df.apply(f) chain in parallel """
    return apply_on_series_parallel(df[col_name], f, n_cores, pbar)

def apply_on_df_col_maybe_parallel(df: pd.DataFrame, col_name: str, f: Callable,
                                   parallel: bool, n_cores: int, pbar: bool = True):
    """Wrapper on top of apply_on_df_col"""
    return apply_on_series_maybe_parallel(df[col_name], f, parallel, n_cores, pbar)


"""
Apply on row
Usage:
    standard => df.apply(f, axis=1)
    serial   => apply_on_df(df, f)
    parallel => parallelize_dataframe(df, partial(apply_on_df, f=f), n_cores)
             => apply_on_df_parallel(df, f, n_cores)
    switch   => apply_on_df_maybe_parallel(df, f, true/false, n_cores)
"""

def apply_on_df(df: pd.DataFrame, f: Callable, pbar: bool = True) -> pd.Series:
    """Apply a function on each row (all possible columns), returning a series"""
    if pbar:
        return df.progress_apply(f, axis=1)
    else:
        return df.apply(f, axis=1)


def apply_on_df_parallel(df: pd.DataFrame, f: Callable, n_cores: int, pbar: bool = True) -> pd.Series:
    """Function to call df.apply(f, axis=1) in parallel on n cores"""
    return parallelize_dataframe(df, partial(apply_on_df, f=f, pbar=pbar), n_cores)


def apply_on_df_maybe_parallel(df: pd.DataFrame, f: Callable, parallel: bool,
                               n_cores: int, pbar: bool = True) -> pd.Series:
    """Wrapper on top of apply_on_df"""
    if parallel:
        return apply_on_df_parallel(df, f, n_cores, pbar)
    else:
        return apply_on_df(df, f, pbar)

"""
Apply on df.groupby
Usage:
    standard => df.groupby([cols]).apply(f)
    serial => apply_on_groupby_parallel(df.groubpy([cols]), f, n_cores)
"""

def _groupby_serial_func(data, func):
    return [func(x) for x in tqdm(data)]

def apply_on_groupby_parallel(df_grouped: DataFrameGroupBy, func: Callable, n_cores: int):
    assert isinstance(df_grouped, DataFrameGroupBy)
    grouped_data = []

    # groupby returns a tuple (key, sub_df), we only care about the sub_df. Other use-cases may appear later.
    for item in iter(df_grouped):
        grouped_data.append(item[1])

    n_cores = min(len(grouped_data), n_cores)
    split_data = np.array_split(grouped_data, n_cores)
    pool = Pool(n_cores)

    res = pool.map(partial(_groupby_serial_func, func=func), split_data)
    res = np.concatenate(res, dtype=object)
    res = pd.DataFrame(res)
    return res
