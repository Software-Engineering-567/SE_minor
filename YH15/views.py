from django.http import HttpResponse
from django.template import loader

from YH15.models import Bar


# def index(request):
#     return HttpResponse("Index.")
def list(request):
    bar_list = Bar.objects.order_by('-bar_name')[:]
    template = loader.get_template('YH15/list.html')
    context = {
        'bar_list': bar_list,
    }
    return HttpResponse(template.render(context, request))
    # output = ', '.join([q.bar_name for q in bar_list])
    # return HttpResponse(output)

def details(request, bar_id):
    bar = Bar.objects.get(id = bar_id)
    bar_name = bar.bar_name
    return HttpResponse("You're looking at bar %s." % bar_name)

def info(request, bar_id):
    return HttpResponse("You're looking at the info of bar %s." % bar_id)