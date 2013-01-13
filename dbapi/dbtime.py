#!/usr/bin/env python3

import datetime

format_str = '%Y-%m-%d %H:%M:%S.%f'

def get_time_from_str(time_str):
    return datetime.datetime.strptime(time_str, format_str)
    
def make_time_str():
    return str(datetime.datetime.today())
