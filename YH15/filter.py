from typing import List, Iterable

from django.db.models.query import QuerySet
from django.db.models import Q

from YH15.models import Bar, Numeric
from YH15 import views as views
from YH15.query import RequestHelper


class BarFilter:
    @staticmethod
    def filter_bars(request) -> QuerySet:
        bar_list = BarFilter.get_filter_source()

        filter_rating, filter_capacity, filter_occupancy = BarFilter.get_filter_request(request)

        if BarFilter.is_empty_filter_condition(filter_rating, filter_capacity, filter_occupancy):
            filter_rating, filter_capacity, filter_occupancy = BarFilter.update_empty_filter_conditions(
                [
                    filter_rating, filter_capacity, filter_occupancy
                ]
            )
            return BarFilter.filter_bars_in_range(
                bar_list,
                min_filter_rating=filter_rating,
                min_filter_capacity=filter_capacity,
                min_filter_occupancy=filter_occupancy,
            )

        RequestHelper.reset_filter_request()
        return BarFilter.get_default_bar_list(bar_list)

    @staticmethod
    def is_reuse_bar_search_query() -> bool:
        return RequestHelper.bar_search_request is not None

    @staticmethod
    def get_filter_source() -> QuerySet:
        if BarFilter.is_reuse_bar_search_query():
            bar_list = Bar.objects.filter(
                Q(bar_name__icontains=RequestHelper.bar_search_request)
            )
        else:
            bar_list = Bar.objects.order_by('-bar_rating')[:]
        return bar_list

    @staticmethod
    def get_filter_request(request) -> Iterable[Numeric]:
        return (
            request.GET.get('rating'),
            request.GET.get('capacity'),
            request.GET.get('occupancy'),
        )

    @staticmethod
    def is_empty_filter_condition(filter_rating: str, filter_capacity: str, filter_occupancy: str) -> bool:
        return filter_rating != '' or filter_capacity != '' or filter_occupancy != ''

    @staticmethod
    def update_empty_filter_condition(filter_condition: str) -> str:
        if filter_condition == '':
            return '0'
        return filter_condition

    @staticmethod
    def update_empty_filter_conditions(filter_conditions: List[str]) -> List[str]:
        return [
            BarFilter.update_empty_filter_condition(x) for x in filter_conditions
        ]

    @staticmethod
    def filter_bars_in_range(
            bar_list: QuerySet,
            min_filter_rating: int = 0,
            min_filter_capacity: int = 0,
            min_filter_occupancy: int = 0,
    ) -> QuerySet:
        bar_list = bar_list.filter(bar_rating__range=(min_filter_rating, Bar.MAX_BAR_RATING))
        bar_list = bar_list.filter(bar_capacity__range=(min_filter_capacity, Bar.MAX_BAR_CAPACITY))
        bar_list = bar_list.filter(bar_occupancy__range=(min_filter_occupancy, Bar.MAX_BAR_CAPACITY))
        return bar_list

    @staticmethod
    def get_default_bar_list(bar_list: QuerySet) -> QuerySet:
        return bar_list.order_by('-bar_rating')[:]

