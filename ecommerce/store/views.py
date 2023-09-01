from django.shortcuts import render
from django.views.generic import ListView, DetailView, View

from .models import Item


class HomeView(ListView):
    model = Item
    # paginate_by = 10
    template_name = "store/home.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "store/product.html"
