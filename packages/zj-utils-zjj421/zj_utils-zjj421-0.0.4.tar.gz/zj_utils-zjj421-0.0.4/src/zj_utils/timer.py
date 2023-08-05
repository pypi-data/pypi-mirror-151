#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by zj on 2020/10/13 
# Task: 

from datetime import datetime
import time


class MyTimer(object):
    def __init__(self):
        self.restart()

    def restart(self):
        self.start_time = time.time()

    def elapsed(self, restart=False, unit='ms'):
        assert unit in ('us', 'ms', 's', 'min')
        duration = (time.time() - self.start_time)
        if unit == 'us':
            duration = duration * 1e6
        elif unit == 'ms':
            duration = duration * 1e3
        elif unit == 's':
            duration = duration
        elif unit == 'min':
            duration = duration / 60
        if restart:
            self.restart()
        return duration

    def log(self, tip='Elapsed time', unit='ms', reset=True):
        duration = round(self.elapsed(reset, unit), 3)
        print('{}: {}{}'.format(tip, duration, unit))
        return duration

    def rlog(self, tip='Elapsed time'):

        return self.log(unit='ms', reset=True, tip=tip)


MYTIMER_ = MyTimer()


def runtime(func):
    def wrapper(*args, **kw):
        MYTIMER_.restart()
        ret = func(*args, **kw)
        MYTIMER_.rlog(f'func "{func.__name__}" run time')
        return ret

    return wrapper


def main():
    timer = MyTimer()
    sum = 0
    for i in range(int(10e6)):
        sum += i

    # timer.log(unit='us', reset=False)
    timer.log(unit='ms', reset=False)
    timer.log(unit='s', reset=False)
    # timer.log(unit='min', reset=False)


if __name__ == '__main__':
    start = datetime.now()
    print("Start time is {}".format(start))
    main()
    end = datetime.now()
    print("End time is {}".format(end))
    print("\nTotal running time is {}s".format((end - start).seconds))
    print("\nCongratulations!!!")
