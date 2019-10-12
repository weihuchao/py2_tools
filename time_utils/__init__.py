#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-10-12 10:42
# @Author  : weihuchao

import datetime
import time


class ChronosTable(object):

    def __init__(self, chronos):
        self._chronos = chronos

    def transform(self, from_type, to_type):
        # if from_type == 1:
        #     if self._chronos._stamp == 0:
        #         self._chronos.now()
        # elif from_type == 2:
        #     if not self._chronos._str:
        #         self.
        pass

    def _one_to_one(self):
        pass

    def _one_to_two(self):
        pass

    def _one_to_three(self):
        pass




class Chronos(object):
    """
    柯罗诺斯（古希腊语：Χρόνος；英语：Chronos）是古希腊神话中的一位原始神，代表着时间。
    """

    def __init__(self, init_value=0, time_zone=None):
        self._stamp = 0
        self._datetime = None
        self._str = ""

        self._time_zone = time_zone
        self._table = ChronosTable(self)
        self._auto_now = init_value == 0

        if isinstance(init_value, datetime.datetime):
            self._datetime = init_value
            self.from_type = 3
        else:
            try:
                self._stamp = float(init_value)
                self.from_type = 1
                if self._stamp > 9999999999:
                    self._stamp = self._stamp / 1000.0
                elif self._stamp <= 0:
                    self._stamp = time.time()
            except ValueError:
                self._str = init_value
                self.from_type = 2

    def _check_table(self, to):
        self._table.transform(self.from_type, to)

    def int(self):
        # self._check_table(1)
        return int(self._stamp)

    def float(self):
        # self._check_table(1)
        return self._stamp

    def millisecond(self):
        # self._check_table(1)
        return int(self._stamp * 1000)

    def str(self):
        return self._str


class ChronosShip(object):
    STR_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self):
        self.stamp = 0
        self.datetime = None
        self.str = ""

    # def _stamp_to_str(self, stamp=0):
    #     if stamp:
    #         self.stamp = stamp
    #     else:
    #         self.now()
    #
    #     self.datetime = datetime.datetime.fromtimestamp(self.stamp)
    #     return self.datetime.strftime(self.STR_FORMAT)

    def _str_to_stamp(self):
        pass

    def _stamp_to_datetime(self):
        self.datetime = datetime.datetime.fromtimestamp(self.stamp)

    def _stamp_to_str(self):
        self.str = self.datetime.strftime(self.STR_FORMAT)

    def int(self):
        return


if __name__ == '__main__':
    print Chronos().int()
    print Chronos().float()
    print Chronos().millisecond()
