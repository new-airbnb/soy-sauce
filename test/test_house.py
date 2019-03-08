import pytest
from .base_test import BaseTest
import utils.error_msg as em


class TestHouse(BaseTest):
    """test house view"""
    prefix = '/house'
    email = 'tester@gogo.com'
    password = 'notclear'

    @pytest.mark.run(order=21)
    def test_create_house(self, client, db_no_rollback):
        # TODO login can be encapsulated to a decorator
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
            'number_of_beds': '3'
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
            'number_of_beds': '3'
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
            'number_of_beds': '3'
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

        # wrong date
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
            'date_end': '2019-02-01',
            'number_of_beds': '3'
        }
        response = self.post(client, '/create', data)
        assert response.status_code == 400
        response_json = response.json()
        assert response_json['success'] == 0
        assert response_json['msg'] == em.WRONG_DATE_BEGIN_END

        # validation error (house_province)
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
            'date_end': '2019-02-01',
            'number_of_beds': '3'
        }
        response = self.post(client, '/create', data)
        assert response.status_code == 400
        response_json = response.json()
        assert response_json['success'] == 0

        # validation error (house_province)
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
            'date_end': '2019-02-01',
            'number_of_beds': '3'
        }
        response = self.post(client, '/create', data)
        assert response.status_code == 400
        response_json = response.json()
        assert response_json['success'] == 0

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
            'date_end': '2019-02-01',
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
        # here, something really tricky, I haven't resolved.
        assert len(response_json['house_list']) > 0

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