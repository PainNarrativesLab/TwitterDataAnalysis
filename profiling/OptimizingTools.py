"""
Created by adam on 4/20/18
"""
__author__ = 'adam'
from functools import wraps
import time

from Loggers.CsvLoggers import log_query, log_query_timestamp
import environment


def time_and_log(fn):
    """
    Decorator to time operation of method
    From High Performance Python, p.27
    """
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        # elapsed = str(t2 - t1)
        # print(("@timefn:%s took %s seconds" % (fn.__name__, elapsed)))
        t2 = time.time()
        elapsed = t2 - t1
        log_query( elapsed )
        log_query_timestamp()
