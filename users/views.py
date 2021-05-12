"""User views module."""

# django imports
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views

# exceptions
from django.db.utils import IntegrityError

# import django models
from django.contrib.auth.models import User

# import site models
from posts.models import Post
from users.models import Profile
from users.forms import SignupForm

class UserDetailView(LoginRequiredMixin, DetailView):
    """User detail page template view."""
    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Adds user's posts to context."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        return context

class SignupView(FormView):
    """Create view for users to signup."""
    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update users profile view."""
    template_name = 'users/update-profile.html'
    model = Profile
    fields = ['website', 'biography', 'phone_numbers', 'picture']

    def get_object(self):
        """Return users profile."""
        return self.request.user.profile

    def get_success_url(self):
        """Return to users profile."""
        username = self.object.user.username

        return reverse('users:detail', kwargs={'username': username})

class LoginView(auth_views.LoginView):
    """Users login view."""
    template_name = 'users/login.html'
    # prevents the user from going to the login view when they already have a session
    redirect_authenticated_user = True

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout user view."""
    next_page = reverse_lazy('users:login')