from django.http import JsonResponse
from functools import wraps

def login_required_session(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        print("in decorator before if statememnt")
        # if not request.session.get('is_logged_in', False):
        if not ("is_logged_in" in request.session and request.session["is_logged_in"]):
            print("in decorator after inside if  statement")
            return JsonResponse({"status": "error", "message": "Authentication required."}, status=401)
        print("after if statement in decorator")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
