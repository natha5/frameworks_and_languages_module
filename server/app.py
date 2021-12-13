import falcon
import json
import datetime

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
        #if req.param("id"):
        resp.media = json.dumps(ITEMS)

        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        pass



class PostResource:
    def on_post(self, req, resp):
        """Handles POST requests"""
        app = json.load(req.bounded_stream)
        
        #data = req.JSON

        #create new values that arent inputted by user
        date_from = datetime.datetime.now()
        date_to = datetime.datetime.now()
        id = max(ITEMS.keys()) + 1

        ## check got the right fields
        

        fields = set({user_id, keywords, description, image, lat, lon})

        if(ITEMS.keys != fields){
            resp.status = HTTP_204
        }else{
            ITEMS[new_id] = req.JSON
            
            ITEMS.add()
            
            resp.status = falcon.HTTP_201
        }

        resp.content_type = falcon.MEDIA_JSON
        #resp.media = {'id' : itemId, 'lat' : lat, 'lon' : lon, 'description' : description, 'keywords' : keywords}
      
        
        pass




    

#class OptionsResource:
#    def on_options(self, req, resp):
#
#        resp.status = falcon.HTTP_200
#        resp.content_type = falcon.MEDIA_JSON


#cors handling
app = falcon.App(middleware=falcon.CORSMiddleware(
    allow_origins='http://localhost:8001', allow_credentials='*'))
    #allow_origins='https://8001-apricot-beaver-j6aztah6.ws-eu23.gitpod.io' , allow_credentials='*'))


app = application = falcon.App()

app.add_route('/item', PostResource())
app.add_route('/item/{itemId}/', ItemResource())
app.add_route('/items', MultipleItemsResource())


if __name__ == '__main__':

    server = simple_server.make_server("0.0.0.0", 8000, app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass