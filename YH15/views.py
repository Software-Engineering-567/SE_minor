from django.http import HttpResponse
from django.template import loader
from django.db.models import Q
from YH15.models import Bar

BAR_SEARCH = None
BAR_FILTER = None


def list(request):
    global BAR_SEARCH
    BAR_SEARCH = None
    global BAR_FILTER
    BAR_FILTER = None
    bar_list = Bar.objects.order_by('-bar_rating')[:]
    template = loader.get_template('YH15/list.html')
    context = {
        'bar_list': bar_list,
    }
    return HttpResponse(template.render(context, request))


def search(request):
    query = request.GET.get('name')
    global BAR_SEARCH
    BAR_SEARCH = query
    bar_list = Bar.objects.filter(
        Q(bar_name__icontains=query)
    )
    bar_list = bar_list.order_by('-bar_name')[:]
    template = loader.get_template('YH15/search.html')
    context = {
        'bar_list': bar_list,
    }
    return HttpResponse(template.render(context, request))


def to_filter(request):
    rating = request.GET.get('rating')
    capacity = request.GET.get('capacity')
    occupancy = request.GET.get('occupancy')
    if rating != '' or capacity != '' or occupancy != '':
        if rating == '':
            rating = '0'
        if capacity == '':
            capacity = '0'
        if occupancy == '':
            occupancy = '0'
        bar_list = Bar.objects.filter(bar_rating__range=(rating, 5))
        bar_list = bar_list.filter(bar_capacity__range=(capacity, 99999))
        bar_list = bar_list.filter(bar_occupancy__range=(occupancy, 99999))
    else:
        global BAR_FILTER
        BAR_FILTER = None
        bar_list = Bar.objects.order_by('-bar_rating')[:]
    return bar_list


def sort(request):
    print(request)
    global BAR_SEARCH
    print(BAR_SEARCH)
    bar_search = BAR_SEARCH
    global BAR_FILTER
    bar_filter = BAR_FILTER
    print(BAR_FILTER)
    if bar_search is not None:
        bar_list = Bar.objects.filter(
            Q(bar_name__icontains=bar_search)
        )
    elif bar_filter is not None:
        print("entered")
        bar_list = to_filter(BAR_FILTER)
    else:
        bar_list = Bar.objects.all()
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


def bar_filter(request):
    global BAR_FILTER
    BAR_FILTER = request
    bar_list = to_filter(request)
    context = {
        'bar_list': bar_list,
    }
    template = loader.get_template('YH15/filter.html')
    return HttpResponse(template.render(context, request))


def details(request, bar_id):
    bar = Bar.objects.get(id=bar_id)
    bar_name = bar.bar_name
    return HttpResponse("You're looking at bar %s." % bar_name)
