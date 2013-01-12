#!/usr/bin/env python3
'''Contains some conveinience functions for managing datetimes.

These functions should be used internally across the entire dbapi.

Written by Alex Mueller

'''

import datetime
import time

format_str = '%Y-%m-%d %H:%M:%S.%f'

def create_datetime(time_float):
    return datetime.datetime.fromtimestamp(float(time_float))
    
def make_time_float(date=tuple()):
    '''Returns in seconds since epoch. Calulates now if time = ().
Otherwise, you can calulate a certain date by specifying
(year, month, day)

'''
    if not date:
        return time.time()
    else:
        return (datetime.date(date[0], date[1], date[2]) -
                datetime.date(1970, 1, 1)).total_seconds()
