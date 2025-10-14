from django.urls import path

from .views import (
    FAQListView,
    HelpArticleView,
    HelpCategoryView,
    HelpHomeView,
    HelpSearchView,
)


app_name = "help_system"

urlpatterns = [
    path('', HelpHomeView.as_view(), name='help_home'),
    path('search/', HelpSearchView.as_view(), name='search'),
    path('category/<slug:slug>/', HelpCategoryView.as_view(), name='category'),
    path('article/<slug:slug>/', HelpArticleView.as_view(), name='article'),
    path('faq/', FAQListView.as_view(), name='faq'),
]
