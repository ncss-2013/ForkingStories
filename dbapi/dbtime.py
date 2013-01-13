#!/usr/bin/env python3

import datetime

format_str = '%Y-%m-%d %H:%M:%S.%f'

def get_time_from_str(time_str):
    return datetime.datetime.strptime(time_str, format_str)
    
def make_time_str(date=tuple()):
    '''Date can be (<year>, <month>, <day>)'''
    if not date:
        return datetime.datetime.today().strftime(format_str)
    else:
        return datetime.datetime(date[0], date[1], date[2]).strftime(format_str)

if __name__ == '__main__':
    assert get_time_from_str('2013-01-13 12:36:01.456000') == \
           datetime.datetime(2013, 1, 13, 12, 36, 1, 456000)
    assert get_time_from_str('2013-01-13 12:36:01.456000').second == 1
    assert make_time_str((1997, 12, 11)) == '1997-12-11 00:00:00.000000'
    assert isinstance(get_time_from_str(make_time_str((1997, 12, 11))),
                      datetime.datetime)
