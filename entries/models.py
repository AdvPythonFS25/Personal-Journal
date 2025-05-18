from django.db import models # ← imports models module from django. Can manage tables and fields
from django.utils import timezone # ← django's timezone. Handles different timezones for users.
from taggit.managers import TaggableManager  # ← import taggit to handle tags being added
from ckeditor.fields import RichTextField  # ← import ckeditor because of formatting requirements
from django.contrib.auth.models import User


class Entry(models.Model): # ← uses django to allow the creation of entries in our journal
    title = models.CharField(max_length=200) # ← for entry titles, dates of creation, formatting
    content = RichTextField()  
    date_created = models.DateTimeField(default=timezone.now)
    sentiment_score = models.FloatField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # New fields:
    tags = TaggableManager(blank=True)   # ← allows comma-separated tags
    image = models.ImageField( # ← allows for images to be uploaded
        upload_to='entry_images/',
        blank=True,
        null=True
    )  # ← optional image upload
    link = models.URLField( # ← stores URLs
        blank=True
    )  # ← optional single link

    def __str__(self): # ← helps for admin page. Gives title when displaying entry
        return self.title #doesn't really work for titles with the same name, though

    class Meta:
        verbose_name_plural = "Entries"
