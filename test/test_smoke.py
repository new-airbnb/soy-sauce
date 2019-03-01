import pytest


class TestSmoke:
    # this class should be the first suite of test to run
    # order range: 1~10

    @pytest.mark.run(order=1)
    def test_index(self, client):
        response = client.get('/')
        assert response.status_code == 200

    @pytest.mark.run(order=2)
    def test_ping(self, client):
        response = client.get('/ping')
        assert response.status_code == 200
        assert response.content.decode('utf8') == 'pong'
