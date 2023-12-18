import logging

from backend.loggers import my_logger


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        my_logger.info(f"Path: {request.path}, Method: {request.method}, Body: {request.body}")

        response = self.get_response(request)

        my_logger.info(f"Response status: {response.status_code}, Body: {response.content}")
        return response
