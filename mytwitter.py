#!/usr/bin/env python
# -*- conding: utf-8 -*-
"""
my twitter 
"""

import twitter
import datetime

from twitter_settings.py import *
from myjp import *

class MyTwitter:
  def __init__(self):
    self.api = twitter.Api(cache=None,consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

  def GetTwitterApi(self):
    return self.api


def main():
  mytwitter = MyTwitter()
  api  = mytwitter.GetTwitterApi()
  status = api.PostUpdate('Test from bot ' + datetime.datetime.now(JapanTZ()).strftime("%Y/%m/%d %H:%M:%S"))
  print status.text


if __name__ == "__main__":
  main()




