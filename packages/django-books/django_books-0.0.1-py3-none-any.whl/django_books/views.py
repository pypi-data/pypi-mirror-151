from django.shortcuts import render
from django.http import HttpResponse

def support(request): 
    html = '<html><body><h1>Hello World!</h1></body></html>'
    return HttpResponse(html)