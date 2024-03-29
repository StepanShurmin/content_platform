from django.urls import path
from content.apps import ContentConfig
from content.views import (
    PublicationCreateView,
    PublicationListView,
    PublicationUpdateView,
    PublicationDetailView,
    SetLikeView,
    SetDislikeView,
    SearchListView,
    PublicationDeleteView,
)

app_name = ContentConfig.name

urlpatterns = [
    path("create/", PublicationCreateView.as_view(), name="create_publication"),
    path("", PublicationListView.as_view(), name="list_publications"),
    path(
        "update/<int:pk>/", PublicationUpdateView.as_view(), name="update_publication"
    ),
    path("<int:pk>/", PublicationDetailView.as_view(), name="publication_detail"),
    path(
        "delete/<int:pk>/", PublicationDeleteView.as_view(), name="delete_publication"
    ),
    path("like/<int:pk>/", SetLikeView.as_view(), name="set_like"),
    path("dislike/<int:pk>/", SetDislikeView.as_view(), name="set_dislike"),
    path("search_results", SearchListView.as_view(), name="search"),
]
