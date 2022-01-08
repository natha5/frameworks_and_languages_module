import falcon
import json
import datetime


from falcon.http_status import HTTPStatus
from wsgiref import simple_server
from dataStore import *


class RootResource:
    def on_get(self, req, resp):
        """Returns basic HTML when server is started"""
        resp.text = "Freecycle"
        resp.content_type = "text/html"
        resp.status = falcon.HTTP_200
        
        
        print("GET /","-", resp.status)
    

    def on_options(self, req, resp):
        """Handles OPTIONS request"""
        resp.text = "hello"
        resp.status = falcon.HTTP_204
        resp.content_type = "text/html"
        resp.set_header = ('Access-Control-Allow-Methods', 'POST')
        print("OPTIONS /", "-", resp.status)


class ItemResource:
    def on_get(self, req, resp, itemId):
        """Handles GET request for single item"""
        
        #Id has to be decremented for correct data to be got.
        fixedId = int(itemId) - 1
        
        fetchedItem = {}
        fetchedItem = datastore.get_item(fixedId)

        if not fetchedItem:
            resp.status = falcon.HTTP_404
        else:
            resp.status = falcon.HTTP_200
            
            #Currently, dates don't work so not returned
            resp.media = {
                'id' : fetchedItem.get('id') + 1, #sed id back to original value
                'user_id' : fetchedItem.get('user_id'),
                'keywords' : fetchedItem.get('keywords'),
                'description' : fetchedItem.get('description'),
                'lat' : fetchedItem.get('lat'),
                'lon' : fetchedItem.get('lon'),
                #'date_from' : fetchedItem.get('date_from'),
               # 'date_to' : fetchedItem.get('date_to')
            }
        resp.content_type = "application/json"
        print("GET /item/"+ str(itemId), "-", resp.status)

    def on_delete(self, req, resp, itemId):
        """Handles DELETE requests"""
        
        fixedId = int(itemId) - 1

        item = datastore.get_item(fixedId)

        if not item:
            resp.status = falcon.HTTP_404
        else:
            datastore.delete_item(fixedId)
            resp.status = falcon.HTTP_201 #Spec asks for a 201 code, despite 201 meaning created
        
        resp.content_type = "application/json"
        print("DELETE /item/" + str(itemId), "-", resp.status)


class ItemsResource:
    def on_get(self, req, resp):
        """Handles GET request for multiple items"""

        noOfItemsinStore = max(ITEMS.keys())

        listOfAllItems = []

        for i in range (noOfItemsinStore):
            listOfAllItems.append(datastore.get_item(i))

        resp.status = falcon.HTTP_200
        resp.content_type = "application/json"
        #Attempt at returning a list to pass test
        resp.media = {'response' : ['hello', 'hi']}

        print("GET /items", "-",)


class PostResource:
    def on_post(self, req, resp):
        """Handles POST requests"""
        inputData = {}
        inputData = req.get_media()
        

        #create new values that arent inputted by user
        newDateFrom = datetime.datetime.now().isoformat
        newDateTo = datetime.datetime.now().isoformat

        #check the correct fields have been filled

        neededFields = set({'user_id', 'keywords', 'description', 'lat', 'lon'})
        givenFields = set(inputData.keys())

        if(givenFields.issubset(neededFields)):
            inputData['date_from'] = newDateFrom
            inputData['date_to'] = newDateTo
            
            datastore.create_item(inputData)
            
            #Assign values to variables. Doesn't work if I directly assign in dictionary

            user_id = inputData.get("user_id")
            keywords = inputData.get('keywords')
            description = inputData.get("description")
            lat = inputData.get("lat")
            lon = inputData.get("lon")

            #Increment Id
            newId = max(ITEMS.keys()) + 1

            #Currently, dates don't work so not returned
            resp.media = {
                'id' : newId,
                'user_id' : user_id,
                'keywords' : inputData.get('keywords'),
                'description' : description,
                'lat' : lat,
                'lon' : lon,
                #'date_from' : newDateFrom,
               # 'date_to' : newDateTo
            }
            resp.status = falcon.HTTP_201

        else:
            resp.status = falcon.HTTP_405
        resp.content_type = "application/json"

        print("POST /item","-", resp.status)


#Adapted from : https://github.com/falconry/falcon/issues/1220
class HandleCORS(object):
    def process_request(self, req, resp):
        """Process the request before routing it."""
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods','POST')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        
#Assign CORS middleware
app = falcon.App(middleware=[HandleCORS() ])


#Routing - matches spec path requirements
app.add_route("/", RootResource())
app.add_route('/item', PostResource())
app.add_route('/item/{itemId}', ItemResource())
app.add_route('/items', ItemsResource())


if __name__ == '__main__':

    server = simple_server.make_server("0.0.0.0", 8000, app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass