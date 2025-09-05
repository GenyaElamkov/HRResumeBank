from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URL, которые не требуют авторизации
        exempt_urls = [
            reverse("authentication:login"),
            #
            # reverse("authentication:logout"),
            # "/admin/",
        ]

        if not request.user.is_authenticated and not any(
            request.path.startswith(url) for url in exempt_urls
        ):
            return redirect(f"{reverse('authentication:login')}?next={request.path}")

        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated:
                return redirect(f'{settings.LOGIN_URL}?next={request.path}')
            if not request.user.is_staff:
                return redirect('/')
        return None