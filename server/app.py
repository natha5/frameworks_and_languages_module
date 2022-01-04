import falcon
import json
import datetime


from falcon.http_status import HTTPStatus
from wsgiref import simple_server
from dataStore import *



class ItemResource:
    def on_get(self, req, resp, itemId):
        """Handles GET request for single item"""
        
        fetchedItem = {}

        fetchedItem = datastore.get_item(itemId)

        if not fetchedItem:
            resp.status = falcon.HTTP_404
        else:
            resp.status = falcon.HTTP_200
            resp.media = fetchedItem
        resp.content_type = "application/json"

    def on_delete(self, req, resp, itemId):
        """Handles DELETE requests"""
        
        item = {}
        item = datastore.get_item(itemId)

        if not item:
            resp.status = falcon.HTTP_404
        else:
            datastore.delete_item(itemId)
            resp.status = falcon.HTTP_201
        

        
        resp.content_type = "application/json"


class MultipleItemsResource:
    def on_get(self, req, resp):
        """Handles GET request for multiple items"""

        fullFetchedData = []

        
        resp.status = falcon.HTTP_200
        resp.content_type = "application/json"
        resp.media = fullFetchedData


class PostResource:
    def on_post(self, req, resp):
        """Handles POST requests"""
        inputData ={}
        inputData = req.get_media()
        

        #create new values that arent inputted by user
        newDateFrom = datetime.datetime.now().isoformat
        newDateTo = datetime.datetime.now().isoformat

        newId = max(ITEMS.keys()) + 1

        ## check the correct fields have been filled

        neededFields = set({'user_id', 'keywords', 'description', 'lat', 'lon'})
        givenFields = set(inputData.keys())

        if(givenFields.issubset(neededFields)):
            inputData['dateFrom'] = newDateFrom
            inputData['dateTo'] = newDateTo
            inputData['id'] = newId

            datastore.create_item(inputData)
            
            resp.media = {'id' : newId}
            
            resp.content_type = "application/json"
            resp.status = falcon.HTTP_201
            
        else:
            resp.status = falcon.HTTP_405


class rootResource:
    def on_get(self, resp, req):
        resp.status = falcon.HTTP_200
        resp.content_type = "text/html"
        resp.text = "hello"
    

class OptionsResource:
    def on_options(self, req, resp):

        resp.status = falcon.HTTP_204
        resp.content_type = falcon.MEDIA_JSON


#cors handling adapted from https://github.com/falconry/falcon/issues/1220


class HandleCORS(object):
    def process_resource(self, req, resp, resource, req_succeeded):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'POST, DELETE, GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        
        if req.method == 'OPTIONS':
            raise HTTPStatus(falcon.HTTP_204, text='\n')

    

app = falcon.API(middleware=[HandleCORS()])


app.add_route('/', rootResource())
app.add_route('/item', PostResource())
app.add_route('/item/{itemId}', ItemResource())
app.add_route('/items', MultipleItemsResource())


if __name__ == '__main__':

    server = simple_server.make_server("0.0.0.0", 8000, app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass