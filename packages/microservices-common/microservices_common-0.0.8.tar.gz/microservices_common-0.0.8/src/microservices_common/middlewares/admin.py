from flask import request
from functools import wraps
from util.util import Util


def admin(handler):
    @wraps(handler)
    def authorize_admin(*args, **kwargs):
        if Util.is_admin(request=request):
            return handler(*args, **kwargs)

        return dict(message='FORBIDDEN'), 403

    return authorize_admin
