from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
# Create your views here.
from .models import Link
from blog.views import CommonViewMixin


class LinkListView(CommonViewMixin, ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'
