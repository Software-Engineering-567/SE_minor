from django_webtest import WebTest


class SystemTest(WebTest):


    def test_get_list(self):
        self.app.get()
