from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView

from content.models import Publication
from content.forms import PublicationForm


class HomePage(TemplateView):
    template_name = "content/home_page.html"


class PublicationCreateView(CreateView):
    model = Publication
    form_class = PublicationForm
    success_url = reverse_lazy("home")


class PublicationListView(ListView):
    model = Publication


class PublicationUpdateView(UpdateView):
    model = Publication
    form_class = PublicationForm
    success_url = reverse_lazy("home")
