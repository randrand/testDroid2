testDroid2
==========
Android web service project 2.

Server: Python code; handle HTTP request from client, store the key/value pairs from client. Backend: google 
app engine (GAE) and NDB.

Client: Android Java code; send HTTP request to server.  Request can be a key/value pair to be stored, or 
a query key.


For example, we can use zipcode/weather as the key/value pair.

The client sends http requests to the server quering the weather for a given zipcode. The server runs on Google's
cloud servers (google app engine). It queries a NDB datastore with the zipcode as the key and sends back the 
weather info as JSON objects.

The client can also use HTTP POST to modify the data stored in the NDB datastore. The temperature information 
is contained in an url. Upon receiving the url, the server extracts the information and stores the data 
into the NDB datastore.

Andriod client UI is used for storing key/value pair, or inputing a query key.
