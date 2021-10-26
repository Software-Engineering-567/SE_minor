import random
from typing import List, Dict

from django.http import HttpResponse
from django.template import loader
from django.db.models.query import QuerySet
from django.db.models import Q
from django.views.generic import DetailView

from YH15.models import Bar
from YH15.filter import BarFilter
from YH15.query import RequestHelper


def send_http_query(request, bar_list: QuerySet, template: str) -> HttpResponse:
    template = loader.get_template(template)
    context = {
        'bar_list': bar_list,
    }
    return HttpResponse(template.render(context, request))


class ListBarView(DetailView):
    DEFAULT_TEMPLATE: str = 'YH15/list.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        # Reset previous search request, because we are querying for all()
        RequestHelper.reset_search_request()
        # Reset previous search request, because we are querying for all()
        RequestHelper.reset_filter_request()

        return send_http_query(request, ListBarView.get_default_bars(), ListBarView.DEFAULT_TEMPLATE)

    @staticmethod
    def get_default_bars() -> QuerySet:
        """Get all the bars sorted by bar rating by default."""
        return Bar.objects.order_by('-bar_rating')[:]


class SearchBarView(DetailView):
    DEFAULT_TEMPLATE: str = 'YH15/search.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        query = request.GET.get('name')
        RequestHelper.cache_search_request(query)

        return send_http_query(
            request,
            SearchBarView.search_bar_models(),
            SearchBarView.DEFAULT_TEMPLATE,
        )

    @staticmethod
    def search_bar_models() -> QuerySet:
        bar_list = Bar.objects.filter(
            Q(bar_name__icontains=RequestHelper.bar_search_request)
        )
        return bar_list.order_by('-bar_name')[:]


class SortBarView(DetailView):
    DEFAULT_TEMPLATE = 'YH15/sort.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        return send_http_query(
            request,
            SortBarView.sort_bars(request),
            SortBarView.DEFAULT_TEMPLATE
        )

    @staticmethod
    def get_sort_sort_order_and_type(request) -> List[str]:
        return [
            request.GET.get('sort_order'),
            request.GET.get('sort_type'),
        ]

    @staticmethod
    def sort_bars(request) -> QuerySet:
        bar_list = RequestHelper.get_current_bar_query()

        sort_order, sort_type = SortBarView.get_sort_sort_order_and_type(request)

        if sort_order == 'high_low':
            return bar_list.order_by(f'-bar_{sort_type}')[:]

        return bar_list.order_by(f'-bar_{sort_type}')[::-1]


class FilterBarView(DetailView):
    DEFAULT_TEMPLATE = 'YH15/filter.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        return send_http_query(
            request,
            FilterBarView.filter_bars(request),
            SortBarView.DEFAULT_TEMPLATE,
        )

    @staticmethod
    def filter_bars(request) -> QuerySet:
        RequestHelper.cache_filter_request(request)
        return BarFilter.filter_bars(request)


class RecommendBarView(DetailView):
    DEFAULT_TEMPLATE = 'YH15/recommend.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        return send_http_query(
            request,
            RecommendBarView.recommend_bars(request),
            RecommendBarView.DEFAULT_TEMPLATE,
        )

    @staticmethod
    def recommend_bars(request, number: int = 1) -> QuerySet:
        bar_query = RequestHelper.get_current_bar_query()
        bar_list = list(bar_query)
        random.shuffle(bar_list)
        bars = RecommendBarView.rank_bars(bar_list)

        if number > len(bars):
            raise ValueError(f"Requested {number} bars than total {len(bars)} bars!")

        return Bar.objects.filter(
            Q(bar_name__in=[bar.bar_name for bar in bars[:number]])
        )

    @staticmethod
    def rank_bars(bars: List[Bar]) -> List[Bar]:
        secure_scores = RecommendBarView.rank_secure_bars(bars)
        popular_scores = RecommendBarView.rank_popular_bars(bars)
        for index, bar in enumerate(secure_scores):
            secure_scores[bar] += popular_scores[bar]
        sorted_total_scores = sorted(secure_scores.items(), key=lambda item: item[1], reverse=True)
        return [x[0] for x in sorted_total_scores]

    @staticmethod
    def rank_secure_bars(bars: List[Bar]) -> Dict[Bar, int]:
        bar_secure_scores: Dict[Bar, int] = {bar: 0 for bar in bars}
        sorted_bars = sorted(bars, key=lambda bar: bar.occupant_rate)
        for index, bar in enumerate(sorted_bars):
            bar_secure_scores[bar] = RecommendBarView.get_secure_score(index / len(sorted_bars))
        return bar_secure_scores

    @staticmethod
    def rank_popular_bars(bars: List[Bar]) -> Dict[Bar, int]:
        bar_popular_scores: Dict[Bar, int] = {bar: 0 for bar in bars}
        sorted_bars = sorted(bars, key=lambda bar: bar.bar_rating)
        for index, bar in enumerate(sorted_bars):
            bar_popular_scores[bar] += RecommendBarView.get_popular_score(index / len(sorted_bars))
        return bar_popular_scores

    @staticmethod
    def get_secure_score(bar_oc_score) -> int:
        if 0.7 < bar_oc_score <= 0.8:
            return 5
        if 0.6 < bar_oc_score <= 0.7:
            return 4
        if (0.4 < bar_oc_score <= 0.6) or (0.8 < bar_oc_score <= 0.9):
            return 3
        if 0.25 < bar_oc_score <= 0.4:
            return 2
        if (0 < bar_oc_score <= 0.25) or (0.9 < bar_oc_score < 1):
            return 1
        return 0

    @staticmethod
    def get_popular_score(bar_popular_score) -> int:
        if 0.9 < bar_popular_score <= 1:
            return 9
        if 0.75 < bar_popular_score <= 0.9:
            return 7
        if 0.6 < bar_popular_score <= 0.75:
            return 5
        if 0.4 < bar_popular_score <= 0.6:
            return 4
        if 0 < bar_popular_score <= 0.4:
            return 3
        return 0


def get_bar_details(request, bar_id: int) -> HttpResponse:
    bar = Bar.objects.get(id=bar_id)
    bar_name = bar.bar_name
    return HttpResponse("You're looking at bar %s." % bar_name)
