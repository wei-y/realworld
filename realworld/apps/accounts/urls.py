from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import ProfileFollowView, ProfileView, RegisterView, SettingView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("settings/", SettingView.as_view(), name="settings"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("profile/follow/<int:pk>/", ProfileFollowView.as_view(), name="follow"),
]
