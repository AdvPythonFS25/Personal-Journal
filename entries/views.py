from django.shortcuts import render
#  Views to display the list of entries and details of a single entry


from django.views.generic import (
    ListView,
    DetailView,
)

from .models import Entry

class EntryListView(ListView):
    model = Entry
    queryset = Entry.objects.all().order_by("-date_created")

class EntryDetailView(DetailView):
    model = Entry
