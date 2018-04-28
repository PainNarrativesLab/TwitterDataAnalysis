"""
Created by adam on 4/20/18
"""
import csv
import datetime

__author__ = 'adam'
from functools import wraps
import time

from Loggers.CsvLoggers import log_query, log_query_timestamp, log_request, log_request_timestamp

import environment


def standard_timestamp():
    """Returns a timestamp in the format to be used in all instrumenation"""
    return datetime.datetime.isoformat( datetime.datetime.now() )

def time_and_log_query(fn):
    """
    Decorator to time operation of method
    From High Performance Python, p.27
    """
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        elapsed = t2 - t1
        log_query( elapsed )
        log_query_timestamp()
        #         print(("@timefn:%s took %s seconds" % (fn.__name__, elapsed)))
        return result
    return measure_time

def time_and_log_request(fn):
    """
    Decorator to time operation of method
    From High Performance Python, p.27
    """
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        elapsed = t2 - t1
        log_request( elapsed )
        log_request_timestamp()
        #         print(("@timefn:%s took %s seconds" % (fn.__name__, elapsed)))
        return result
    return measure_time


def log_func_start(fn):
    """
    Decorator to time operation of method
    From High Performance Python, p.27
    """
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        elapsed = t2 - t1
        log_request( elapsed )
        log_request_timestamp()
        #         print(("@timefn:%s took %s seconds" % (fn.__name__, elapsed)))
        return result
    return measure_time


def timestamp_writer( logFile ):
    """Writes the current timestamp to a csv log file"""
    ts = standard_timestamp()
    with open( logFile, 'a' ) as csvfile:
        writer = csv.writer( csvfile )
        writer.writerow( [ ts ] )


def write_start_stop( logFile, start, stop ):
    """Writes the current timestamp to a csv log file"""
    with open( logFile, 'a' ) as csvfile:
        writer = csv.writer( csvfile )
        writer.writerow( [ start, stop ] )


def log_start_stop(log_files):
    """Decorator which logs the timestamp of when the function
    starts and the timestamp of when the function stops to a csv file
    """
    def rd(fn):
        def wrapper(*args, **kwargs):
            t1 = standard_timestamp()
            result = fn(*args, **kwargs)
            t2 = standard_timestamp()
            # if type(log_files) is not list: log_files = [log_files]
            for f in log_files:
                write_start_stop(f, t1, t2)
            return result
        return wrapper
    return rd
