import falcon

import json

from wsgiref import simple_server
from dataStore import ITEMS




class resource:
    def on_get(self, req):
        """Handles GET requests"""
        if req.get_param("id"):
            resp.media = {'user_id': "", "keywords":"","description": "", "lat": "" , "lon": "" }
        
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
    
   
    def on_post(self, req, resp):
        """Handles POST requests"""

        resp.media = {"id" : ITEMS.id, 'user_id' : ITEMS.user_id, 'description' : ""}

        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON



    def on_delete(self, req, resp):
        """Handles DELETE requests"""
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        


app = application = falcon.App()
app.add_route('/get', resource.on_get(ITEMS['id'], ITEMS))
app.add_route('/post', resource.on_post())
app.add_route('/delete' , resource.on_delete())

if __name__ == '__main__':

    server = simple_server.make_server("0.0.0.0", 8000, app)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass