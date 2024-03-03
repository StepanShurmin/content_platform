"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from content.views import HomePage, NoPermPage
from users.views import CreateCheckoutSession

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomePage.as_view(), name="home"),
    path("content/", include("content.urls", namespace="content")),
    path("user/", include("users.urls", namespace="user")),
    path("no_permission/", NoPermPage.as_view(), name="no_perm"),
    path(
        "create_checkout_session/<int:pk>/",
        CreateCheckoutSession.as_view(),
        name="create_checkout_session",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
