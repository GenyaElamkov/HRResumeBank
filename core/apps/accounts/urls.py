from django.urls import path

from .views import add_user, user_list


urlpatterns = [
    path('users/', user_list, name="user_list"),
    path('user/add/', add_user, name="add_user"),
]
