from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from .forms import LoginUserForm, SignInUserForm, ProfileUserForm, UserPasswordChangeForm

from books.models import Book, Review
from bookworm import settings


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Log in'}


class SignInUser(CreateView):
    form_class = SignInUserForm
    template_name = 'users/signin.html'
    extra_context = {'title': 'Sign in'}
    success_url = reverse_lazy('users:login')


class ChangeProfileInfo(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/change_profile.html'
    extra_context = {'title': 'Change Profile',
                     'default_avatar': settings.DEFAULT_USER_AVATAR,
                     }

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.request.user.pk])

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUser(DetailView):
    model = get_user_model()
    template_name = 'users/profile.html'
    context_object_name = 'user'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        user_books = Book.published.filter(user=user)
        user_reviews = Review.objects.filter(user=user)

        context['user_books'] = user_books
        context['user_reviews'] = user_reviews
        context['default_avatar'] = settings.DEFAULT_USER_AVATAR
        context['title'] = f'{user} profile'
        context['is_authenticated'] = self.request.user.is_authenticated
        return context


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'

