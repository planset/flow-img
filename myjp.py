#!/usr/bin/env python
# encoding: utf-8
"""
myjp.py

Created by planset on 2011-04-10.
Copyright (c) 2011 Daisuke Igarashi. All rights reserved.
"""

import datetime

class JapanTZ(datetime.tzinfo):
  def tzname(self, dt):
    return "JST"
  def utcoffset(self, td):
    return datetime.timedelta(hours=9)
  def dst(self, dt):
    return datetime.timedelta(0)
