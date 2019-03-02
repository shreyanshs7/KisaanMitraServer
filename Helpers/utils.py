from django.http import JsonResponse
from django.contrib.auth.models import User
from functools import wraps

def generate_exception_body(message, status_code):
    body = {}
    body['success'] = False
    if message is not None:
        body['message'] = message
    if status_code is not None:
        body['status_code'] = status_code
    return body

def assert_check(condition, message = None, status_code = None):
    if condition is False:
        exception = generate_exception_body(message, status_code)
        return Exception(exception)

def assert_true(condition, message = "Forbidden", status_code = 403):
    assert_check(condition, message, status_code)

def assert_found(instance, message = "Not Found", status_code = 404):
    if instance is None:
        assert_check(False, message, status_code)

def assert_valid(condition, message = "Bad Request", status_code = 400):
    assert_check(condition, message, status_code)

