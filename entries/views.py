from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q, Count, Avg
from django.db.models.functions import TruncMonth, TruncDate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Entry
from .forms import EntryForm, SearchForm
from taggit.models import Tag
from .sentiment import get_sentiment

import json
import calendar
from collections import OrderedDict
from django.utils import timezone
from dateutil.relativedelta import relativedelta


@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Entry deleted successfully.')
        return redirect('entry-list')
    return render(request, 'entries/entry_confirm_delete.html', {'entry': entry})


def mood_chart_data():
    entries = Entry.objects.annotate(date=TruncDate('date_created')) \
                       .values('date') \
                       .annotate(avg_sentiment=Avg('sentiment_score')) \
                       .order_by('date')
    dates = [e['date'].strftime('%Y-%m-%d') for e in entries]
    sentiments = [e['avg_sentiment'] for e in entries]
    return dates, sentiments


class EntryListView(ListView):
    model = Entry
    template_name = 'entries/entry_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().order_by('-date_created')
        form = SearchForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data

            if data['query']:
                qs = qs.filter(
                    Q(title__icontains=data['query']) |
                    Q(content__icontains=data['query'])
                )
            if data['tags']:
                tag_list = [t.strip() for t in data['tags'].split(',') if t.strip()]
                for tag in tag_list:
                    qs = qs.filter(tags__name__iexact=tag)

            if data['date_from']:
                qs = qs.filter(date_created__date__gte=data['date_from'])
            if data['date_to']:
                qs = qs.filter(date_created__date__lte=data['date_to'])

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = SearchForm(self.request.GET)
        return ctx


def mood_chart(request):
    dates, sentiments = mood_chart_data()
    context = {
        'dates': json.dumps(dates),
        'sentiments': json.dumps(sentiments),
    }
    return render(request, 'entries/mood_chart.html', context)


class EntryDetailView(DetailView):
    model = Entry


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'entries/create_entry.html'
    success_url = reverse_lazy('entry-list')

    def form_valid(self, form):
        entry = form.save(commit=False)
        entry.user = self.request.user
        entry.sentiment_score = get_sentiment(entry.content)
        entry.save()
        return super().form_valid(form)


def entry_stats(request):
    try:
        # Annotate counts per month
        qs = (
            Entry.objects
            .annotate(month=TruncMonth('date_created'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        # Prepare an ordered dict for the last 6 months
        months = OrderedDict()
        for i in range(5, -1, -1):
            m = (timezone.now().date().replace(day=1)
                 - relativedelta(months=i))
            months[m] = 0

        # Fill in actual counts
        for item in qs:
            m_date = item['month'].date() if item['month'] else None
            if m_date:
                month_key = m_date.replace(day=1)
                if month_key in months:
                    months[month_key] = item['count']

        labels = [calendar.month_name[m.month] for m in months.keys()]
        counts = list(months.values())

        # Tag stats
        tag_qs = (
            Tag.objects
            .annotate(count=Count('taggit_taggeditem_items'))
            .order_by('-count')
        )
        tag_labels = [tag.name for tag in tag_qs]
        tag_counts = [tag.count for tag in tag_qs]

    except Exception as e:
        labels, counts, tag_labels, tag_counts = [], [], [], []
        print(f"Error in entry_stats view: {e}")

    return render(request, 'entries/stats.html', {
        'labels': labels,
        'counts': counts,
        'tag_labels': tag_labels,
        'tag_counts': tag_counts,
    })


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def create_entry_view(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.sentiment_score = get_sentiment(entry.content)
            entry.save()
            messages.success(request, "Entry created successfully!")
            return redirect('entry-list')
    else:
        form = EntryForm()
    return render(request, 'entries/create_entry.html', {'form': form})


