from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    UpdateView,
    DetailView,
    DeleteView,
)

from content.forms import PublicationForm
from content.models import Publication, Likes, Dislikes
from content.services import toggle_like, toggle_dislike
from users.models import User


class HomePage(TemplateView):

    template_name = "content/home_page.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        users = User.objects.all()
        if users.count() > 1:
            the_most_popular_author = None
            prev_subscriber_counter = 0
            for author in users:
                subscriber_counter = 0
                for user in users:
                    if author in user.subscriptions.all():
                        subscriber_counter += 1
                if subscriber_counter > prev_subscriber_counter:
                    prev_subscriber_counter = subscriber_counter
                    the_most_popular_author = author
            context["the_most_popular_author"] = the_most_popular_author

        posts = Publication.objects.order_by("-views_count")
        if posts:
            context["the_most_popular_post"] = posts[0]

        return context


class NoPermPage(TemplateView):
    template_name = "content/no_permission.html"


class PublicationCreateView(LoginRequiredMixin, CreateView):
    model = Publication
    form_class = PublicationForm
    raise_exception = False

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        users = User.objects.all()

        for user in users:
            Likes.objects.create(user=user, publication=self.object)
            Dislikes.objects.create(user=user, publication=self.object)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("content:publication_detail", args=[self.object.pk])


class PublicationListView(ListView):
    model = Publication
    context_object_name = "posts"


class PublicationDetailView(DetailView):
    model = Publication
    context_object_name = "post"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        if user.pk is None:
            return context

        obj = self.object
        try:
            like = Likes.objects.get(user=user, publication=obj)

            if like.is_active:
                context["is_liked"] = True
            else:
                context["is_liked"] = False

        except ObjectDoesNotExist:
            context["is_liked"] = False

        try:
            dislike = Dislikes.objects.get(user=user, publication=obj)

            if dislike.is_active:
                context["is_disliked"] = True
            else:
                context["is_disliked"] = False

        except ObjectDoesNotExist:
            context["is_disliked"] = False

        like_counter = Likes.objects.filter(publication=obj, is_active=True).count()
        dislike_counter = Dislikes.objects.filter(
            publication=obj, is_active=True
        ).count()

        context["like_counter"] = like_counter
        context["dislike_counter"] = dislike_counter

        return context


class PublicationUpdateView(LoginRequiredMixin, UpdateView):
    model = Publication
    form_class = PublicationForm

    def get(self, request, *args, **kwargs):
        if request.user == self.get_object().owner:
            self.object = self.get_object()
            return super().get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy("no_perm"))

    def get_success_url(self):
        return reverse_lazy("content:publication_detail", args=[self.object.pk])


class PublicationDeleteView(DeleteView):
    model = Publication

    def get(self, request, *args, **kwargs):
        if request.user == self.get_object().owner:
            self.object = self.get_object()
            return super().get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy("no_perm"))

    def get_success_url(self):
        return reverse_lazy("content:list_publications")


class SetLikeView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Publication.objects.get(pk=pk)
        user = request.user
        like = Likes.objects.get_or_create(user=user, publication=post)[0]
        dislike = Dislikes.objects.get_or_create(user=user, publication=post)[0]

        if dislike.is_active:
            toggle_dislike(dislike)
            toggle_like(like)
        else:
            toggle_like(like)

        return redirect(request.META.get("HTTP_REFERER"))


class SetDislikeView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Publication.objects.get(pk=pk)
        user = request.user
        dislike = Dislikes.objects.get_or_create(user=user, publication=post)[0]
        like = Likes.objects.get_or_create(user=user, publication=post)[0]

        if like.is_active:
            toggle_like(like)
            toggle_dislike(dislike)
        else:
            toggle_dislike(dislike)

        return redirect(request.META.get("HTTP_REFERER"))


class SearchListView(ListView):
    model = Publication
    template_name = "content/publication_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Publication.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        return object_list
