from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth views (login/logout)
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # User registration and other custom account views if any
    path('accounts/', include('entries.urls')),  # assuming signup is here

    # Your main app's URLs
    path('entries/', include('entries.urls')),

    # Redirect base URL to entries
    path('', RedirectView.as_view(url='/entries/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

