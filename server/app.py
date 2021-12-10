import falcon
import json

from wsgiref import simple_server
from dataStore import ITEMS




class ItemResource:
    def on_get(self, req, resp):
        """Handles GET request for single item"""
        if req.param("id"):
            resp.media = {'id': "", 'keywords': "",'description': "", 'lat': "", 'lon': "" }
        
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        pass
    

class MultipleItemsResource:
    def on_get(self, req, resp):
        """Handles GET request for multiple items"""
        if req.param("id"):
            resp.media

        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        pass



class PostResource:
    def on_post(self, req, resp):
        """Handles POST requests"""
        obj = req.get_media()
        print(obj)

        id = obj.get('id')
        description = obj.get('description')
        lat = obj.get('lat')
        lon = obj.get('lon')
        keywords = obj.get('keywords')



        resp.media = {'id' : id,  'description' : description, 'lat' : lat, 'lon' : lon , 'keywords' : keywords}

        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        pass



class DeleteResource:
    def on_delete(self, req, resp):
        """Handles DELETE requests"""
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON

#class OptionsResource:
#    def on_options(self, req, resp):
#
#        resp.status = falcon.HTTP_200
#        resp.content_type = falcon.MEDIA_JSON



app = application = falcon.App()

app.add_route('/item', PostResource())
app.add_route('/item/{itemId}/', ItemResource())
app.add_route('/items', MultipleItemsResource())
app.add_route('/item/{itemId}/' , DeleteResource())

if __name__ == '__main__':

    server = simple_server.make_server("0.0.0.0", 8000, app)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass