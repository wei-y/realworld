from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, ListView, UpdateView

from realworld.apps.articles.models import Article

from .forms import User, SettingsForm, UserCreationForm


class ProfileView(ListView):
    context_object_name = "articles"
    template_name = "realworld/accounts/profile.html"

    def get_queryset(self):
        profile = get_object_or_404(User, pk=self.kwargs["pk"])
        articles = (
            Article.objects.select_related("author")
            .with_favorites(self.request.user)
            .prefetch_related("tags")
            .order_by("-created")
        )

        if "favorites" in self.request.GET:
            return articles.filter(is_favorite=True)

        return articles.filter(author=profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(User, pk=self.kwargs["pk"])
        context["profile"] = profile
        context["is_following"] = profile.followers.filter(
            pk=self.request.user.id
        ).exists()
        return context


class SettingView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = SettingsForm
    template_name = "realworld/accounts/settings.html"

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)


class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "registration/register.html"

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid


class ProfileFollowView(LoginRequiredMixin, UpdateView):
    fields = ["followers"]
    http_method_names = ["post"]

    def get_queryset(self, **kwargs):
        return User.objects.filter(pk=self.kwargs["pk"]).exclude(
            pk=self.request.user.id
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.followers.filter(id=request.user.id).exists():
            self.object.followers.remove(request.user)
        else:
            self.object.followers.add(request.user)

        return redirect(self.object.get_absolute_url())
