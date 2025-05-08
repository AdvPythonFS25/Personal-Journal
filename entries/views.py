from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .models import Entry
from .forms import EntryForm, SearchForm  # <-- import your SearchForm too

class EntryListView(ListView):
    model = Entry
    template_name = 'entries/entry_list.html'
    paginate_by = 10  # optional

    def get_queryset(self):
        qs = super().get_queryset().order_by('-date_created')
        form = SearchForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data

            # Keyword search in title or content
            if data['query']:
                qs = qs.filter(
                    Q(title__icontains=data['query']) |
                    Q(content__icontains=data['query'])
                )

            # Tag filtering (django-taggit)
            if data['tags']:
                tag_list = [t.strip() for t in data['tags'].split(',') if t.strip()]
                for tag in tag_list:
                    qs = qs.filter(tags__name__iexact=tag)

            # Date range
            if data['date_from']:
                qs = qs.filter(date_created__date__gte=data['date_from'])
            if data['date_to']:
                qs = qs.filter(date_created__date__lte=data['date_to'])

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = SearchForm(self.request.GET)
        return ctx


class EntryDetailView(DetailView):
    model = Entry


class EntryCreateView(CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'entries/create_entry.html'
    success_url = reverse_lazy('entry-list')
