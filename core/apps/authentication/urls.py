from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = "authentication"

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            redirect_authenticated_user=True,
            template_name='authentication/login.html',
        ),
        name='login',
    ),
    path(
        'logout/', views.logout_everywhere, name='logout',
    ),
    path(
        'locked/',
        TemplateView.as_view(template_name='authentication/locked.html'),
        name='locked',
    ),
]
