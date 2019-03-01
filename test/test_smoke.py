class TestSmoke:
    def test_index(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_ping(self, client):
        response = client.get('/ping')
        assert response.status_code == 200
        assert response.content.decode('utf8') == 'pong'
