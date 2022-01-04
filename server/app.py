import falcon
import json
import datetime


from falcon.http_status import HTTPStatus
from wsgiref import simple_server
from dataStore import *



class ItemResource:
    def on_get(self, req, resp):
        """Handles GET request for single item"""
        inputID = req.get_media()

        fetchedItem = datastore.get_item(inputID)

        dataStoreKeys = set(ITEMS.keys)
        idSet = set(inputID)

        if(id.issubset(dataStoreKeys)):
            if not fetchedItem:
                #item not found
                resp.status = falcon.http_404
            else:
                resp.media = fetchedItem
                resp.status = falcon.HTTP_200
        else:
            #invalid id supplied
            resp.status = falcon.HTTP_400
        resp.content_type = "application/json"
        

    def on_delete(self, req, resp):
        """Handles DELETE requests"""
        idToDelete = req.get_media()

        inputID = set(idToDelete)
        dataStoreKeys = set(ITEMS.keys)
        if(dataStoreKeys.issubset(inputID)):
            datastore.delete_item(idToDelete)
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
        

        
        resp.content_type = "application/json"


class MultipleItemsResource:
    def on_get(self, req, resp):
        """Handles GET request for multiple items"""

        fullFetchedData = []

        for i in range (len(ITEMS)):
            fullFetchedData.append(ITEMS[i])

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
        resp.set_header('Access-Control-Allow-Methods', 'POST')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        
        if req.method == 'OPTIONS':
            raise HTTPStatus(falcon.HTTP_204, text='\n')

    

app = falcon.API(middleware=[HandleCORS()])


app.add_route('/', rootResource())
app.add_route('/item', PostResource())
app.add_route('/item/{itemId}/', ItemResource())
app.add_route('/items', MultipleItemsResource())


if __name__ == '__main__':

    server = simple_server.make_server("0.0.0.0", 8000, app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass