import falcon
import json
import datetime


from falcon.http_status import HTTPStatus
from wsgiref import simple_server
from dataStore import *



class ItemResource:
    def on_get(self, req, resp, itemId):
        """Handles GET request for single item"""
        
        resp.media = json.dumps(ITEMS)
        
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        pass
    def on_delete(self, req, resp, itemId):
        """Handles DELETE requests"""
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON


class MultipleItemsResource:
    def on_get(self, req, resp):
        """Handles GET request for multiple items"""

        inputData = json.load(req.bounded_stream)
        userid = inputData.userid

        
        if(ITEMS.values == userid):
            resp.media = json.dumps(ITEMS)

            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_400
        resp.content_type = falcon.MEDIA_JSON
        pass



class PostResource:
    def on_post(self, req, resp):
        """Handles POST requests"""
        inputData = json.load(req.bounded_stream)
        
        #data = req.JSON

        #create new values that arent inputted by user
        newDateFrom = datetime.datetime.now()
        newDateTo = datetime.datetime.now()
        newId = max(ITEMS.keys()) + 1

        ## check the correct fields have been filled

        neededFields = set({'user_id', 'keywords', 'description', 'lat', 'lon'})
        givenFields = set(inputData.keys())

        if(givenFields.issubset(neededFields)):
            ITEMS[newId] = {
                "id" : newId,
                "user_id" : inputData.user_id,
                "keywords" : inputData.keywords,
                "description" : inputData.description,
                "image" : inputData.image,
                "lat" : inputData.lat,
                "lon" : inputData.lon,
                "date_from" : newDateFrom,
                "date_to ": newDateTo
            }

            
            ITEMS.add()
            
            resp.status = falcon.HTTP_201
            
            
            
        else:
            resp.status = falcon.HTTP_405

        resp.content_type = "application/json"
        #resp.media = {'id' : itemId, 'lat' : lat, 'lon' : lon, 'description' : description, 'keywords' : keywords}

        pass

class rootResource:
    def on_get(self, resp, req):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
    

class OptionsResource:
    def on_options(self, req, resp):

        resp.status = falcon.HTTP_204
        resp.content_type = falcon.MEDIA_JSON


#cors handling adapted from https://github.com/falconry/falcon/issues/1220


class HandleCORS(object):
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'POST')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        resp.set_header('Access-Control-Max-Age', 1728000)  # 20 days
        resp.body = 'hi'
        resp.content_type = "text/html"
        if req.method == 'OPTIONS':
            raise HTTPStatus(falcon.HTTP_204, body='\n')

app = falcon.API(middleware=[HandleCORS() ])





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