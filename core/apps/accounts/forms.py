from django import forms
from django.contrib.auth.models import User

from core.apps.resumes.models.department import Department
from core.apps.resumes.models.role import Role


class CreateUserForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Логин",
    )
    email = forms.EmailField(
        required=True,
        label="Email",
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Пароль',
    )
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        label="Роль",
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        label="Департамент",
    )

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Такой логин уже существует")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email