
from django.contrib import admin
from django.urls import path, include

# Import these two so Django can serve media files in dev
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('entries/', include('entries.urls')),
]

# This bit tells Django to serve files under MEDIA_URL from MEDIA_ROOT
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
