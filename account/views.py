from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginForm
from .forms import SignUpForm


class MyLoginView(LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'


class MyLogoutView(LogoutView):
    template_name = 'account/logout.html'


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('account:login')
    template_name = 'account/signup.html'
