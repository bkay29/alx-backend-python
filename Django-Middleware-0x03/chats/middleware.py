import logging
from datetime import datetime, time
from django.http import JsonResponse


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger("request_logger")

        # Create file handler
        file_handler = logging.FileHandler("requests.log")
        formatter = logging.Formatter("%(message)s")
        file_handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(file_handler)

        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        self.logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access outside 6PM–9PM.
    Returns 403 Forbidden when outside allowed hours.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()

        # Allowed access ONLY between 18:00 (6PM) and 21:00 (9PM)
        start_allowed = time(18, 0)
        end_allowed = time(21, 0)

        if not (start_allowed <= now <= end_allowed):
            return HttpResponseForbidden("Access to the chat is restricted during this time.")


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_requests = {}  # { "ip": [timestamps] }
        self.limit = 5
        self.window_seconds = 60  # 1 minute window

    def __call__(self, request):
        # Only limit POST requests (messages)
        if request.method == "POST":
            ip = request.META.get("REMOTE_ADDR", "unknown")
            now = datetime.now()

            # Initialize list if no record exists
            if ip not in self.ip_requests:
                self.ip_requests[ip] = []

            # Remove messages outside the 1-minute window
            self.ip_requests[ip] = [
                ts for ts in self.ip_requests[ip]
                if now - ts < timedelta(seconds=self.window_seconds)
            ]

            # Check block condition
            if len(self.ip_requests[ip]) >= self.limit:
                return JsonResponse(
                    {"error": "Rate limit exceeded. Try again later."},
                    status=429
                )

            # Add current request timestamp
            self.ip_requests[ip].append(now)


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow safe methods such as GET, HEAD, OPTIONS
        # Only restrict actions that require admin/moderator
        protected_paths = [
            "/admin-actions/",
            "/moderate/",
            "/delete-message/",
            "/manage-users/",
        ]

        # Only apply check if user is hitting protected paths
        if any(request.path.startswith(p) for p in protected_paths):
            user = request.user

            # If user not authenticated OR does not have required role
            # (Assuming user.role exists OR using is_staff / is_superuser fallback)
            if not user.is_authenticated:
                return JsonResponse(
                    {"error": "Authentication required"},
                    status=403
                )

            # Check role – modify based on your model structure
            user_role = getattr(user, "role", None)

            # Allowed: admin or moderator
            allowed_roles = ["admin", "moderator"]

            # Fallback: allow Django admins
            if user_role not in allowed_roles and not user.is_staff and not user.is_superuser:
                return JsonResponse(
                    {"error": "Forbidden: insufficient permissions"},
                    status=403
                )


        return self.get_response(request)
