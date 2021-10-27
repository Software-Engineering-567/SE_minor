from django.db.models.query import QuerySet
from django.db.models import Q

from YH15.models import Bar


class RequestHelper:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(RequestHelper, cls).__new__(cls)
        return cls.instance

    bar_search_request = None
    """Cache the existing search request, prepare for a possible next user request."""

    bar_filter_request = None
    """Cache the existing filter request, prepare for a possible next user request."""

    @staticmethod
    def get_current_bar_query() -> QuerySet:
        """Return the cached filter or search query."""

        if RequestHelper.bar_search_request is not None:
            return Bar.objects.filter(
                Q(bar_name__icontains=RequestHelper.bar_search_request)
            )
        if RequestHelper.bar_filter_request is not None:
            from YH15.filter import BarFilter

            return BarFilter.filter_bars(RequestHelper.bar_filter_request)

        return RequestHelper.get_all_bar_models()

    @staticmethod
    def get_all_bar_models() -> QuerySet:
        return Bar.objects.all()

    @staticmethod
    def cache_search_request(search_query: QuerySet) -> None:
        RequestHelper.bar_search_request = search_query
        return None

    @staticmethod
    def cache_filter_request(filter_query: QuerySet) -> None:
        RequestHelper.bar_filter_request = filter_query
        return None

    @staticmethod
    def reset_search_request() -> None:
        RequestHelper.bar_search_request = None
        return None

    @staticmethod
    def reset_filter_request() -> None:
        RequestHelper.bar_filter_request = None
        return None
