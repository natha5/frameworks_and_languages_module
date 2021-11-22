import falcon

import json

from wsgiref import simple_server
from datastore import ITEMS

class resource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        if req.get_param("id"):
            resp.media = {'user_id': id, "keywords":[],"description": "", "lat": "" , "lon": "" }
        
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
    
   
    def on_post(self, req, resp):
        """Handles POST requests"""

        resp.media = {"id" : ITEMS.id, 'user_id' : ITEMS.user_id, 'description' : }

        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON



    def on_delete(self, req, resp):
        """Handles DELETE requests"""
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        

    

api = openapi.yml

app = application = falcon.App()
app.add_route('/', resource())

server = make_server('localhost', 8000, application)
server.serve_forever()