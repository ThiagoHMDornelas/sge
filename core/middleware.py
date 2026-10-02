from threading import local

_user = local()


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = getattr(request, 'user', None)
        try:
            return self.get_response(request)
        finally:
            _user.value = None


def get_current_user():
    return getattr(_user, 'value', None)
