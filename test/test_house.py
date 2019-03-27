import pytest

import utils.error_msg as em
from utils import error_msg
from .base_test import BaseTest


class TestHouse(BaseTest):
    '''test house view'''
    prefix = '/house'
    email = 'tester@gogo.com'
    password = 'notclear'

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
        'description': 'this is a really nice house with a big living room.',
        'price': '200'
    }

    @pytest.mark.run(order=31)
    def test_create_house_forbidden(self, client, db_no_rollback):
        # forbidden
        response = self.post(client, '/create', self.data)
        assert response.status_code == 403

    @pytest.mark.run(order=32)
    def test_create_house_illegal(self, client, db_no_rollback):
        # illegal request method
        response = self.get(client, '/create', self.data)
        assert response.status_code == 405

    @pytest.mark.run(order=33)
    def test_create_house_success_1(self, client, db_no_rollback):
        # success
        self.login(client, self.email, self.password)
        response = self.post(client, '/create', self.data)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['success'] == 1

    @pytest.mark.run(order=34)
    def test_create_house_success_2(self, client, db_no_rollback):
        self.login(client, self.email, self.password)
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
            'description': 'although I am small, I have ten bathrooms.',
            'price': '100'

        }

        # success
        response = self.post(client, '/create', data)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['success'] == 1

    @pytest.mark.run(order=35)
    def test_create_house_dulicate_data(self, client, db_no_rollback):
        # duplicate data
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
            'number_of_beds': '3',
            'description': 'this is a really nice house with a big living room.',
            'price': '200'
        }
        response = self.post(client, '/create', data)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['success'] == 0
        assert response_json['msg'] == em.DUPLICATE_HOUSE

    @pytest.mark.run(order=36)
    def test_create_house_missing_parameter(self, client, db_no_rollback):
        # missing parameter
        self.login(client, self.email, self.password)
        data = {
            'house_name': 'big house',
            'place_id': '9ni9fdqwj19219jdj9q192j9129e',
            'house_address': '123 main street n',
            'house_city': 'waterloo',
            'house_province': 'ON',
            'house_postcode': 'A1B C2D',
            'date_begin': '2019-03-01',
            'date_end': '2019-03-02',
            'number_of_beds': '3',
            'price': '200'
        }
        response = self.post(client, '/create', data)
        assert response.status_code == 400

    @pytest.mark.run(order=37)
    def test_create_house_wrong_date(self, client, db_no_rollback):
        # wrong date (date_begin > date_end)
        self.login(client, self.email, self.password)
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
            'description': 'I am 690 a month.',
            'price': '690'
        }
        response = self.post(client, '/create', data)
        assert response.status_code == 400
        response_json = response.json()
        assert response_json['success'] == 0
        assert response_json['msg'] == em.WRONG_DATE_BEGIN_END

    @pytest.mark.run(order=38)
    def test_create_house_validation_error(self, client, db_no_rollback):
        # validation error (number_of_beds)
        self.login(client, self.email, self.password)
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
            'number_of_beds': '-1',
            'price': '200'
        }
        response = self.post(client, '/create', data)
        assert response.status_code == 400
        response_json = response.json()
        assert response_json['success'] == 0

    @pytest.mark.run(order=39)
    def test_search_without_parameters_forbidden(self, client, db_no_rollback):
        # forbidden
        response = self.get(client, '/search')
        assert response.status_code == 403

    @pytest.mark.run(order=40)
    def test_search_without_parameters_success(self, client, db_no_rollback):
        # success
        self.login(client, self.email, self.password)
        response = self.get(client, '/search')
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['success'] == 1

    @pytest.mark.run(order=41)
    def test_search_without_parameters_illegal_request_method(self, client, db_no_rollback):
        # illegal request method
        self.login(client, self.email, self.password)
        response = self.post(client, '/search')
        assert response.status_code == 405

    @pytest.mark.run(order=42)
    def test_search_with_parameters_success_1(self, client, db_no_rollback):
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

    @pytest.mark.run(order=43)
    def test_search_with_parameters_success_2(self, client, db_no_rollback):
        self.login(client, self.email, self.password)
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

    @pytest.mark.run(order=44)
    def test_search_with_parameters_success_3(self, client, db_no_rollback):
        self.login(client, self.email, self.password)
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

    @pytest.mark.run(order=45)
    def test_search_with_parameters_success_4(self, client, db_no_rollback):
        self.login(client, self.email, self.password)
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

    @pytest.mark.run(order=46)
    def test_search_with_parameters_illegal_parameter(self, client, db_no_rollback):
        self.login(client, self.email, self.password)
        data = {
            'longitude': '1.23456789',
            'latitude': '2.345678901',
            'number_of_beds': '3',
            'max_distance': '20000'
        }
        response = self.get(client, '/search', data)
        assert response.status_code == 400

    @pytest.mark.run(order=47)
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
            'house_id': house_id
        }

        # test GET
        response = self.get(client, '/info', data)
        assert response.status_code == 200

        response_json = response.json()
        assert response_json['success'] == 1
        assert response_json['info']['name'] == 'big house'

    @pytest.mark.run(order=48)
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
            'house_id': house_id
        }

        # test POST
        response = self.post(client, '/info', data)
        assert response.status_code == 405

    @pytest.mark.run(order=49)
    def test_house_info_wrong_house_id(self, client, db_no_rollback):
        self.login(client, self.email, self.password)
        data = {
            'house_id': 9999
        }
        response = self.get(client, '/info', data)
        assert response.status_code == 404

        response_json = response.json()
        assert response_json['success'] == 0

    @pytest.mark.run(order=50)
    def test_house_info_without_login(self, client, db_no_rollback):
        data = {
            'house_id': 1
        }
        response = self.get(client, '/info', data)
        assert response.status_code == 403

    @pytest.mark.run(order=51)
    def test_house_booking_without_login(self, client, db_no_rollback):
        data = {
            'house_id': 1,
            'date_begin': '2019-03-01',
            'date_end': '2019-03-02'
        }
        response = self.post(client, '/create_booking', data)
        assert response.status_code == 403

    @pytest.mark.run(order=52)
    def test_house_booking_request_method_is_get(self, client, db_no_rollback):
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
            'house_id': house_id,
            'date_begin': '2019-03-01',
            'date_end': '2019-03-02'
        }
        response = self.get(client, '/create_booking', data)
        assert response.status_code == 405

    @pytest.mark.run(order=52)
    def test_house_booking_request_method_is_post(self, client, db_no_rollback):
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
            'house_id': house_id,
            'date_begin': '2019-03-01',
            'date_end': '2019-03-02'
        }
        response = self.post(client, '/create_booking', data)
        assert response.status_code == 200

        response_json = response.json()
        assert response_json['success'] == 1

    @pytest.mark.run(order=53)
    def test_house_booking_has_already_booked(self, client, db_no_rollback):
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
            'house_id': house_id,
            'date_begin': '2019-03-01',
            'date_end': '2019-03-02'
        }
        response = self.post(client, '/create_booking', data)
        assert response.status_code == 404

        response_json = response.json()
        assert response_json['success'] == 0
        assert response_json['msg'] == error_msg.HAS_ALREADY_BOOKED

    @pytest.mark.run(order=54)
    def test_house_booking_validation_error(self, client, db_no_rollback):
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
            'house_id': house_id,
            'date_begin': '2019-03-01',
        }
        response = self.post(client, '/create_booking', data)
        assert response.status_code == 400

        response_json = response.json()
        assert response_json['success'] == 0

    @pytest.mark.run(order=55)
    def test_house_booking_date_invalid(self, client, db_no_rollback):
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
            'house_id': house_id,
            'date_begin': '2019-03-01',
            'date_end': '2019-02-01'
        }
        response = self.post(client, '/create_booking', data)
        assert response.status_code == 400

        response_json = response.json()
        assert response_json['success'] == 0
        assert response_json['msg'] == error_msg.WRONG_DATE_BEGIN_END

    @pytest.mark.run(order=56)
    def test_house_booking_already_exist(self, client, db_no_rollback):
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
            'house_id': house_id,
            'date_begin': '2019-03-01',
            'date_end': '2019-03-02'
        }
        response = self.post(client, '/create_booking', data)
        assert response.status_code == 404

        response_json = response.json()
        assert response_json['success'] == 0
        assert response_json['msg'] == error_msg.HAS_ALREADY_BOOKED

    @pytest.mark.run(order=57)
    def test_house_booking_key_error(self, client, db_no_rollback):
        self.login(client, self.email, self.password)

        data = {
            'date_begin': '2019-03-01',
            'date_end': '2019-03-02'
        }
        response = self.post(client, '/create_booking', data)
        assert response.status_code == 400

        response_json = response.json()
        assert response_json['success'] == 0

    @pytest.mark.run(order=59)
    def test_downloading_house_photo_photo_does_not_exist(self, client, db_no_rollback):
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
            'house_id': house_id,
        }
        response = self.get(client, '/download_photos', data)

        assert response.status_code == 404

        response_json = response.json()
        assert response_json['success'] == 0
        assert response_json['msg'] == error_msg.PHOTOS_DOES_NOT_EXIST

    @pytest.mark.run(order=60)
    def test_uploading_house_photo(self, client, db_no_rollback):
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

        with open('test/photo_for_test/test0.jpg', 'rb') as f:
            data = {
                'house_id': house_id,
                'photo': f
            }
            response = self.post(client, '/upload_photo', data)

        assert response.status_code == 200

        response_json = response.json()
        assert response_json['success'] == 1

    @pytest.mark.run(order=61)
    def test_downloading_house_photo_success(self, client, db_no_rollback):
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
            'house_id': house_id,
        }
        response = self.get(client, '/download_photos', data)

        assert response.status_code == 200

        response_json = response.json()
        assert response_json['success'] == 1
        assert response_json['number_of_photos'] == 1

    @pytest.mark.run(order=62)
    def test_downloading_house_photo_object_does_not_exist(self, client, db_no_rollback):
        self.login(client, self.email, self.password)

        data = {
            'house_id': 0,
        }
        response = self.get(client, '/download_photos', data)

        assert response.status_code == 404

    @pytest.mark.run(order=63)
    def test_getting_comment_error_comment_does_not_exist(self, client, db_no_rollback):
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
            'house_id': house_id
        }
        response = self.get(client, '/get_comments', data)

        assert response.status_code == 404

        response_json = response.json()
        assert response_json['success'] == 0
        assert response_json['msg'] == error_msg.COMMENT_DOES_NOT_EXIST

    @pytest.mark.run(order=64)
    def test_creating_comment_success(self, client, db_no_rollback):
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
            'house_id': house_id,
            'comment': 'this house is so great!'
        }
        response = self.post(client, '/create_comment', data)

        assert response.status_code == 200

        response_json = response.json()
        assert response_json['success'] == 1

    @pytest.mark.run(order=65)
    def test_getting_comment_success(self, client, db_no_rollback):
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
            'house_id': house_id
        }
        response = self.get(client, '/get_comments', data)

        assert response.status_code == 200

        response_json = response.json()
        assert response_json['success'] == 1
        assert response_json['info'] == [{self.email : 'this house is so great!'}]
        assert response_json['number_of_comments'] == 1

    @pytest.mark.run(order=66)
    def test_getting_comment_key_error(self, client, db_no_rollback):
        self.login(client, self.email, self.password)

        response = self.get(client, '/get_comments')

        assert response.status_code == 400

        response_json = response.json()
        assert response_json['success'] == 0

    @pytest.mark.run(order=67)
    def test_getting_comment_key_error(self, client, db_no_rollback):
        self.login(client, self.email, self.password)

        response = self.post(client, '/create_comment')

        assert response.status_code == 400

        response_json = response.json()
        assert response_json['success'] == 0