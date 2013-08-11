import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2
from django.utils import simplejson as json

MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/" method="post">
      <div><textarea name="content" rows="1" cols="60"></textarea></div>
      <div><input type="submit" value="Sign Guestbook"></div>
    </form>
  </body>
</html>
"""

class StoredData(ndb.Model):
    """datebase model"""
    zipcode = ndb.StringProperty(indexed=False)
    temperature = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

def guestbook_key(guestbook_name=""):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Guestbook', guestbook_name)


class MainPage(webapp2.RequestHandler):

    def get(self, tag):
        self.response.write(MAIN_PAGE_HTML)
        """
        guestbook_name = self.request.get(tag);
        
        
        # Query 
        # https://developers.google.com/appengine/docs/python/datastore/queryclass
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        #greetings = greetings_query.fetch(10)
        if greetings_query:
            value = greetings_query.fetch(1)
        else:
            value = "-inf"
        if self.request.get('fmt') == "html":
            WritePhoneOrWeb(self, lambda : json.dump(["VALUE", tag, value], self.response.out))
        """

    def post(self):
        
        self.response.write('<html><body>You wrote:<pre>')
        self.response.write(cgi.escape(self.request.get('content')))
        self.response.write('</pre></body></html>')
        
        # Inert new entry into the database
        # https://developers.google.com/appengine/docs/python/tools/webapp/requestclass
        zipcodeIn = self.request.get('zipcode', '-inf');
        newEntry = StoredData(parent=guestbook_key(zipcodeIn))
        newEntry.zipcode = zipcodeIn
        newEntry.temperature = self.request.get('temperature', '-inf');
        newEntry.date = self.request.get('date', '-inf');
        newEntry.put()
        #query_params = {'zipcode': zipcodeIn}


class StoreAValue(webapp2.RequestHandler):
    def store_a_value(self, tag, value):
        entry = self.request.get('zipcode', '-inf')
        if entry:
            entry.temperature = value
        else: 
            entry = StoredData(zipcode = tag, temperature = value)
        entry.put()
        ## Send back a confirmation message.  The TinyWebDB component ignores
        ## the message (other than to note that it was received), but other
        ## components might use this.
        result = ["STORED", tag, value]
        WritePhoneOrWeb(self, lambda : json.dump(result, self.response.out))

    def post(self):
        zipcodeIn = self.request.get('tag')
        tempIn = self.request.get('value')
        self.store_a_value(zipcodeIn, tempIn)

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

        
#### Utilty procedures for generating the output

#### Write response to the phone or to the Web depending on fmt
#### Handler is an appengine request handler.  writer is a thunk
#### (i.e. a procedure of no arguments) that does the write when invoked.
def WritePhoneOrWeb(handler, writer):
    if handler.request.get('fmt') == "html":
        WritePhoneOrWebToWeb(handler, writer)
    else:
        handler.response.headers['Content-Type'] = 'application/jsonrequest'
        writer()

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

        

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/storeavalue', StoreAValue),
], debug=True)


"""

class MainPage(webapp2.RequestHandler):
    
    
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('''
    <html><body>
    <form action="/storeavalue" method="post"
          enctype=application/x-www-form-urlencoded>
       <p>Tag<input type="text" name="tag" /></p>
       <p>Value<input type="text" name="value" /></p>
       <input type="hidden" name="fmt" value="html">
       <input type="submit" value="Store a value">
    </form></body></html>\n''')




application = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=False)

"""
