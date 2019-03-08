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

    def create_user(self, client, email, password, should_succ=True):
        data = {
            "email": email,
            "password": password
        }
        response = self.post(client, "/user/register", data, user_operate=True)
        if should_succ:
            assert response.status_code == 200
        return response

    def login(self, client, email, password, should_succ=True):
        data = {
            "email": email,
            "password": password,
            "remember_me": 'false'
        }
        response = self.post(client, "/user/login", data, user_operate=True)
        if should_succ:
            assert response.status_code == 200
        return response
