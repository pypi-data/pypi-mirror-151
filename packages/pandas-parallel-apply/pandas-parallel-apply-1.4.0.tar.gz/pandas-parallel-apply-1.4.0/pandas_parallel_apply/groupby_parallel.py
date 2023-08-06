from typing import Callable
from pandas.core.groupby.generic import DataFrameGroupBy
from .pandas_parallel_apply import apply_on_groupby_parallel

class GroupByParallel:
    def __init__(self, df_grouped: DataFrameGroupBy, n_cores: int, pbar: bool = True):
        self.df_grouped = df_grouped
        self.n_cores = n_cores
        self.pbar = pbar
    
    def apply(self, func: Callable):
        return apply_on_groupby_parallel(self.df_grouped, func, self.n_cores, self.pbar)
