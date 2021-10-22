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
    return HttpResponse(template.render(context,request))

def to_filter(request):
    rating = request.GET.get('rating')
    if rating == '':
        rating = '0'
    capacity = request.GET.get('capacity')
    if capacity == '':
        capacity = '0'
    occupancy = request.GET.get('occupancy')
    if occupancy == '':
        occupancy = '0'
    bar_list = Bar.objects.filter(bar_rating__range=(rating, 5))
    bar_list = bar_list.filter(bar_capacity__range=(capacity, 99999))
    bar_list = bar_list.filter(bar_occupancy__range=(occupancy, 99999))
    return bar_list

def sort(request):
    global BAR_SEARCH
    bar_search = BAR_SEARCH
    global BAR_FILTER
    if bar_search is not None:
        bar_list = Bar.objects.filter(
            Q(bar_name__icontains=bar_search)
        )
    elif bar_filter is not None:
        bar_list = to_filter(BAR_FILTER)
    else:
        bar_list = Bar.objects.all()
    sort_type = request.GET.get('sort_type')
    bar_list = bar_list.order_by(f'-bar_{sort_type}')[:]
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