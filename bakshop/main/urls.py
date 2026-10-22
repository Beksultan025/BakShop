from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", views.register, name="register"),
    path("social/", include("allauth.urls")),
    path("after-login/", views.after_login, name="after_login"),
    path("", views.index, name="index"),
    path("after-login/", views.after_login, name="after_login"),
    path("panel/", views.panel_dashboard, name="panel_dashboard"),
    path("panel/products/", views.panel_list, name="panel_list"),
    path("panel/add/", views.panel_add, name="panel_add"),
    path("panel/<int:pk>/edit/", views.panel_edit, name="panel_edit"),
    path("panel/<int:pk>/delete/", views.panel_delete, name="panel_delete"),
    path("panel/analytics/", views.panel_analytics, name="panel_analytics"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)