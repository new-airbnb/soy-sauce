class BaseTest:
    prefix = ''  # in derived classes, set to, for example, '/user', '/house'

    def get(self, client, url, *args, **kwargs):
        if "user_operate" not in kwargs:
            url = self.prefix + url
        return client.get(url, *args, **kwargs)

    def post(self, client, url, *args, **kwargs):
        if "user_operate" not in kwargs:
            url = self.prefix + url
        return client.post(url, *args, **kwargs)

    def create_user(self, client, email, password):
        data = {
            "email": email,
            "password": password
        }
        response = self.post(client, "/user/register", data, user_operate=True)
        assert response.status_code == 200

    def login(self, client, email, password):
        data = {
            "email": email,
            "password": password,
            "remember_me": 'false'
        }
        response = self.post(client, "/user/login", data, user_operate=True)
        assert response.status_code == 200
