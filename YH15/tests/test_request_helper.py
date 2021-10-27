from django.test import TestCase
from YH15.request_helper import RequestHelper


class TestRequestHelper(TestCase):

    def test_get_all_bar_models(self) -> None:
        RequestHelper.get_all_bar_models()