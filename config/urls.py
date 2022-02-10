from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("realworld.apps.articles.urls")),
    path("", include("realworld.apps.accounts.urls")),
    path("comments/", include("realworld.apps.comments.urls")),
    path("admin/", admin.site.urls),
]
