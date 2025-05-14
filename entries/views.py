from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth

from .models import Entry
from .forms import EntryForm, SearchForm
from taggit.models import Tag

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

            # Tag filtering
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

def entry_stats(request):
    try:
        qs = (
            Entry.objects
            .annotate(month=TruncMonth('date_created'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        labels = [item['month'].strftime("%Y-%m") for item in qs if item['month']]
        counts = [item['count'] for item in qs]

    except Exception as e:
        # Fallback in case of failure
        labels = []
        counts = []
        print(f"Error in entry_stats view: {e}")  # Good for debugging in dev

    return render(request, 'entries/stats.html', {
        'labels': labels,
        'counts': counts,
    })

    
    

    # 2) Build lists for Chart.js
    labels = [item['month'].strftime("%Y-%m") for item in qs]
    counts = [item['count'] for item in qs]

     # 3) Annotate each tag with the number of entries using it
    tag_qs = (
        Tag.objects
        .annotate(count=Count('taggit_taggeditem_items'))
        .order_by('-count')
    )
    tag_labels = [tag.name for tag in tag_qs]
    tag_counts = [tag.count for tag in tag_qs]

    # 4) Render the stats template with BOTH data sets
    return render(request, 'entries/stats.html', {
        'labels':      labels,
        'counts':      counts,
        'tag_labels':  tag_labels,
        'tag_counts':  tag_counts,
    })

