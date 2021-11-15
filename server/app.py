import falcon

import json


class resource
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.media = {'message': 'hello world'}
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
    
"""    def on_post()


    def on_delete()"""

    resp.text = json.dumps()    

api = falcon.API()

app =  = falcon.app()
app.add_route('/', resource())