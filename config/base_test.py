from services.posts.api_methods import PostsAPI

class BaseTest:

    def setup_method(self):
        self.api_users = PostsAPI()