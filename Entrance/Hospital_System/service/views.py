from django.shortcuts import render


def run_service(request):
    context = {'hello': 'Hello World!'}
    return render(request, 'service.html', context)
# Create your views here.
