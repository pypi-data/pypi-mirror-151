from typing import Callable
import pandas as pd

from .pandas_parallel_apply import apply_on_series_parallel

class SeriesParallel:
    def __init__(self, series: pd.Series, n_cores: int, pbar: bool = True):
        self.series = series
        self.n_cores = n_cores
        self.pbar = pbar
    
    def apply(self, func: Callable) -> pd.Series:
        return apply_on_series_parallel(self.series, func, self.n_cores, self.pbar)
