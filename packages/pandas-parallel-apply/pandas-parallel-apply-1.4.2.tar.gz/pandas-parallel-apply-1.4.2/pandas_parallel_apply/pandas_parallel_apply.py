"""General module for parallelizing a dataframe apply function on a column (series) or entire row"""

import logging
from typing import Callable, Union, List
from functools import partial
import numpy as np
import pandas as pd
from tqdm import tqdm
from pathos.multiprocessing import cpu_count, ProcessingPool as Pool
from pandas.core.groupby.generic import DataFrameGroupBy
from pandas.core.indexes.multi import MultiIndex
tqdm.pandas()


def parallelize_dataframe(df: pd.DataFrame, func: Callable, n_cores: int) -> pd.DataFrame:
    """Function used to split a dataframe in n sub dataframes, based on the number of cores we want to use."""
    n_cores = min(cpu_count(), len(df), n_cores)
    logging.debug(f"Parallelizing apply on df (rows: {len(df)}) with {n_cores} cores")
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    pool_res = pool.map(func, df_split)
    df = pd.concat(pool_res)
    return df

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

def _groupby_serial_func(data: List, func: Callable, pbar: bool = True) -> List:
    _range = tqdm(data) if pbar else data
    return [func(x) for x in _range]

def _get_multi_index_key(concat_res, key_data):
    new_key_data = []
    for i in range(len(concat_res)):
        # An awesome (KEY_1, 1), (KEY_2, 2), ..., (KEY_N, K) kind of deal
        n_keys = len(concat_res[i])
        multi_key = n_keys * [key_data[i]]
        counter_key = concat_res[i].index
        new_key = tuple(zip(multi_key, counter_key))
        new_key_data.extend(new_key)
    key_data = MultiIndex.from_tuples(new_key_data)
    return key_data

def apply_on_groupby_parallel(df_grouped: DataFrameGroupBy, func: Callable, n_cores: int, pbar: bool = True,
                              keep_original_indexes: bool = False) -> Union[pd.DataFrame, pd.Series]:
    if n_cores == 1:
        logging.info("n_cores is set to 1, returning serial apply.")
        return df_grouped.apply(func)

    grouped_data = []
    key_data = []
    for item in iter(df_grouped):
        key_data.append(item[0])
        grouped_data.append(item[1])
    # This is here to suppress warnings
    grouped_data = np.array(grouped_data, dtype=object)
    n_cores = min(cpu_count(), len(grouped_data), n_cores)
    split_data = np.array_split(grouped_data, n_cores)

    # Run the multi-process job
    pool = Pool(n_cores)
    pool_res = pool.map(partial(_groupby_serial_func, func=func, pbar=pbar), split_data)

    # Concatenate the result to preserve the original result of a regular groupby pandas code.
    concat_res = []
    for i in range(len(pool_res)):
        concat_res.extend(pool_res[i])

    if isinstance(concat_res[0], pd.Series):
        res = pd.DataFrame(concat_res)
    elif isinstance(concat_res[0], pd.DataFrame):
        res = pd.concat(concat_res)
        # SLOWS DOWN BY A LOT, LIKE 5x SERIAL TIME. TO INVESTIGATE
        if keep_original_indexes:
            key_data = _get_multi_index_key(concat_res, key_data)
        else:
            key_data = np.arange(len(res))
    else:
        res = pd.Series(concat_res)

    # Fix the index
    res.index = key_data
    res.index.name = df_grouped.keys
    return res
