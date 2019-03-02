from functools import wraps
from django.http import JsonResponse
from Helpers.utils import generate_exception_body

def respond(reponse):
    return JsonResponse(reponse, safe=False)

def get_or_none(Model, **kwargs):
    try:
        return Model.objects.get(**kwargs)
    except Exception as e:
        return None

# def role(roles_allowed):
# 	def decorator(func):
# 		@wraps(func)
# 		def role_check(request, *args, **kwargs):
# 			token = request.META.get('Authorisation')
# 			if get_role(token) not in roles_allowed:
# 				return respond(generate_exception_body("Insufficient Permissions", 403))
# 			else:
# 				return func(request, *args, **kwargs)
# 		return role_check
# 	return decorator