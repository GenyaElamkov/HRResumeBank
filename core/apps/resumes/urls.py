from django.urls import path

from .views import (
    AdvancedCardSearchView,
    CardCreateView,
    CardDetailView,
    CardListView,
    CardUpdateView,
    FileDeleteView,
    HomeScreenCardSearchView,
    ImageDeleteView,
)


app_name = "resumes"

urlpatterns = [
    path("", CardListView.as_view(), name="card_list"),
    path("card/create/", CardCreateView.as_view(), name="create_card"),
    path("card/<int:pk>/fill/", CardUpdateView.as_view(), name="update_card"),
    path("card/<int:pk>/", CardDetailView.as_view(), name="card_detail"),
    path("cards/advanced-search/", AdvancedCardSearchView.as_view(), name="advanced_search_cards"),
    path("cards/home-screen/", HomeScreenCardSearchView.as_view(), name="home_screen_search"),
    path("card/file/<int:pk>/delete/", FileDeleteView.as_view(), name="delete_file"),
    path("card/image/<int:pk>/delete/", ImageDeleteView.as_view(), name="delete_image"),
]
