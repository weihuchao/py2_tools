#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-10-12 10:42
# @Author  : weihuchao

import datetime
import os
import time

CHRONOS_DEFAULT_TIME_ZONE = 8
CHRONOS_DEFAULT_TIME_ZONE_NAME = "CHRONOS_DEFAULT_TIME_ZONE"


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


# class ChronosUtils(object):
#
#     def __init__(self, *args):
#         self._stamp = 0
#         self._datetime = None
#         self._str = ""
#
#         self._table = ChronosTable(self)
#         self._auto_now = init_value == 0
#
#         if isinstance(init_value, datetime.datetime):
#             self._datetime = init_value
#             self.from_type = 3
#         else:
#             try:
#                 self._stamp = float(init_value)
#                 self.from_type = 1
#                 if self._stamp > 9999999999:
#                     self._stamp = self._stamp / 1000.0
#                 elif self._stamp <= 0:
#                     self._stamp = time.time()
#             except ValueError:
#                 self._str = init_value
#                 self.from_type = 2
#
#     @classmethod
#     def get_stamp(cls, *args):
#
#     def get_result(self, func_name, **kwargs):
#         return getattr(self, func_name)(**kwargs)
#
#     def int(self):
#         # self._check_table(1)
#         return int(self._stamp)
#
#     def float(self):
#         # self._check_table(1)
#         return self._stamp
#
#     def millisecond(self):
#         # self._check_table(1)
#         return int(self._stamp * 1000)
#
#     def str(self):
#         return self._str
#
#     def dt(self):
#         pass


# import requests
#
# requests.get()


class Chronos(object):
    """
    柯罗诺斯（古希腊语：Χρόνος；英语：Chronos）是古希腊神话中的一位原始神，代表着时间。
    """

    def __init__(self, *args, **kwargs):
        time_zone = kwargs.get("time_zone")
        if not time_zone:
            self.time_zone = os.environ.get(CHRONOS_DEFAULT_TIME_ZONE_NAME, CHRONOS_DEFAULT_TIME_ZONE)

        self.children = []
        for init_args in args or [0]:
            self.children.append(self._get_init_stamp(*init_args))

    def _get_init_stamp(self, init_value, format_str=None):
        if format_str:
            return time.mktime(time.strptime(init_value, format_str))
        else:
            if isinstance(init_value, datetime.datetime):
                return time.mktime(init_value.timetuple())
            else:
                try:
                    stamp = float(init_value)
                    if stamp > 9999999999:
                        stamp = stamp / 1000.0
                    elif stamp <= 0:
                        stamp = time.time()
                except ValueError:
                    return time.mktime(time.strptime(init_value, format_str))
                return stamp

    def _pack_single(self, func_name, **kwargs):
        ret = [child.get_result(func_name, **kwargs) for child in self.children]
        return ret[0] if self.single else ret

    # 处理函数
    # ---------

    def delta(self, year=0, month=0, day=0, hour=0, minute=0, second=0):
        delta_val = 0
        if year != 0:
            delta_val += year * 365 * 24 * 3600
        if month != 0:
            delta_val += month * 30 * 24 * 3600
        if day != 0:
            delta_val += day * 24 * 3600
        if hour != 0:
            delta_val += hour * 3600
        if minute != 0:
            delta_val += minute * 60
        if second != 0:
            delta_val += second

        self.children = [child + delta_val for child in self.children]

    # 输出函数
    # ---------
    def int(self, **kwargs):
        return self._pack_single("int", **kwargs)

    def float(self, **kwargs):
        return self._pack_single("float", **kwargs)

    def millisecond(self, **kwargs):
        return self._pack_single("millisecond")

    def str(self, **kwargs):
        return self._pack_single("str", **kwargs)

    def dt(self, **kwargs):
        return self._pack_single("dt", **kwargs)


"""
时间戳
时间字符串
datetime对象

所有计算都是以时间戳为基本


now = datetime.datetime.now()
time.mktime(now.timetuple())
"""


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
