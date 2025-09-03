from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from core.apps.resumes.models.user_role import UserRole
from .forms import CreateUserForm
from .decorators import role_required


@login_required
@role_required(["Администратор", "Root"])
def add_user(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            role = form.cleaned_data["role"]
            department = form.cleaned_data["department"]

            # создаём пользователя
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=True,
            )

            # назначаем роль
            UserRole.objects.create(
                user=user,
                role=role,
                department=department
            )


            # send_credentials(user, password)

            messages.success(request, f"Пользователь {username} успешно создан")
            return redirect("user_list")
    else:
        form = CreateUserForm()

    return render(request, "accounts/add_user.html", {"form": form})


@login_required
@role_required(["Администратор", "Root"])
def user_list(request):
    users = User.objects.all().select_related()
    return render(request, "accounts/user_list.html", {"users": users})