from django.urls import path 
from django_books.views import support

urlpatterns = [
    path('', support, name='support')
]