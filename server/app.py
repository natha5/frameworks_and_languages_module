import falcon
import json
import datetime


from falcon.http_status import HTTPStatus
from wsgiref import simple_server
from dataStore import *



class ItemResource:
    def on_get(self, req, resp, itemId):
        """Handles GET request for single item"""
        
        fixedId = int(itemId) - 1
        
        fetchedItem = {}
        fetchedItem = datastore.get_item(fixedId)

        if not fetchedItem:
            resp.status = falcon.HTTP_404
        else:
            resp.status = falcon.HTTP_200
            resp.media = {"id" : fetchedItem.get('id') + 1}
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


class MultipleItemsResource:
    def on_get(self, req, resp):
        """Handles GET request for multiple items"""

        noOfItemsinStore = max(ITEMS.keys())

        dictOfAllItems = {}

        for i in range (noOfItemsinStore):
            dictOfAllItems[i] = datastore.get_item(i)


        
        resp.status = falcon.HTTP_200
        resp.content_type = "application/json"
        resp.media = dictOfAllItems

        print("GET /items", "-",)


class PostResource:
    def on_post(self, req, resp):
        """Handles POST requests"""
        inputData ={}
        inputData = req.get_media()
        

        #create new values that arent inputted by user
        newDateFrom = datetime.datetime.now().isoformat
        newDateTo = datetime.datetime.now().isoformat

        

        ## check the correct fields have been filled

        neededFields = set({'user_id', 'keywords', 'description', 'lat', 'lon'})
        givenFields = set(inputData.keys())

        if(givenFields.issubset(neededFields)):
            inputData['date_from'] = newDateFrom
            inputData['date_to'] = newDateTo
            
            datastore.create_item(inputData)
            
            newId = max(ITEMS.keys()) + 1
            
            

            resp.media = {'id' : newId}
            
            resp.content_type = "application/json"
            resp.status = falcon.HTTP_201


            
        else:
            resp.status = falcon.HTTP_405

        print("POST /item","-", resp.status)


class rootResource:
    def on_get(self, resp, req):
        resp.status = falcon.HTTP_200
        resp.content_type = "text/html"
        resp.text = "hello"
        print("GET /","-", resp.status)
    
    def on_options(self, req, resp):
        resp.text = "hello"
        resp.status = falcon.HTTP_204
        resp.content_type = "text/html"
        resp.methods = 'POST, GET, DELETE'
        print("OPTIONS /", "-", resp.status)


#cors handling adapted from https://github.com/falconry/falcon/issues/1220



    
app = falcon.App(cors_enable=True)
app = falcon.App(middleware=falcon.CORSMiddleware(
    allow_origins='*', allow_credentials='*'
))


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