from google.appengine.ext import ndb
import cgi 
import json
import urllib 
import webapp2

# ndb entry for key/value store
class WeatherEntry(ndb.Model):
  zipcode = ndb.StringProperty()
  # date = ndb.StringProperty()
  temp = ndb.StringProperty()
  dateTime = ndb.DateTimeProperty(auto_now=True)

  # Using zipcode as the query key
  @classmethod
  def queryZip(cls, zip):
    return cls.query( cls.zipcode==zip) #.order(-cls.dateTime)

# Query from HTTP POST message
class QueryWeather(webapp2.RequestHandler):
   def post(self):
      zipcode = self.request.get('zipcode')
      weaths = WeatherEntry.queryZip(zipcode).fetch(20)
      self.response.out.write(len(weaths))
      self.response.headers['Content-Type'] = 'application/json'  
      for weath in weaths: 
         obj = {
           'zipcode': weath.zipcode, 
           #'date': weath.date,
           'temperature' : weath.temp
         } 
         self.response.out.write(json.dumps(obj))
     
# Store request from HTTP POST message
class InsertWeather(webapp2.RequestHandler):  
  def post(self):
    zip = self.request.get('zipcode')
    temp = self.request.get('temp')
    #date = self.request.get('date')
    weath = WeatherEntry(parent=ndb.Key("weather", "yea"))
    weath.zipcode=zip
    #weath.date=date
    weath.temp=temp
    weath.put()

# Structure of server website 
application = webapp2.WSGIApplication([
  ('/query', QueryWeather),
  ('/modify', InsertWeather),
], debug=True)
