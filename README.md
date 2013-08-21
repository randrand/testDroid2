testDroid2
==========
Android web service project 2.

Server: Python code; handle HTTP request from client, store the key/value pairs from client. Backend: google 
app engine (GAE) and NDB.

Client: Android Java code; send HTTP request to server.  Request can be a key/value pair to be stored, or 
a query key.


For example, we can use zipcode/weather as the key/value pair.

The client sends http request to the server quering the weather for a given zipcode. The server queries
the NDB datastore with the zipcode as the key and sends back the weather info as JSON objects.

The client uses HTTP GET to modify the data stored in the NDB datastore. The temperature information 
is contained in a url. Upon receiving the url, the server extracts the information and store the data 
into the NDB datastore.

Example usage:

After deploying the app into GAE, url1 can display the history weather information in JSON array format. 
url2 can be used as HTTP POST request that mofidifies the weather information in NDB.

url1: http://dearbabymaimai.appspot.com/query?zipcode=53705

url2: http://dearbabymaimai.appspot.com/modify?zipcode=53705&temp=90&date=08212013
