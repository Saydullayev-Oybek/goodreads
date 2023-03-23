from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from users.forms import UserCreateForm


class RegisterView(View):

    def get(self, request):
        user_form = UserCreateForm()
        context = {
            'user_form': user_form
        }

        return render(request, 'registration/register.html', context=context)

    def post(self, request):
        user_form = UserCreateForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('login')

        else:
            user_form = UserCreateForm(data=request.POST)
            context = {
                'user_form': user_form
            }

            return render(request, 'registration/register.html', context=context)




# class RegisterView(View):
#     def get(self, request):
#         return render(request, 'registration/register.html')
#
#     def post(self, request):
#         username = request.POST['username']
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         password = request.POST['password']
#         email = request.POST['email']
#
#         user = User.objects.create(
#             username=username,
#             first_name=first_name,
#             last_name=last_name,
#             email=email
#         )
#         user.set_password(password)
#         user.save()
#
#         return redirect('login')

class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'registration/login.html', context=context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)

            return redirect('home')
        else:
            return render(request, 'registration/login.html', {'login_form': login_form})


class HomePage(View):
    def get(self, request):
        return render(request, 'home.html')

