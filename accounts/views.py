from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View


@login_required
def index(request):
    return render(request, 'accounts/index.html')


class SignUpView(View):
    def get(self, request):
        context = {}
        return render(request, 'registration/sign-up.html', context)

    def post(self, request):
        if request.POST['password1'] == '' or request.POST['username'] == '':
            messages.error(request, 'Username or password cannot be empty.')
        elif len(request.POST['password1']) < 8:
            messages.error(request, 'Password is too short.')
        elif request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                messages.success(request, 'Signed Up and Logged In to your account.')
                return redirect('accounts:home')
            except IntegrityError:
                messages.error(request, 'That username has already been taken. Please choose a new username.')
        else:
            messages.error(request, 'Passwords did not match.')
        return render(request, 'registration/sign-up.html')


class LoginView(View):
    def get(self, request):
        context = {}
        return render(request, 'registration/login.html', context)

    def post(self, request):
        context = {}
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, "Invalid Credentials")
            return render(request, 'registration/login.html')
        else:
            login(request, user)
            messages.success(request, 'Logged In Successfully!!')
            return redirect('accounts:home')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'registration/logged-out.html')

    def post(self, request):
        logout(request)
        messages.info(request, 'Logged out successfully.')
        return redirect('accounts:login')
