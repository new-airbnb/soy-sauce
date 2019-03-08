import pytest
from .base_test import BaseTest


class TestHouse(BaseTest):
    """test house view"""
    prefix = '/house'
    email = 'tester@gogo.com'
    password = 'notclear'

    @pytest.mark.run(order=13)
    def test_create_house(self, client, db_no_rollback):
        # TODO login can be encapsulated to a decorator
        self.login(client, self.email, self.password)
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
        assert response_json['success'] == 1

    @pytest.mark.run(order=14)
    def test_search_without_parameters(self, client, db_no_rollback):
        self.login(client, self.email, self.password)
        response = self.get(client, '/search')
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['success'] == 1

    @pytest.mark.run(order=15)
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
        response = self.get(client, '/search', data)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['success'] == 1
