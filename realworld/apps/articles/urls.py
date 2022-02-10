from django.urls import path

from . import views

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="home"),
    path("new/", views.ArticleCreateView.as_view(), name="create_article"),
    path(
        "article/<int:pk>/<slug:slug>/",
        views.ArticleDetailView.as_view(),
        name="article_detail",
    ),
    path(
        "article/edit/<int:pk>/",
        views.ArticleUpdateView.as_view(),
        name="edit_article",
    ),
    path(
        "article/delete/<int:pk>/",
        views.ArticleDeleteView.as_view(),
        name="delete_article",
    ),
    path(
        "article/favorite/<int:article_id>/",
        views.favorite,
        name="favorite",
    ),
]
