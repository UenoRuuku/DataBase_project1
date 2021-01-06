from django.shortcuts import render
from django.template import RequestContext


def run_service(request):
    context = {'hello': 'Hello World!', 'dis': "none"}
    return render(request, 'login.html', context)
# Create your views here.
