from django.urls import path
from users.views import RegisterView, ProfileUpdateView, UserSubscribeView, SubscriptionListView, ProfileDetailView
from users.apps import UsersConfig
from django.contrib.auth.views import LoginView, LogoutView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_update"),
    path("profile/<int:pk>", ProfileDetailView.as_view(), name="profile_view"),
    path("subscribe/<int:pk>/", UserSubscribeView.as_view(), name="subscribe"),
    path("subscriptions/", SubscriptionListView.as_view(), name="subscriptions_list"),
]
