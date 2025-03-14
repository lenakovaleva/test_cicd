import pytest
import requests
import allure
from config.base_test import BaseTest
from config.headers import Headers
from services.posts.endpoints import Endpoints
from services.posts.payloads import Payloads
from services.posts.models.post_model import Model, PutModel
from urllib.parse import urljoin
from utils.helper import Helper


helper = Helper()
header = Headers()

@allure.feature("Posts")
class TestPosts(BaseTest):
    

    @pytest.mark.parametrize(
        'endp, status_code',
        [
            pytest.param('/posts', 200, marks=pytest.mark.smoke),
        ]
    )
    @allure.title("Проверить получение всех постов")
    def test_get_all_posts(self, endp, status_code):
        response = requests.get(
            url=urljoin(Endpoints.HOST, endp)
        )
        assert response.status_code == status_code, response.json()
        helper.attach_response(response.json())
        model = [Model(**item) for item in response.json()]
        return model

    @pytest.mark.parametrize(
        'endp, status_code',
        [
            pytest.param('/posts/1', 200, marks=pytest.mark.smoke),
            pytest.param('/posts/0', 404, marks=pytest.mark.extended),
            pytest.param('/posts/100', 200, marks=pytest.mark.extended),
            pytest.param('/posts/101', 404, marks=pytest.mark.extended),
            pytest.param('/posts/-1', 404, marks=pytest.mark.extended),
            pytest.param('/posts/k', 404, marks=pytest.mark.extended),
        ]
    )
    @allure.title("Проверить получение поста по id")
    def test_get_post_by_id(self, endp, status_code, request):
        response = requests.get(
            url=urljoin(Endpoints.HOST, endp)
        )
        assert response.status_code == status_code, response.json()
        if request.node.get_closest_marker('smoke'):
            helper.attach_response(response.json())
            model = Model(**response.json())
            return model


