from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView

from taggit.models import Tag

from realworld.apps.comments.forms import CommentForm
from realworld.apps.comments.models import Comment

from .forms import ArticleForm
from .models import Article


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


@require_http_methods(["GET", "POST"])
@login_required
def create_article(request: HttpRequest) -> HttpResponse:

    if request.method == "GET":
        return TemplateResponse(
            request,
            "realworld/articles/article_form.html",
            {"form": ArticleForm()},
        )

    if (form := ArticleForm(request.POST)).is_valid():

        article = form.save(commit=False)
        article.author = request.user
        article.save()

        # save tags
        form.save_m2m()

        return HttpResponseRedirect(article.get_absolute_url())

    return TemplateResponse(request, "realworld/articles/partials/article_form.html", {"form": form})


@require_http_methods(["GET", "POST"])
@login_required
def edit_article(request: HttpRequest, article_id: int) -> HttpResponse:

    article = get_object_or_404(Article, pk=article_id, author=request.user)

    if request.method == "GET":

        return TemplateResponse(
            request,
            "realworld/articles/article_form.html",
            {
                "form": ArticleForm(instance=article),
                "article": article,
            },
        )

    if (form := ArticleForm(request.POST, instance=article)).is_valid():
        form.save()
        return HttpResponseRedirect(article.get_absolute_url())

    return TemplateResponse(
        request,
        "realworld/articles/partials/article_form.html",
        {
            "form": form,
            "article": article,
        },
    )


@require_http_methods(["DELETE"])
@login_required
def delete_article(request: HttpRequest, article_id: int) -> HttpResponse:

    article = get_object_or_404(Article, pk=article_id, author=request.user)
    article.delete()
    return HttpResponseRedirect(reverse("home"))


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


@require_http_methods(["GET"])
def tags_autocomplete(request: HttpRequest) -> HttpResponse:

    # find the latest item in tag string

    search: str = ""

    try:
        search = request.GET["tags"].split()[-1].strip()
    except (KeyError, IndexError):
        pass

    tags = (
        Tag.objects.filter(name__istartswith=search).distinct()
        if search
        else Tag.objects.none()
    )

    return TemplateResponse(request, "realworld/articles/partials/tags.html", {"tags": tags})
