from django.test import TestCase, RequestFactory

from typing import List
from YH15.models import Bar
from tests.YH15.test_views import create_test_bar_list
from unittest.mock import MagicMock, patch
from YH15.views import (
    ListBarView,
    FilterBarView,
    SearchBarView,
    BAR_SEARCH,
    BAR_FILTER,
    RecommendBarView,
)
from YH15 import views as views


class TestBarRecommendation(TestCase):
    def setUp(self) -> None:
        self.bar_list: List[Bar] = create_test_bar_list()
        self.factory = RequestFactory()

    def test_bar_recommendation(self) -> None:
        with patch("YH15.views.get_current_bar_query",
                   MagicMock(
                       return_value=self.bar_list,
                   )
                   ):
            request = self.factory.get("/YH15/")
            response = RecommendBarView().get(request)
            self.assertEqual(
                response.status_code,
                200
            )


class TestBarList(TestCase):
    def setUp(self) -> None:
        self.bar_list: List[Bar] = create_test_bar_list()
        self.factory = RequestFactory()

    def test_bar_list(self) -> None:
        request = self.factory.get("/YH15/")
        response = ListBarView().get(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(BAR_SEARCH)
        self.assertIsNone(BAR_FILTER)


class TestBarSearch(TestCase):
    def setUp(self) -> None:
        self.bar_list: List[Bar] = create_test_bar_list()
        self.factory = RequestFactory()

    def test_bar_search(self) -> None:
        with self.assertRaises(ValueError):
            request = self.factory.get("/YH15/")
            SearchBarView().get(request)

        request = self.factory.get("/YH15/search/?name=bar")
        response = SearchBarView().get(request)
        self.assertEqual(response.status_code, 200)


class TestBarFilter(TestCase):
    def setUp(self) -> None:
        self.bar_list: List[Bar] = create_test_bar_list()
        self.factory = RequestFactory()

    def test_filter_bar(self) -> None:
        request = self.factory.get("/YH15/filter/?rating=&capacity=100&occupancy=")
        response = FilterBarView().get(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.get("/YH15/filter/?rating=&capacity=&occupancy=100")
        response = FilterBarView().get(request)
        self.assertEqual(response.status_code, 200)

        views.BAR_SEARCH = None
        request = self.factory.get("/YH15/filter/?rating=&capacity=&occupancy=100")
        response = FilterBarView().get(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.get("/YH15/filter/?rating=&capacity=&occupancy=")
        response = FilterBarView().get(request)
        self.assertEqual(response.status_code, 200)
