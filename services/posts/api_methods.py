import requests
from utils.helper import Helper
# from config.headers import Headers
# from services.posts.endpoints import Endpoints
# from services.posts.payloads import Payloads
from services.posts.models.post_model import Model

class PostsAPI(Helper):

    # def __init__(self):
    #     super().__init__()
    #     self.headers = Headers()
    #     self.payloads = Payloads()
    #     self.endpoints = Endpoints()

    def get_all_posts(self, status_code):
        response = requests.get(
            url=self.endpoints.get_all_posts
        )
        assert response.status_code == status_code, response.json()
        models = [Model(**post) for post in response.json()]
        self.attach_response(response.json())
        return models
    
    # def get_post_by_id(self, id, status_code, request):
    #     response = requests.get(
    #         url=self.endpoints.get_post_by_id(id)
    #     )
    #     assert response.status_code == status_code, response.json()
    #     if request.node.get_closest_marker('smoke'):
    #         model = Model(**response.json())
    #         self.attach_response(response.json())
    #         return model
        
    def get_post_by_id(self, url, id, status_code, request):
        response = requests.get(
            url=url
        )
        assert response.status_code == status_code, response.json()
        if request.node.get_closest_marker('smoke'):
            model = Model(**response.json())
            self.attach_response(response.json())
            return model
    
    def create_new_post(self, status_code, request):
        # print(response.json().id)
        response = requests.post(
            url=self.endpoints.create_new_post,
            json=self.payloads.valid_post
        )
        assert response.status_code == status_code, response.json()
        if request.node.get_closest_marker('smoke'):
            model = Model(**response.json())
            self.attach_response(response.json())
            return model
    
    def update_post(self, uuid, status_code):
        response = requests.put(
            url=self.endpoints.update_post(uuid),
            json=self.payloads.text_only
        )
        assert response.status_code == status_code, response.json()
        self.attach_response(response.json())
        model = Model(**response.json())
        return model
    
    def patch_post(self, uuid, status_code):
        response = requests.patch(
            url=self.endpoints.patch_post(uuid),
            json=self.payloads.text_only
        )
        assert response.status_code == status_code, response.json()
        self.attach_response(response.json())
        model = Model(**response.json())
        return model
    
    def delete_post(self, uuid, status_code):
        response = requests.delete(
            url=self.endpoints.delete_post(uuid)
        )
        assert response.status_code == status_code, response.json()
        self.attach_response(response.json())
        model = Model(**response.json())
        return model
    