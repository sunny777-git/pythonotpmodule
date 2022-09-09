
'''
check the OTP whether it is expired or alive
'''
from distutils.log import ERROR
import json
from logging import exception
from sre_constants import SUCCESS
from urllib.request import urlopen

from accountmanager.models import UserOTP, UserToken

from .repository import get_object
from django.http import JsonResponse

""" To hash the access-token"""
def access_token():
    import secrets
    password_length = 13
    token = secrets.token_urlsafe(password_length)
    return token

def get_user(accesstoken):
    user=get_object(UserToken,{'access_token':accesstoken})
    
    return user

def OTP_Validity(mobile,currentdatetime):
    otp_obj = get_object(UserOTP,{'mobile':mobile})
    if otp_obj:
        split_sent_time = str(currentdatetime.strftime("%H:%M:%S")).split(':')
        send_time_in_minutes = int(split_sent_time[0])*60 + int(split_sent_time[1])
        split_expiry_time = str(otp_obj.expires_at.strftime("%H:%M:%S")).split(':')
        expiry_time_in_minutes= int(split_expiry_time[0])*60 + int(split_expiry_time[1])
        isExpired = send_time_in_minutes > expiry_time_in_minutes # 826 > 811
        
        if isExpired:
            return False
        else:
            return True
    else:
        return None

""" To get ip location"""
def get_geo_ip_location():
	url = 'http://ipinfo.io/json'
	response = urlopen(url)
	return json.load(response)
    

def AppResponse(code,data=None,message=None,access_token=None):
    from django.forms.models import model_to_dict
    try:
        data =model_to_dict(data)
    except Exception as e:
        data=""
    status_message= "Success" if code==200 else "Error"
    return JsonResponse({"code": code,"message":message,"status":status_message,"data":data,"access_token":str(access_token)})


# def FilterResponse(code,data=None,message=None,access_token=None):
#     from django.core.serializers.json import DjangoJSONEncoder
#     try:

#         data =json.dumps(list(data), cls=DjangoJSONEncoder)
#     except exception as e:
#         data=""
#     status_message= "Success" if code==200 else "Error"
#     return JsonResponse({"code": code,"message":message,"status":status_message,"data":data})