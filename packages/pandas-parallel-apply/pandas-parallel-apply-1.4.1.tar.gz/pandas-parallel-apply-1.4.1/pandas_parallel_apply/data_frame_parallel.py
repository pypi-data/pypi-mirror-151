"""Wrapper on top of pd.DataFrame with some parallel operations"""
from multiprocessing import Pool
import pandas as pd
from .pandas_parallel_apply import apply_on_df_parallel
from .series_parallel import SeriesParallel

class DataFrameParallel:
    def __init__(self, df: pd.DataFrame, n_cores: int, pbar: bool = True):
        self._n_cores = None
        self.df = df
        self.n_cores = n_cores
        self.pbar = pbar

    def apply(self, func, axis, raw: bool = False, result_type = None, args=(), **kwargs):
        assert axis == 1
        return apply_on_df_parallel(self.df, func, self.n_cores, self.pbar)

    def __getitem__(self, x):
        return SeriesParallel(self.df[x], self.n_cores, self.pbar)

    def __str__(self) -> str:
        f_str = f"[Parallel DataFrame - {self.n_cores} crores]\n" + self.df.__str__()
        return f_str
