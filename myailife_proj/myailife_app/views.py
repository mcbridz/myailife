from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {}
    return render(request, 'myailife_app/index.html', context)
