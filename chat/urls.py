from django.conf import settings
from django.urls import path
from django.urls import re_path
from django.conf.urls.static import static

from . import views

app_name='chat'
urlpatterns = [
    path('', views.Chat.as_view(), name='chatapp'),
    path('<str:username>/', views.Chat.as_view(), name='chat'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
