# chats/middleware.py
from datetime import datetime
import logging

# Configure the logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')  # Log file in project root
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response  # Django passes the next middleware/view

    def __call__(self, request):
        # Determine user
        if request.user.is_authenticated:
            user = request.user.email  # or request.user.username
        else:
            user = "Anonymous"

        # Log the request
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        # Call the next middleware or view
        response = self.get_response(request)
        return response
