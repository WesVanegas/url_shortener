#from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.base import RedirectView
from .forms import ShortenerForm
from .models import Link

# Create your views here.
class CreateShortener(CreateView):
    model = Link
    form_class = ShortenerForm
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_links'] = Link.links.total_links()
        context['total_redirections'] = Link.links.total_redirections()['redirections']
        return context
