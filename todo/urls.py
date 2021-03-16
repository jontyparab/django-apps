from django.urls import path

from . import views

# https://docs.djangoproject.com/en/3.0/topics/http/urls/

# To make {% url 'portfolio:cats' %} work in templates
# Also, add namespace in project urls.py

app_name = 'todo'

# Note use of plural for list view and singular for detail view
urlpatterns = [
    path('', views.Todo.as_view(), name='todo'),

]
