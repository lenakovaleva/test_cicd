# HOST = "https://jsonplaceholder.typicode.com"

class Endpoints:

    HOST = "https://jsonplaceholder.typicode.com"

    get_all_posts = f"{HOST}/posts"
    get_post_by_id = lambda self, id: f"{HOST}/posts/{id}"
    create_new_post = f"{HOST}/posts"
    update_post = lambda self, id: f"{HOST}/posts/{id}"
    patch_post = lambda self, id: f"{HOST}/posts/{id}"
    delete_post = lambda self, id: f"{HOST}/posts/{id}"
    