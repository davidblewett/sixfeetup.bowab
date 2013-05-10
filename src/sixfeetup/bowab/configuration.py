from functools import wraps

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.session import check_csrf_token


class CSRFValidationFailure(HTTPBadRequest):
    pass


def require_csrf(view):
    @wraps(view)
    def wrapped(context, request):
        if not check_csrf_token(request, raises=False):
            url = request.current_route_url()
            link = '<a href="%s">reloading the form</a>' % url
            msg = 'Invalid form token. Try %s and re-submitting.' % link
            raise CSRFValidationFailure(msg)
        return view(context, request)
    return wrapped
