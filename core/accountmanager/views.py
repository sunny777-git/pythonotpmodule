
from django.shortcuts import render
import datetime
import os
import random
from django.contrib.auth import authenticate
from accountmanager.utils import AppResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import decorator_from_middleware
from accountmanager.validators import validate_mobile, validate_user_role
from accountmanager.models import User, UserOTP
from accountmanager.repository import get_object, is_exists, store, update


@api_view(['POST'])
@csrf_exempt
def Send_OTP(request):
    if request.method == 'POST':
        data = request.data
        is_mobile_validated = validate_mobile(data['mobile'])

        if is_mobile_validated:
            data['mobile'] = '91'+data['mobile']
        else:
            return AppResponse('Please enter valid mobile number',status=400)

        is_user = validate_user_role(data['mobile'])

        is_user_exists = is_exists(User, {'mobile': data['mobile']})
        print(is_user_exists,"is_user_exists")
        is_otp_exists = is_exists(UserOTP, {'mobile': data['mobile']})
        print(is_otp_exists,"is_otp_exists")
        data['otp'] = str(random.randint(100000, 999999))

        # For signup users
        if not is_user_exists and not is_otp_exists:
            store_user_otp = store(UserOTP,{
            'mobile':data['mobile'],
            'otp': data['otp'],
            'created_at':datetime.datetime.now(),
            'expires_at':datetime.datetime.now() + datetime.timedelta(minutes=2),
            'is_otp_verified': False})
          
            serialized_data = get_object(UserOTP,{'mobile':data['mobile']})
            return AppResponse(200,serialized_data,"New OTP generated")
            

        # "Login - already registered user"
        elif is_user_exists and is_otp_exists:
            update_user=UserOTP.objects.filter(mobile=data['mobile']).update(otp= data['otp'],created_at= datetime.datetime.now(),expires_at= datetime.datetime.now() + datetime.timedelta(minutes=2),is_otp_verified=False)
           
            if update_user:
                serialized_data = get_object(UserOTP,{'mobile':data['mobile']})
                return AppResponse(200,serialized_data,"New OTP generated")

        elif is_user_exists and not is_otp_exists:
            store_user_otp = store(UserOTP, {'mobile':data['mobile'],'otp': data['otp'],'created_at':datetime.datetime.now(),'expires_at':datetime.datetime.now() + datetime.timedelta(minutes=2),'is_otp_verified': False})
          
            if store_user_otp:
                serialized_data = get_object(UserOTP,{'mobile':data['mobile']})
                return AppResponse(200,serialized_data,"New OTP generated")

        # cond 3: "not a registered user" but already has otp and trying to send again
        else:
            store_user_otp = update(UserOTP, {'mobile':data['mobile']},{'otp': data['otp'],'created_at':datetime.datetime.now(),'expires_at':datetime.datetime.now() + datetime.timedelta(minutes=2),'is_otp_verified': False})
            serialized_data = get_object(UserOTP,{'mobile':data['mobile']})
            return AppResponse(200,serialized_data,"New OTP generated")

    return AppResponse(400,"something went wrong")


