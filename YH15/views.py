from django.http import HttpResponse
from django.template import loader
from django.db.models.query import QuerySet
from django.db.models import Q
from YH15.models import Bar
from django.views.generic import DetailView
from YH15.filter import BarFilter
from typing import List, Dict
import random

BAR_SEARCH = None
"""Cache the existing search request, prepare for a possible next user request."""

BAR_FILTER = None
"""Cache the existing filter request, prepare for a possible next user request."""

def get_current_bar_query() -> QuerySet:
    global BAR_SEARCH
    bar_search = BAR_SEARCH
    global BAR_FILTER
    bar_filter = BAR_FILTER
    if bar_search is not None:
        bar_list = Bar.objects.filter(
            Q(bar_name__icontains=bar_search)
        )
    elif bar_filter is not None:
        bar_list = BarFilter.filter_bars(BAR_FILTER)
    else:
        bar_list = Bar.objects.all()
    return bar_list


class ListBarView(DetailView):
    DEFAULT_TEMPLATE = 'YH15/list.html'

    @staticmethod
    def get_default_bars() -> QuerySet:
        """Get all the bars sorted by bar rating by default."""
        return Bar.objects.order_by('-bar_rating')[:]

    def get(self, request, *args, **kwargs) -> HttpResponse:
        # Reset previous search request, because we are querying for all()
        global BAR_SEARCH
        BAR_SEARCH = None
        # Reset previous search request, because we are querying for all()
        BarFilter.reset_filter_query()
        # Query for all available bars, send the result in 'context' to list.html
        bar_list = ListBarView.get_default_bars()
        template = loader.get_template(ListBarView.DEFAULT_TEMPLATE)
        context = {
            'bar_list': bar_list,
        }
        return HttpResponse(template.render(context, request))


class SearchBarView(DetailView):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        # Get and save the search information from current request
        query = request.GET.get('name')
        global BAR_SEARCH
        BAR_SEARCH = query
        # Query the bars with search conditions
        bar_list = Bar.objects.filter(
            Q(bar_name__icontains=query)
        )
        bar_list = bar_list.order_by('-bar_name')[:]
        template = loader.get_template('YH15/search.html')
        context = {
            'bar_list': bar_list,
        }
        return HttpResponse(template.render(context, request))


class SortBarView(DetailView):
    DEFAULT_TEMPLATE = 'YH15/sort.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        return SortBarView.sort_bars(request)

    @staticmethod
    def sort_bars(request) -> HttpResponse:
        # Prepare to check if the current sort-request should be based on a searched or filtered list.
        bar_list = get_current_bar_query()
        sort_type = request.GET.get('sort_type')
        sort_order = request.GET.get('sort_order')
        if sort_order == 'high_low':
            bar_list = bar_list.order_by(f'-bar_{sort_type}')[:]
        else:
            bar_list = bar_list.order_by(f'-bar_{sort_type}')[::-1]
        template = loader.get_template('YH15/sort.html')
        context = {
            'bar_list': bar_list,
        }
        return HttpResponse(template.render(context, request))


class FilterBarView(DetailView):
    DEFAULT_TEMPLATE = 'YH15/filter.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        return FilterBarView.filter_bars(request)

    @staticmethod
    def filter_bars(request) -> HttpResponse:
        global BAR_FILTER
        BAR_FILTER = request
        bar_list = BarFilter.filter_bars(request)
        context = {
            'bar_list': bar_list,
        }
        template = loader.get_template(FilterBarView.DEFAULT_TEMPLATE)
        return HttpResponse(template.render(context, request))


def get_bar_details(request, bar_id: int) -> HttpResponse:
    bar = Bar.objects.get(id=bar_id)
    bar_name = bar.bar_name
    return HttpResponse("You're looking at bar %s." % bar_name)


class RecommendBarView(DetailView):
    DEFAULT_TEMPLATE = 'YH15/recommend.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        return RecommendBarView.recommend_bars(request)

    @staticmethod
    def recommend_bars(request) -> HttpResponse:
        bar_query = get_current_bar_query()
        bar_list = list(bar_query)
        random.shuffle(bar_list)
        bars = RecommendBarView.rank_bars(bar_list)
        bar_name = bars[0].bar_name
        bar = Bar.objects.filter(
            Q(bar_name__iexact=bar_name)
        )
        context = {
            'bar_list': bar,
        }
        template = loader.get_template(RecommendBarView.DEFAULT_TEMPLATE)
        return HttpResponse(template.render(context, request))

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
