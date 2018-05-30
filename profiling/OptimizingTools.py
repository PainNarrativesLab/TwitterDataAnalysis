"""
Created by adam on 4/20/18
"""
import csv
import datetime
import environment
__author__ = 'adam'
from functools import wraps
import time

from Loggers.CsvLoggers import log_query, log_query_timestamp, log_request, log_request_timestamp
import Loggers.SlackNotifications as Slack

def standard_timestamp():
    """Returns a timestamp in the format to be used in all instrumenation"""
    return datetime.datetime.isoformat( datetime.datetime.now() )

def format_standard_timestamp(datetime_obj):
    return datetime.datetime.isoformat(datetime_obj)

def time_and_log_query( fn ):
    """
    Decorator to time operation of method
    From High Performance Python, p.27
    """

    @wraps( fn )
    def measure_time( *args, **kwargs ):
        t1 = time.time()
        result = fn( *args, **kwargs )
        t2 = time.time()
        elapsed = t2 - t1
        log_query( elapsed )
        log_query_timestamp()
        #         print(("@timefn:%s took %s seconds" % (fn.__name__, elapsed)))
        return result

    return measure_time


def time_and_log_request( fn ):
    """
    Decorator to time operation of method
    From High Performance Python, p.27
    """

    @wraps( fn )
    def measure_time( *args, **kwargs ):
        t1 = time.time()
        result = fn( *args, **kwargs )
        t2 = time.time()
        elapsed = t2 - t1
        log_request( elapsed )
        log_request_timestamp()
        #         print(("@timefn:%s took %s seconds" % (fn.__name__, elapsed)))
        return result

    return measure_time


def log_func_start( fn ):
    """
    Decorator to time operation of method
    From High Performance Python, p.27
    """

    @wraps( fn )
    def measure_time( *args, **kwargs ):
        t1 = time.time()
        result = fn( *args, **kwargs )
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


def timestamped_count_writer( logFile, count, text=None ):
    ts = standard_timestamp()
    with open( logFile, 'a' ) as csvfile:
        writer = csv.writer( csvfile )
        writer.writerow( [ ts, count, text ] )


def write_start_stop( logFile, start, stop, count=None, text=None ):
    """Writes the current timestamp to a csv log file"""
    with open( logFile, 'a' ) as csvfile:
        writer = csv.writer( csvfile )
        if count is not None:
            writer.writerow( [ start, stop, count, text ] )
        else:
            writer.writerow( [ start, stop ] )


def log_start_stop( log_files, text=None, notify_slack=environment.SLACK_NOTIFY ):
    """Decorator which logs the timestamp of when the function
    starts and the timestamp of when the function stops to a csv file
    """

    def rd( fn ):
        def wrapper( *args, **kwargs ):
            t1 = datetime.datetime.now()
            result = fn( *args, **kwargs )
            t2 = datetime.datetime.now()
            # if type(log_files) is not list: log_files = [log_files]
            for f in log_files:
                write_start_stop( f, format_standard_timestamp(t1), format_standard_timestamp(t2), result, text )
            if notify_slack:
                delta = t2 - t1
                runtime = round(delta.total_seconds()/60, 2)
                msg = "Processing complete \n Runtime = %s minutes \n Records = %s \n %s" % (runtime, result, text)
                Slack.send_slack_update(msg)

            return result

        return wrapper

    return rd
