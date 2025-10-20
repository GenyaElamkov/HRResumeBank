from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect


def logout_everywhere(request):
    """Выход из системы и удаление всех сессий пользователя."""
    user = request.user

    user_id_str = str(user.id)
    sessions_to_delete = []

    for session in Session.objects.all():
        session_data = session.get_decoded()
        if session_data.get('_auth_user_id') == user_id_str:
            sessions_to_delete.append(session.pk)

    Session.objects.filter(pk__in=sessions_to_delete).delete()

    logout(request)
    return HttpResponseRedirect('/')
