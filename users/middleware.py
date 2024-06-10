# middleware.py
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin

class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return
        try:
            last_activity = request.session['last_activity']
            if datetime.now() - last_activity > timedelta(minutes=5):
                logout(request)
        except KeyError:
            pass
        request.session['last_activity'] = datetime.now()
