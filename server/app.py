import falcon
import json

from wsgiref import simple_server
from dataStore import ITEMS


class ItemResource:
    def on_get(self, req, resp):
        """Handles GET request for single item"""
        if req.get_param("id"):
            resp.media = {'user_id': "", "keywords":"","description": "", "lat": "" , "lon": "" }
        
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
    

class MultipleItemsResource:
    def on_get(self, req, resp):
        """Handles GET request for multiple items"""
        if req.get_param("id"):
            resp.media

        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON



class PostResource:
    def on_post(self, req, resp):
        """Handles POST requests"""

        resp.media = {"id" : ITEMS.id, 'user_id' : ITEMS.user_id, 'description' : ""}

        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON



class DeleteResource:
    def on_delete(self, req, resp):
        """Handles DELETE requests"""
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON



app = application = falcon.App()


app.add_route('/get', ItemResource())
app.add_route('/getmany', MultipleItemsResource())
app.add_route('/post', PostResource())
app.add_route('/delete/{itemID}' , DeleteResource())

if __name__ == '__main__':

    server = simple_server.make_server("0.0.0.0", 8000, app)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass