import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden


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

        return self.get_response(request)
