from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.EntryListView.as_view(),
        name="entry-list"
        
    ),
    path(
        "entry/<int:pk>",
        views.EntryDetailView.as_view(),
        name="entry-detail"
    ),

    path('mood-chart/', views.mood_chart, name='mood_chart'),
    path('create/', views.EntryCreateView.as_view(), name='entry-create'),
]
