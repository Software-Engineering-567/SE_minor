from django.http import HttpResponse
from django.template import loader
from django.db.models import Q
from YH15.models import Bar

# To save a search user request, prepare for a possible next user request
BAR_SEARCH = None
# To save a filter user request, prepare for a possible next user request
BAR_FILTER = None

# Generates list: all available bars
def list(request):
    # Reset previous search request, because we are querying for all()
    global BAR_SEARCH
    BAR_SEARCH = None
    # Reset previous search request, because we are querying for all()
    global BAR_FILTER
    BAR_FILTER = None
    # Query for all available bars, send the result in 'context' to list.html
    bar_list = Bar.objects.order_by('-bar_rating')[:]
    template = loader.get_template('YH15/list.html')
    context = {
        'bar_list': bar_list,
    }
    return HttpResponse(template.render(context, request))

# Generates list: search-resulted bars
def search(request):
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

# Generates list: filter-resulted bars
def to_filter(request):
    # Be prepare to check if the current filter-request should be based on a searched list
    global BAR_SEARCH
    bar_search = BAR_SEARCH
    # If yes, based on a searched list:
    if bar_search is not None:
        # Re-query the searched list with latest information
        bar_list = Bar.objects.filter(
            Q(bar_name__icontains=bar_search)
        )
    # If no, just based on a list of all:
    else:
        # Re-query the list of all with latest information
        bar_list = Bar.objects.order_by('-bar_rating')[:]
    rating = request.GET.get('rating')
    capacity = request.GET.get('capacity')
    occupancy = request.GET.get('occupancy')
    # If we have at least 1 input for the above 3 definitions:
    if rating != '' or capacity != '' or occupancy != '':
        # If we have any None input, set it as 0:
        if rating == '':
            rating = '0'
        if capacity == '':
            capacity = '0'
        if occupancy == '':
            occupancy = '0'
        bar_list = bar_list.filter(bar_rating__range=(rating, 5))
        bar_list = bar_list.filter(bar_capacity__range=(capacity, 99999))
        bar_list = bar_list.filter(bar_occupancy__range=(occupancy, 99999))
    # If we have no input for all 3 definitions
    else:
        # Reset the filter information
        global BAR_FILTER
        BAR_FILTER = None
        bar_list = bar_list.order_by('-bar_rating')[:]
    return bar_list

# Generates list: sort resulted list
def sort(request):
    # Prepare to check if the current sort-request should be based on a searched or filtered list
    global BAR_SEARCH
    bar_search = BAR_SEARCH
    global BAR_FILTER
    bar_filter = BAR_FILTER
    # If yes, based on a search resulted list:
    if bar_search is not None:
        # Re-query the searched list with latest information
        bar_list = Bar.objects.filter(
            Q(bar_name__icontains=bar_search)
        )
    # If yes, based on a filter resulted list:
    elif bar_filter is not None:
        # Re-query the filtered list with latest information
        bar_list = to_filter(BAR_FILTER)
    # If no, just based on a list of all
    else:
        # Re-query a list of all with latest information
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
