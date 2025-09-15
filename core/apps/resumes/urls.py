from django.urls import path

from . import views
from .views import (
    CardListView,
    CartDetailView,
)


app_name = "resumes"

urlpatterns = [
    path("", CardListView.as_view(), name="card_list"),
    path("card/create/", views.create_card, name="create_card"),
    path("card/<int:card_id>/fill/", views.fill_card, name="fill_card"),
    path("card/<int:pk>/", CartDetailView.as_view(), name="card_detail"),
    path("cards/advanced_search/", views.advanced_search_cards, name="advanced_search_cards"),
]
