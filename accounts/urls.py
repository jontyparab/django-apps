from django.contrib import admin
from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('', views.index, name="home"),
    path('accounts/sign-up/', views.SignUpView.as_view(), name="sign-up"),
    path('accounts/login/', views.LoginView.as_view(), name="login"),
    path('accounts/logout/', views.LogoutView.as_view(), name="logout")
]
