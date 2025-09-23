from django.contrib.auth import views as auth_views
from django.urls import path


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
        'logout/', auth_views.LogoutView.as_view(
            template_name='authentication/logged_out.html',
        ), name='logout',
    ),
]
