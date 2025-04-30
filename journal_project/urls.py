
from django.contrib import admin
from django.urls import path, include
#Handles global URLs
urlpatterns = [
    path('admin/', admin.site.urls),
    path("entries/", include("entries.urls")),
]
