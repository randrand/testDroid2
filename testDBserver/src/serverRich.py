
###
### This is a web service for use with App
### Inventor for Android (<http://appinventor.googlelabs.com>)
### This particular service stores and retrieves tag-value pairs 
### using the protocol necessary to communicate with the TinyWebDB
### component of an App Inventor app.


### Author: David Wolber (wolber@usfca.edu), using sample of Hal Abelson

#import logging
#from cgi import escape
##from google.appengine.ext import webapp
##from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
#from google.appengine.ext.db import Key
#from django.utils import simplejson as json
import webapp2
import json
#import cgi
#import urllib

MAIN_PAGE_HTML = """\
<html>
  <body>
    <a href="storeavalue">StoreValue </a>
    </br>
    <a href="getvalue">QueryValue </a>
  </body>
</html>
"""

class StoredData(db.Model):
  tag = db.StringProperty()
  value = db.StringProperty(multiline=True)
  ## defining value as a string property limits individual values to 500
  ## characters.   To remove this limit, define value to be a text
  ## property instead, by commnenting out the previous line
  ## and replacing it by this one:
  ## value db.TextProperty()
  date = db.DateTimeProperty(required=True, auto_now=True)



class StoreAValue(webapp2.RequestHandler):

  def store_a_value(self, tag, value):
    # There's a potential readers/writers error here :(
    entry = db.GqlQuery("SELECT * FROM StoredData where tag = :1", tag).get()
    if entry:
      entry.value = value
    else: entry = StoredData(tag = tag, value = value)
    entry.put()
    ## Send back a confirmation message.  The TinyWebDB component ignores
    ## the message (other than to note that it was received), but other
    ## components might use this.
    #result = ["STORED", tag, value]
    #WritePhoneOrWeb(self, lambda : json.dump(result, self.response.out))

  def post(self):
    tag = self.request.get('tag')
    value = self.request.get('value')
    self.store_a_value(tag, value)

  def get(self):
    self.response.out.write('''
    <html><body>
    <form action="/storeavalue" method="post"
          enctype=application/x-www-form-urlencoded>
       <p>Tag<input type="text" name="tag" /></p>
       <p>Value<input type="text" name="value" /></p>
       <input type="hidden" name="fmt" value="html">
       <input type="submit" value="Store a value">
    </form></body></html>\n''')

class GetValue(webapp2.RequestHandler):

  def get_value(self, tag):
    entry = db.GqlQuery("SELECT * FROM StoredData where tag = :1", tag).get()
    if entry:
      value = entry.value
    else: value = ""
    ## We tag the returned result with "VALUE".  The TinyWebDB
    ## component makes no use of this, but other programs might.
    ## check if it is a html request and if so clean the tag and value variables
    #if self.request.get('fmt') == "html":
      #value = escape(value)
      #tag = escape(tag)
    WritePhoneOrWeb(self, lambda : json.dump(["VALUE", tag, value], self.response.out))

  def post(self):
    tag = self.request.get('tag')
    self.get_value(tag)

  def get(self):
    self.response.out.write('''
    <html><body>
    <form action="/getvalue" method="post"
          enctype=application/x-www-form-urlencoded>
       <p>Tag<input type="text" name="tag" /></p>
       <input type="hidden" name="fmt" value="html">
       <input type="submit" value="Get value">
    </form></body></html>\n''')
    
#### Utilty procedures for generating the output

#### Write response to the phone or to the Web depending on fmt
#### Handler is an appengine request handler.  writer is a thunk
#### (i.e. a procedure of no arguments) that does the write when invoked.
def WritePhoneOrWeb(handler, writer):
  #if handler.request.get('fmt') == "html":
  #  WritePhoneOrWebToWeb(handler, writer)
  #else:
    handler.response.headers['Content-Type'] = 'application/jsonrequest'
    writer()

"""
#### Result when writing to the Web
def WritePhoneOrWebToWeb(handler, writer):
  handler.response.headers['Content-Type'] = 'text/html'
  handler.response.out.write('<html><body>')
  handler.response.out.write('''
  <em>The server will send this to the component:</em>
  <p />''')
  writer()
  WriteWebFooter(handler, writer)


#### Write to the Web (without checking fmt)
def WriteToWeb(handler, writer):
  handler.response.headers['Content-Type'] = 'text/html'
  handler.response.out.write('<html><body>')
  writer()
  WriteWebFooter(handler, writer)

def WriteWebFooter(handler, writer):
  handler.response.out.write('''
  <p><a href="/">
  <i>Return to Game Server Main Page</i>
  </a>''')
  handler.response.out.write('</body></html>')

### A utility that guards against attempts to delete a non-existent object
#def dbSafeDelete(key):
#  if db.get(key) :  db.delete(key)
"""



class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write(MAIN_PAGE_HTML)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/storeavalue', StoreAValue),
    ('/getvalue', GetValue),
    ], debug=True)

