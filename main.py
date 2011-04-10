# coding: UTF-8

import settings

from flask import Flask
app = Flask(__name__)
app.config.from_object('settings')

from flask import g
from flask import redirect
from flask import url_for
from flask import session
from flask import request
from flask import Response
from flask import render_template
from flask import abort
from flask import flash
from flask import get_flashed_messages
from flask import json
import logging

from decorators import login_required, cache_page

from models import User
from models import InstaData

from gaeUtils.util import generate_key
from google.appengine.api.labs import taskqueue
from google.appengine.api import images

from google.appengine.ext import db

def getInstaData(since_id=0):
    if since_id == 0:
        q = db.GqlQuery("SELECT * FROM InstaData WHERE instagram_id > :1 ORDER BY instagram_id DESC", str(since_id))
        results = q.fetch(10, 30)
    else:
        q = db.GqlQuery("SELECT * FROM InstaData WHERE instagram_id > :1 ORDER BY instagram_id ASC", str(since_id))
        results = q.fetch(1)
    
    return results

@app.before_request
def before_request():
    """
    if the session includes a user_key it will also try to fetch
    the user's object from memcache (or the datastore).
    if this succeeds, the user object is also added to g.
    """
    if 'user_key' in session:
        user = cache.get(session['user_key'])

        if user is None:
            # if the user is not available in memcache we fetch
            # it from the datastore
            user = User.get_by_key_name(session['user_key'])

            if user:
                # add the user object to memcache so we
                # don't need to hit the datastore next time
                cache.set(session['user_key'], user)

        g.user = user
    else:
        g.user = None



@app.route('/img/<string:key>')
def getImage(key):
    app.logger.debug(key)
    data = db.get(key)
    if not data:
        #self.error(404)
        return Response(status="404")
    #self.response.headers["Content-Type"] = "image/jpg"
    #self.response.out.write()
    return Response(response=data.thumbnail,content_type=data.content_type)

@app.route('/getNewItem')
def getNewItem():
    since_id = request.args.get("since_id", 0)
    data = getInstaData(int(since_id))
        
    if len(data) > 0:
        since_id = data[0].instagram_id
        
    return render_template("_item.html", data=data, since_id=since_id)


@app.route('/list')
def list():
    """
    renders the list page template
    """
    data = getInstaData()
    return render_template("list.html", data=data)

@app.route('/')
def index():
    """
    renders the index page template
    """
    return list()

