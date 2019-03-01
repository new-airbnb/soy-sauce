import pytest
from .base_test import BaseTest


class TestUser(BaseTest):
    # order range: 11~30. see https://pytest-ordering.readthedocs.io

    prefix = '/user'

    right_email = 'tester@gogo.com'
    right_password = 'notclear'
    wrong_email = 'toeiwji@feio.com'
    wrong_password = 'oifwioioe'

    @pytest.mark.run(order=11)
    def test_register(self, client, db_no_rollback):
        data = {
            'email': self.right_email,
            'password': self.right_password
        }
        response = self.post(client, '/register', data)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['success'] == 1
        assert response_json['user']['email'] == data['email']

    @pytest.mark.run(order=12)
    def test_login(self, client, db_no_rollback):
        data = {
            'email': self.right_email,
            'password': self.wrong_password,
            'remember_me': 'false',
        }
        response = self.post(client, '/login', data)
        assert response.status_code == 401

        data = {
            'email': self.wrong_email,
            'password': self.right_password,
            'remember_me': 'false',
        }
        response = self.post(client, '/login', data)
        assert response.status_code == 401

        data = {
            'email': self.right_email,
            'password': self.right_password,
            'remember_me': 'false',
        }
        response = self.post(client, '/login', data)
        assert response.status_code == 200
        assert 'sessionid' in response.cookies
