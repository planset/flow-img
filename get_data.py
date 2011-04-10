#!/usr/bin/env python
# -*- conding: utf-8 -*-
"""
"""

import twitter
import datetime
import time
import re
import urllib
import logging

from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import urlfetch

from models import InstaData, SinceData

from twitter_settings import *
from myjp import *

class MyTwitter:
    def __init__(self):
        self.api = twitter.Api(cache=None,consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

    def GetTwitterApi(self):
      return self.api

def getInstagramTweet(api, since_id):
    words = "instagr.am"
    try:
        if since_id > 0:
            return api.GetSearch(term=words, since_id=since_id, per_page=10)
    except twitter.TwitterError:
        pass

    return api.GetSearch(term=words)


def getSinceData():
    q = db.GqlQuery("SELECT * FROM SinceData LIMIT 1")
    results = q.fetch(1)
    for p in results:
        return p

    d = None
    d = SinceData(since_id=0)
    key = d.put()
    return SinceData.get(key)

def _getData():
    q = db.GqlQuery("SELECT * "
                    + " FROM InstaData "
                    + " ORDER BY date DESC"
                    )
    results = q.fetch(10)
    return results

def addData(id, twitter_screen_name, twitter_name, twitter_message, url, created_at):
    p = InstaData()
    p.instagram_id = id
    p.twitter_url = ""
    p.twitter_name = twitter_screen_name
    if twitter_name is not None and len(twitter_name) > 0:
        p.twitter_name += "(" + twitter_name + ")"
    p.twitter_message = twitter_message
    p.url = url
    p.image_url = getImageURL(url)
    p.thumbnail = getThumbnailImage(p.image_url)
    p.content_type = "image/jpg"
    p.created_at = datetime.datetime.strptime(created_at, "%a, %d %b %Y %H:%M:%S +0000")
    p.put()
    
def getImageURL(url):
    regex = re.compile(r'<img src="(.*.jpg)"')
    try:
        f = urllib.urlopen(url)
        try:
            ss = f.read()
            o = regex.search(ss)
            logging.info(o)
            if o:
                return o.group(1)
        finally:
            f.close()
    finally:
        pass
        
    return ""

def getThumbnailImage(image_url):
    try:
        img = images.Image(urlfetch.fetch(image_url).content)
        img.resize(100, 100)
        return img.execute_transforms(output_encoding=images.JPEG)

    finally:
        pass

def getData():
    mytwitter = MyTwitter()
    api  = mytwitter.GetTwitterApi()

    sinceData = getSinceData()

    statuses = getInstagramTweet(api, sinceData.since_id)

    regex = re.compile(r"(http://instagr.am/\w*/\S*/)")
    for s in statuses:
        # logging.info(s.id)
#         logging.info(s.user.name)
#         logging.info(s.user.screen_name)
#         logging.info(s.created_at)
#         logging.info(s.text)

        o = regex.search(s.text)
        if o is not None:
            addData(s.id, s.user.screen_name, s.user.name, s.text, o.group(1), s.created_at)

	sinceData.since_id = statuses[len(statuses) - 1].id + 1
	sinceData.put()


if __name__ == "__main__":
    getData()




