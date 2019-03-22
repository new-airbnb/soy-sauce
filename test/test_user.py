import pytest

from utils import error_msg
from .base_test import BaseTest


class TestUser(BaseTest):
    # order range: 11~30. see https://pytest-ordering.readthedocs.io

    prefix = '/user'

    right_email = 'tester@gogo.com'
    right_password = 'notclear'
    wrong_email = 'toeiwji@feio.com'
    wrong_password = 'oifwioioe'
    illegal_email = '0' * 129
    illegal_password = '0' * 65

    @pytest.mark.run(order=11)
    def test_register_success(self, client, db_no_rollback):
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
    def test_register_duplicate_email(self, client, db_no_rollback):
        data = {
            'email': self.right_email,
            'password': self.right_password
        }
        response = self.post(client, '/register', data)
        assert response.status_code == 409
        response_json = response.json()
        assert response_json['success'] == 0
        assert response_json['msg'] == error_msg.DUPLICATE_EMAIL

    @pytest.mark.run(order=13)
    def test_register_validation_error(self, client, db_no_rollback):
        data = {
            'email': self.illegal_email,
            'password': self.illegal_password
        }
        response = self.post(client, '/register', data)
        assert response.status_code == 400
        response_json = response.json()
        assert response_json['success'] == 0
        assert response_json['msg'] == error_msg.ILLEGAL_ARGUMENT

    @pytest.mark.run(order=14)
    def test_login_wrong_password(self, client, db_no_rollback):
        data = {
            'email': self.right_email,
            'password': self.wrong_password,
            'remember_me': 'false',
        }
        response = self.post(client, '/login', data)
        assert response.status_code == 401

    @pytest.mark.run(order=15)
    def test_login_wrong_email(self, client, db_no_rollback):
        data = {
            'email': self.wrong_email,
            'password': self.right_password,
            'remember_me': 'false',
        }
        response = self.post(client, '/login', data)
        assert response.status_code == 401

    @pytest.mark.run(order=16)
    def test_login_success(self, client, db_no_rollback):
        data = {
            'email': self.right_email,
            'password': self.right_password,
            'remember_me': 'false',
        }
        response = self.post(client, '/login', data)
        assert response.status_code == 200
        assert 'sessionid' in response.cookies
