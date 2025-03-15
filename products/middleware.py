from django.utils import timezone
from django.contrib.sessions.models import Session
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class SessionExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
        # Skip this middleware for login/logout URLs
            if request.path in [reverse('login'), reverse('logout')]:
                return self.get_response(request)
                
            # Get the session key
            session_key = request.session.session_key
            
            try:
                # Get the session from the database
                session = Session.objects.get(session_key=session_key)
                
                # Check if the session has expired
                expiry_date = session.expire_date
                if expiry_date < timezone.now():
                    # Session expired, log out the user
                    request.session.flush()
                    return redirect(settings.LOGIN_URL + '?next=' + request.path)
                    
            except Session.DoesNotExist:
                # Session doesn't exist, continue with the request
                pass
                
        return self.get_response(request)