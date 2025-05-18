from django.urls import path
from . import views

# Sets up URLs to connect with views
urlpatterns = [
    path("", views.EntryListView.as_view(), name="entry-list"),
    path("entry/<int:pk>", views.EntryDetailView.as_view(), name="entry-detail"),
    path("create/", views.EntryCreateView.as_view(), name="entry-create"),
    path("stats/", views.entry_stats, name="entry-stats"),  # <-- new visualization URL
    path('signup/', views.signup_view, name='signup'),
    path("mood-chart/", views.mood_chart, name="mood_chart"),
    path('entry/<int:pk>/delete/', views.entry_delete, name='entry-delete'),
]
