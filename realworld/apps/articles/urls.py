from django.urls import path

from .views import (ArticleCreateView, ArticleDetailView, ArticleDeleteView,
                    ArticleFavoriteView, ArticleListView, ArticleUpdateView)

urlpatterns = [
    path("", ArticleListView.as_view(), name="home"),
    path("new/", ArticleCreateView.as_view(), name="create_article"),
    path(
        "article/<int:pk>/<slug:slug>/",
        ArticleDetailView.as_view(),
        name="article_detail",
    ),
    path(
        "article/edit/<int:pk>/",
        ArticleUpdateView.as_view(),
        name="edit_article",
    ),
    path(
        "article/delete/<int:pk>/",
        ArticleDeleteView.as_view(),
        name="delete_article",
    ),
    path(
        "article/favorite/<int:pk>/",
        ArticleFavoriteView.as_view(),
        name="favorite",
    ),
]
