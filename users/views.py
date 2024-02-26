from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from content.models import Publication
from users.forms import UserRegisterForm, UserProfileChangeForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("home")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileChangeForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("user:profile_view", args=[self.object.pk])


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        author = self.object
        user = self.request.user
        posts = Publication.objects.filter(owner=author)
        context["posts"] = posts
        if context["object"] == user:
            context["is_current_user"] = True
        else:
            if context["object"] in user.subscriptions.all():
                context["is_subscribed"] = True
                subscribers = User.objects.filter(subscriptions=author)
                context["subscribers"] = subscribers
        return context


class UserSubscribeView(View):
    def get(self, request, pk):
        author = User.objects.get(pk=pk)
        user = request.user

        if author in user.subscriptions.all():
            user.subscriptions.remove(author)
        else:
            user.subscriptions.add(author)

        return redirect(reverse_lazy("user:profile_view", args=[author.pk]))


class SubscriptionListView(ListView):
    template_name = "users/subscriptions.html"

    def get_queryset(self, **kwargs):
        user = self.request.user

        subscriptions = user.subscriptions.all()

        return subscriptions
