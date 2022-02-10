from django.urls import path

from . import views

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="home"),
    path("new/", views.create_article, name="create_article"),
    path(
        "article/<int:pk>/<slug:slug>/",
        views.ArticleDetailView.as_view(),
        name="article_detail",
    ),
    path(
        "article/edit/<int:article_id>/",
        views.edit_article,
        name="edit_article",
    ),
    path(
        "article/delete/<int:article_id>/",
        views.delete_article,
        name="delete_article",
    ),
    path(
        "article/favorite/<int:article_id>/",
        views.favorite,
        name="favorite",
    ),
]
