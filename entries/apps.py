from django.apps import AppConfig

# Settings for the app. Handles IDs.
class EntriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'entries'
