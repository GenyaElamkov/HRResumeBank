from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path('logout/', login_required(auth_views.LogoutView.as_view(next_page="login")), name="logout"),
]
