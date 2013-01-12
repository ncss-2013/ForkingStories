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
    
def make_time_float():
    return time.time()
