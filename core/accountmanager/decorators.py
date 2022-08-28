
from core.accountmanager.utils import AppResponse, get_user


def user_role(func):
    def process_request(request,**kwargs):
        user = get_user(request.META['HTTP_ACCESSTOKEN'])
        if user.is_user:
            return AppResponse(200,message="is a user")
        return func(request,**kwargs)
    return process_request
 
 
# def new_or_existing_user(func):
