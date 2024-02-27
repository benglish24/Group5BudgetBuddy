from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path("admin/", admin.site.urls),
    path("accounts/", include("users.urls")),
    path("accounts/", include("user_profile.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("logout/", auth_views.LogoutView.as_view(), name='logout'),  # Add this line for logout
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
