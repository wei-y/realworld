from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from taggit.models import Tag

from realworld.core.mixins import AuthorRequiredMixin
from realworld.apps.comments.forms import Comment, CommentForm

from .forms import Article, ArticleForm


class ArticleListView(ListView):
    model = Article
    context_object_name = "articles"
    template_name = "realworld/articles/article_list.html"

    def get_queryset(self):
        queryset = (super().get_queryset()
                    .select_related("author")
                    .with_favorites(self.request.user)
                    .prefetch_related("tags")
                    .order_by("-created"))

        if tag := self.request.GET.get("tag"):
            return queryset.filter(tags__name__in=[tag])

        if self.request.user.is_authenticated and "own" in self.request.GET:
            return queryset.filter(author=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = "article"
    template_name = "realworld/articles/article_detail.html"

    def get_queryset(self):
        queryset = (super().get_queryset()
                    .select_related("author")
                    .with_favorites(self.request.user))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = (Comment.objects.filter(article=self.kwargs['pk'])
                               .select_related("author")
                               .order_by("-created"))

        if self.request.user.is_authenticated:
            context.update(
                {
                    "comment_form": CommentForm(),
                }
            )
        return context


class ArticleCreateView(AuthorRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'realworld/articles/article_form.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()

        # save tags
        form.save_m2m()

        return super().form_valid(form)


class ArticleUpdateView(AuthorRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'realworld/articles/article_form.html'


class ArticleDeleteView(AuthorRequiredMixin, DeleteView):
    model = Article
    success_url = '/'


@require_http_methods(["POST", "DELETE"])
@login_required
def favorite(request: HttpRequest, article_id: int) -> HttpResponse:

    article = get_object_or_404(
        Article.objects.select_related("author").exclude(author=request.user),
        pk=article_id,
    )

    is_favorite: bool

    if request.method == "DELETE":
        article.favorites.remove(request.user)
        is_favorite = False
    else:
        article.favorites.add(request.user)
        is_favorite = True

    return TemplateResponse(
        request,
        "realworld/articles/partials/favorite_action.html",
        {
            "article": article,
            "is_favorite": is_favorite,
            "num_favorites": article.favorites.count(),
            "is_action": True,
            "is_detail": False
            if request.htmx.target == f"favorite-{article.id}"
            else True,
        },
    )
