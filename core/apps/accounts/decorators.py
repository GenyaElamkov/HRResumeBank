from functools import wraps
from django.http import HttpResponseForbidden


def role_required(roles: list[str]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Требуется вход в систему")
            # связь User -> UserRole: related_name "users" в твоей модели
            user_roles = set(
                request.user.users.values_list("role__title", flat=True)
            )
            if not user_roles.intersection(set(roles)):
                return HttpResponseForbidden("Недостаточно прав")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
