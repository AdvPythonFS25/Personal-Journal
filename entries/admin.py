from django.contrib import admin
from .models import Entry

# Allows for edit, delete and add in the admin page
admin.site.register(Entry)
