from django.test import TestCase
from YH15.views import (
    RecommendBarView,
)
from typing import List
from YH15.models import Bar
from tests.YH15.test_views import create_bar_list


class TestBarRecommendation(TestCase):
    def setUp(self) -> None:
        self.bar_list: List[Bar] = create_bar_list()

    # def test_bar_recommendation(self) -> None:
    #     recommend_bar_view = RecommendBarView()
    #     recommend_bar_view.rank_bars(self.bar_list, 1)