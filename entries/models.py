# Import Django
from django.db import models
from django.utils import timezone

#  Makes a journal entry with a title, content, and timestamp, and customizes the admin display.

class Entry(models.Model):
    
    title = models.CharField(max_length=200)  
    content = models.TextField()  
    date_created = models.DateTimeField(default=timezone.now)  
    def __str__(self):
        return self.title  

    
    class Meta:
        verbose_name_plural = "Entries"  