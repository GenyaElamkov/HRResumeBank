from django.urls import path

from . import views
from .views import (
    CardCreateView,
    CardDetailView,
    CardListView,
    CardUpdateView,
)


app_name = "resumes"

urlpatterns = [
    path("", CardListView.as_view(), name="card_list"),
    path("card/create/", CardCreateView.as_view(), name="create_card"),
    path("card/<int:pk>/fill/", CardUpdateView.as_view(), name="fill_card"),
    path("card/<int:pk>/", CardDetailView.as_view(), name="card_detail"),
    path("cards/advanced_search/", views.advanced_search_cards, name="advanced_search_cards"),
]
