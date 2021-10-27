from typing import List
from unittest.mock import MagicMock, patch

from django.test import TestCase, RequestFactory

from YH15.models import Bar
from YH15.views import (
    ListBarView,
    FilterBarView,
    SearchBarView,
    RecommendBarView,
)
from YH15.tests.test_views import create_test_bar_list

class TestBarRecommendation(TestCase):
    def setUp(self) -> None:
        self.bar_list: List[Bar] = create_test_bar_list()
        self.factory = RequestFactory()

    def test_bar_recommendation(self) -> None:
        with patch("YH15.request_helper.RequestHelper.get_current_bar_query",
                   MagicMock(
                       return_value=self.bar_list,
                   )
                   ):
            request = self.factory.get("/YH15/")
            response = RecommendBarView().get(request)
            
            self.assertEqual(
                response.headers,
                {'Content-Type': 'text/html; charset=utf-8'}
            )

            self.assertEqual(
                len(response.content),
                511
            )

            self.assertIn(
                b'<td>Index</td>\n',
                response.content,
            )

            self.assertIn(
                b'<td>Index</td>\n',
                response.content,
            )

            self.assertIn(
                b'<td>Bar Name</td>\n',
                response.content,
            )

            self.assertIn(
                b'<td>Rating</td>\n',
                response.content,
            )

            self.assertIn(
                b'<td>Capacity</td>\n',
                response.content,
            )

            self.assertIn(
                b'<td>Occupancy</td>\n',
                response.content,
            )

            self.assertIn(
                b'test_bar_name_2',
                response.content,
            )

            self.assertIn(
                b'0.3',
                response.content,
            )

            self.assertIn(
                b'980',
                response.content,
            )

            self.assertIn(
                b'480',
                response.content,
            )


class TestBarList(TestCase):
    def setUp(self) -> None:
        self.bar_list: List[Bar] = create_test_bar_list()
        self.factory = RequestFactory()

    def test_bar_list(self) -> None:
        request = self.factory.get("/YH15/")
        response = ListBarView().get(request)
        self.assertEqual(response.status_code, 200)

        self.assertIn(
            b'csrfmiddlewaretoken',
            response.content,
        )

        self.assertEqual(
            len(response.content),
            3187,
        )


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
        self.assertIn(
            b'csrfmiddlewaretoken',
            response.content,
        )

        self.assertEqual(
            len(response.content),
            3033,
        )


class TestBarFilter(TestCase):
    def setUp(self) -> None:
        self.bar_list: List[Bar] = create_test_bar_list()
        self.factory = RequestFactory()

    def test_filter_bar(self) -> None:
        request = self.factory.get("/YH15/filter/?rating=&capacity=100&occupancy=")
        response = FilterBarView().get(request)

        self.assertIn(
            b'csrfmiddlewaretoken',
            response.content,
        )

        self.assertEqual(
            len(response.content),
            2583,
        )