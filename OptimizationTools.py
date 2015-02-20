"""
This contains various tools for testing and optimizing
"""
import time
from functools import wraps


def timefn(fn):
    """
    Decorator to time operation of method
    From High Performance Python, p.27
    """
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        elapsed = str(t2 - t1)
        print("@timefn:%s took %s seconds" % (fn.func_name, elapsed))