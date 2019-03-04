class BaseTest:
    prefix = ''  # in derived classes, set to, for example, '/user', '/house'

    def get(self, client, url, *args, **kwargs):
        url = self.prefix + url
        return client.get(url, *args, **kwargs)

    def post(self, client, url, *args, **kwargs):
        url = self.prefix + url
        return client.post(url, *args, **kwargs)
