import pytest

import utils.error_msg as em
from .base_test import BaseTest


class TestHouse(BaseTest):
    """test house view"""
    prefix = '/house'
    email = 'tester@gogo.com'
    password = 'notclear'

    @pytest.mark.run(order=21)
    def test_create_house(self, client, db_no_rollback):
        data = {
            'house_name': 'big house',
            'place_id': '9ni9fdqwj19219jdj9q192j9129e',
            'house_address': '123 main street n',
            'house_city': 'waterloo',
            'house_province': 'ON',
            'house_postcode': 'A1B C2D',
            'longitude': '1.23456789',
            'latitude': '2.345678901',
            'date_begin': '2019-03-01',
            'date_end': '2019-03-02',
            'number_of_beds': '3',
            'description': 'this is a really nice house with a big living room.'
        }
        # forbidden
        response = self.post(client, '/create', data)
        assert response.status_code == 403

        # illegal request method
        response = self.get(client, '/create', data)
        assert response.status_code == 405

        # success
        self.login(client, self.email, self.password)
        response = self.post(client, '/create', data)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['success'] == 1

        data = {
            'house_name': 'small house',
            'place_id': '9ifamskd1nmkasofiajw4e1221j31i2',
            'house_address': '789 main street n',
            'house_city': 'baby blue',
            'house_province': 'ON',
            'house_postcode': 'C0J S9J',
            'longitude': '6.192391251',
            'latitude': '-5.999494939',
            'date_begin': '2019-03-01',
            'date_end': '2019-03-02',
            'number_of_beds': '3',
            'description': 'although I am small, I have ten bathrooms.'
        }

        # success
        response = self.post(client, '/create', data)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['success'] == 1

        # duplicate data
        data = {
            'house_name': 'big house',
            'place_id': '9ni9fdqwj19219jdj9q192j9129e',
            'house_address': '123 main street n',
            'house_city': 'waterloo',
            'house_province': 'ON',
            'house_postcode': 'A1B C2D',
            'longitude': '1.23456789',
            'latitude': '2.345678901',
            'date_begin': '2019-03-01',
            'date_end': '2019-03-02',
            'number_of_beds': '3',
            'description': 'this is a really nice house with a big living room.'
        }
        response = self.post(client, '/create', data)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['success'] == 0
        assert response_json['msg'] == em.DUPLICATE_HOUSE

        # missing parameter
        data = {
            'house_name': 'big house',
            'place_id': '9ni9fdqwj19219jdj9q192j9129e',
            'house_address': '123 main street n',
            'house_city': 'waterloo',
            'house_province': 'ON',
            'house_postcode': 'A1B C2D',
            'date_begin': '2019-03-01',
            'date_end': '2019-03-02',
            'number_of_beds': '3'
        }
        response = self.post(client, '/create', data)
        assert response.status_code == 400

        # wrong date (date_begin > date_end)
        data = {
            'house_name': 'preston house',
            'place_id': '9f91ufhujjasdj21j192931239',
            'house_address': '123 main street n',
            'house_city': 'waterloo',
            'house_province': 'ON',
            'house_postcode': 'A1B C2D',
            'longitude': '1.23456789',
            'latitude': '2.345678901',
            'date_begin': '2019-03-01',
            'date_end': '2019-02-01',
            'number_of_beds': '3',
            'description': 'I am 690 a month.'
        }
        response = self.post(client, '/create', data)
        assert response.status_code == 400
        response_json = response.json()
        assert response_json['success'] == 0
        assert response_json['msg'] == em.WRONG_DATE_BEGIN_END

        # validation error (number_of_beds)
        data = {
            'house_name': 'big house',
            'place_id': '9ni9fdqwj19219jdj9q192j9129e',
            'house_address': '123 main street n',
            'house_city': 'waterloo',
            'house_province': 'ontario',
            'house_postcode': 'A1B C2D',
            'longitude': '1.23456789',
            'latitude': '2.345678901',
            'date_begin': '2019-03-01',
            'date_end': '2019-03-02',
            'number_of_beds': '-1'
        }
        response = self.post(client, '/create', data)
        assert response.status_code == 400
        response_json = response.json()
        assert response_json['success'] == 0

    @pytest.mark.run(order=22)
    def test_search_without_parameters(self, client, db_no_rollback):
        # forbidden
        response = self.get(client, '/search')
        assert response.status_code == 403

        # success
        self.login(client, self.email, self.password)
        response = self.get(client, '/search')
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['success'] == 1

        # illegal request method
        response = self.post(client, '/search')
        assert response.status_code == 405

    @pytest.mark.run(order=23)
    def test_search_with_parameters(self, client, db_no_rollback):
        self.login(client, self.email, self.password)
        data = {
            'longitude': '1.23456789',
            'latitude': '2.345678901',
            'date_begin': '2019-03-01',
            'date_end': '2019-03-02',
            'number_of_beds': '3',
            'max_distance': '20000'
        }
        # big house can be found
        response = self.get(client, '/search', data)
        assert response.status_code == 200
        response_json = response.json()
        print(response_json)
        assert response_json['success'] == 1
        assert len(response_json['house_list']) == 1

        data = {
            'longitude': '1.23456789',
            'latitude': '2.345678901',
            'date_begin': '2019-03-01',
            'date_end': '2019-03-02',
            'number_of_beds': '4',
            'max_distance': '20000'
        }
        # nothing can be found
        response = self.get(client, '/search', data)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['success'] == 1
        assert len(response_json['house_list']) == 0

        data = {
            'longitude': '1.23456789',
            'latitude': '2.345678901',
            'date_begin': '2019-02-01',
            'date_end': '2019-03-02',
            'number_of_beds': '3',
            'max_distance': '20000'
        }
        # nothing can be found
        response = self.get(client, '/search', data)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['success'] == 1
        assert len(response_json['house_list']) == 0

        data = {
            'longitude': '4.919292922',
            'latitude': '2.345678901',
            'date_begin': '2019-02-01',
            'date_end': '2019-03-02',
            'number_of_beds': '3',
            'max_distance': '20000'
        }
        # nothing can be found
        response = self.get(client, '/search', data)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['success'] == 1
        assert len(response_json['house_list']) == 0

        data = {
            'longitude': '1.23456789',
            'latitude': '2.345678901',
            'number_of_beds': '3',
            'max_distance': '20000'
        }
        response = self.get(client, '/search', data)
        assert response.status_code == 400

    @pytest.mark.run(order=51)
    def test_house_info_request_method_is_get(self, client, db_no_rollback):
        self.login(client, self.email, self.password)
        # pre work, get the house_id
        data = {
            'longitude': '1.23456789',
            'latitude': '2.345678901',
            'date_begin': '2019-03-01',
            'date_end': '2019-03-02',
            'number_of_beds': '3',
            'max_distance': '20000'
        }
        response = self.get(client, '/search', data)
        assert response.status_code == 200

        response_json = response.json()
        assert response_json['success'] == 1
        assert len(response_json['house_list']) == 1

        house_id = response_json['house_list'][0]['house_id']
        assert isinstance(house_id, int) is True

        data = {
            "house_id": house_id
        }

        # test GET
        response = self.get(client, '/info', data)
        assert response.status_code == 200

        response_json = response.json()
        assert response_json['success'] == 1
        assert response_json['info']['name'] == 'big house'

    @pytest.mark.run(order=52)
    def test_house_info_request_method_is_post(self, client, db_no_rollback):
        self.login(client, self.email, self.password)

        # pre work, get the house_id
        data = {
            'longitude': '1.23456789',
            'latitude': '2.345678901',
            'date_begin': '2019-03-01',
            'date_end': '2019-03-02',
            'number_of_beds': '3',
            'max_distance': '20000'
        }
        response = self.get(client, '/search', data)
        assert response.status_code == 200

        response_json = response.json()
        assert response_json['success'] == 1
        assert len(response_json['house_list']) == 1

        house_id = response_json['house_list'][0]['house_id']
        assert isinstance(house_id, int) is True

        data = {
            "house_id": house_id
        }

        # test POST
        response = self.post(client, '/info', data)
        assert response.status_code == 405

    @pytest.mark.run(order=53)
    def test_house_info_wrong_house_id(self, client, db_no_rollback):
        self.login(client, self.email, self.password)
        data = {
            "house_id": 9999
        }
        response = self.get(client, '/info', data)
        assert response.status_code == 404

        response_json = response.json()
        assert response_json['success'] == 0

    @pytest.mark.run(order=54)
    def test_house_info_without_login(self, client, db_no_rollback):
        data = {
            "house_id": 1
        }
        response = self.get(client, '/info', data)
        assert response.status_code == 403