# Ожидаемый статус-код: 201. От сервера приходит статус-код 404. В тесте для наглядности оставила 201
    @pytest.mark.parametrize(
        'endp1, payload, status_code1, endp2, status_code2',
        [
            pytest.param('/posts', Payloads.valid_post(), 201, None, None, marks=pytest.mark.smoke),
            pytest.param('/posts', Payloads.body_only(), 201, None, None, marks=pytest.mark.crit_path),
            pytest.param('/posts', Payloads.without_id(), 201, None, None, marks=pytest.mark.crit_path),
            pytest.param('/posts', Payloads.without_userId(), 201, None, None, marks=pytest.mark.crit_path),
            pytest.param('/posts', Payloads.without_title(), 201, None, None, marks=pytest.mark.crit_path),
            pytest.param('/posts', Payloads.valid_post(), 201, '/posts/101', 201, marks=pytest.mark.crit_path),
            pytest.param('/posts', Payloads.without_body(), 201, None, None, marks=pytest.mark.extended),
            pytest.param('/posts', Payloads.empty(), 201, None, None, marks=pytest.mark.extended),
        ]
    )
    @allure.title("Проверить создание нового поста")
    def test_create_new_post(self, endp1, payload, status_code1, endp2, status_code2, request):
        response = requests.post(
            url=urljoin(Endpoints.HOST, endp1),
            json=payload
        )

        if endp2 is not None and status_code2 is not None:
            response2 = requests.post(
            url=urljoin(Endpoints.HOST, endp2),
            json=payload
        )
            assert response.status_code == status_code1, response.json()
            assert response2.status_code == status_code2, response2.json()
            helper.attach_response(response.json())
            
        if request.node.get_closest_marker('smoke'):
            assert response.headers["Content-Type"] == header.basic["Content-Type"], response.json()
            helper.attach_response(response.json())
            model = Model(**response.json())
            return model


    @pytest.mark.parametrize(
        'endp1, payload, status_code1, endp2, status_code2',
        [
            pytest.param('/posts/2', Payloads.valid_put(), 200, None, None, marks=pytest.mark.smoke),
            pytest.param('/posts/2', Payloads.body_only(), 200, None, None, marks=pytest.mark.crit_path),
            pytest.param('/posts/2', Payloads.valid_put(), 200, '/posts/2', 200, marks=pytest.mark.crit_path),
            pytest.param('/posts/2', Payloads.without_id(), 200, None, None, marks=pytest.mark.extended),
            pytest.param('/posts/2', Payloads.without_userId(), 200, None, None, marks=pytest.mark.extended),
            pytest.param('/posts/2', Payloads.without_title(), 200, None, None, marks=pytest.mark.extended),
            pytest.param('/posts/2', Payloads.without_body(), 200, None, None, marks=pytest.mark.extended),
            pytest.param('/posts/2', Payloads.empty(), 200, None, None, marks=pytest.mark.extended),
        ]
    )
    @allure.title("Проверить обновление поста (метод PUT)")
    def test_update_post(self, endp1, payload, status_code1, endp2, status_code2, request):
        response = requests.put(
            url=urljoin(Endpoints.HOST, endp1),
            json=payload
        )
        
        if request.node.get_closest_marker('smoke'):
            assert response.headers["Content-Type"] == header.basic["Content-Type"], response.json()
            helper.attach_response(response.json())
            model = PutModel(**response.json())
            return model

        if endp2 is not None and status_code2 is not None:
            response2 = requests.get(
            url=urljoin(Endpoints.HOST, endp2),
        )
            assert response.status_code == status_code1, response.json()
            assert response.json()['body'] == Payloads.valid_put()['body'], response.json()
            assert response2.status_code == status_code2, response2.json()
            assert response.json()['body'] == Payloads.valid_put()['body'], response.json()
            helper.attach_response(response.json())
            model = PutModel(**response.json())
            return model    


    @pytest.mark.parametrize(
        'endp1, payload, status_code1, endp2, status_code2',
        [
            pytest.param('/posts/2', Payloads.valid_put(), 200, None, None, marks=pytest.mark.smoke),
            pytest.param('/posts/2', Payloads.body_only(), 200, None, None, marks=pytest.mark.crit_path),
            pytest.param('/posts/2', Payloads.valid_put(), 200, '/posts/2', 200, marks=pytest.mark.crit_path),
            pytest.param('/posts/2', Payloads.without_id(), 200, None, None, marks=pytest.mark.extended),
            pytest.param('/posts/2', Payloads.without_userId(), 200, None, None, marks=pytest.mark.extended),
            pytest.param('/posts/2', Payloads.without_title(), 200, None, None, marks=pytest.mark.extended),
            pytest.param('/posts/2', Payloads.without_body(), 200, None, None, marks=pytest.mark.extended),
            pytest.param('/posts/2', Payloads.empty(), 200, None, None, marks=pytest.mark.extended),
        ]
    )
    @allure.title("Проверить обновление поста (метод PATCH)")
    def test_patch_post(self, endp1, payload, status_code1, endp2, status_code2, request):
        response = requests.patch(
            url=urljoin(Endpoints.HOST, endp1),
            json=payload
        )
        
        if request.node.get_closest_marker('smoke'):
            assert response.headers["Content-Type"] == header.basic["Content-Type"], response.json()
            helper.attach_response(response.json())
            model = Model(**response.json())
            return model

        if endp2 is not None and status_code2 is not None:
            response2 = requests.get(
            url=urljoin(Endpoints.HOST, endp2),
        )
            assert response.status_code == status_code1, response.json()
            assert response.json()['body'] == Payloads.valid_put()['body'], response.json()
            assert response2.status_code == status_code2, response2.json()
            assert response.json()['body'] == Payloads.valid_put()['body'], response.json()
            helper.attach_response(response.json())
            model = Model(**response.json())
            return model 


# Ожидаемый статус-код: 404. От сервера приходит статус-код 200. В тесте для наглядности оставила 404
    @pytest.mark.parametrize(
        'endp1, status_code1, endp2, status_code2',
        [
            pytest.param('/posts/2', 200, None, None, marks=pytest.mark.smoke),
            pytest.param('/posts/3', 200, '/posts/3', 404, marks=pytest.mark.crit_path),
        ]
    )
    @allure.title("Проверить удаление поста")
    def test_delete_post(self, endp1, status_code1, endp2, status_code2, request):
        response = requests.delete(
            url=urljoin(Endpoints.HOST, endp1)
        )

        if endp2 is not None and status_code2 is not None:
            response2 = requests.get(
            url=urljoin(Endpoints.HOST, endp2)
        )
            assert response.status_code == status_code1, response.json()
            assert response2.status_code == status_code2, response2.json()
            helper.attach_response(response.json())
            
        if request.node.get_closest_marker('smoke'):
            assert response.headers["Content-Type"] == header.basic["Content-Type"], response.json()
            helper.attach_response(response.json())
        
        assert response.json() == Payloads.empty(), response.json()
        helper.attach_response(response.json())  
