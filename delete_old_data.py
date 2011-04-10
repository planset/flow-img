#!/usr/bin/env python
# encoding: utf-8
"""
delete_old_data.py

Created by planset on 2011-04-10.
Copyright (c) 2011 Daisuke Igarashi. All rights reserved.
"""

import datetime

from google.appengine.ext import db

def DeleteOldData():
    """
    1時間前以前のデータを全て削除する。
    """
    cnt = 1000
    while cnt == 1000:
        q = db.GqlQuery("SELECT * "
                        + " FROM InstaData "
                        + " WHERE created_at < :1"
                        , datetime.datetime.now() - datetime.timedelta(hours=1))
        results = q.fetch()
        cnt = len(results)
        db.delete(results)
    
if __name__ == '__main__':
    DeleteOldData()

