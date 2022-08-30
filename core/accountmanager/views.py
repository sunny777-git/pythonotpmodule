
from django.shortcuts import render
import datetime
import os
import random
from django.contrib.auth import authenticate
from accountmanager.utils import AppResponse, OTP_Validity, access_token, get_geo_ip_location, get_user
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import decorator_from_middleware
from accountmanager.validators import validate_mobile, validate_user_otp, validate_user_role
from accountmanager.models import User, UserOTP, UserToken
from accountmanager.repository import filter_attribute, get_object, is_exists, store, update


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
       
        is_otp_exists = is_exists(UserOTP, {'mobile': data['mobile']})

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



@api_view(['POST'])
@csrf_exempt
def VerifyOTP(request):
    if request.method == "POST":
        data = request.data

        is_phone_validated = validate_mobile(data['mobile'])
        if is_phone_validated:
            data['mobile'] = '91'+data['mobile']
        else:
            return AppResponse(400,message='Please enter valid phone number')
        try:
            is_user_exists = is_exists(User, {'mobile': data['mobile']})
        except Exception as e:
            return AppResponse(200,message='User not found')
        if data:
            is_validated = validate_user_otp(data)
            if is_validated:
                otp_obj = get_object(UserOTP, {'mobile':data['mobile']})
                if otp_obj.otp == data['otp']:
                    is_otp_validated = OTP_Validity(data['mobile'],datetime.datetime.now())    
                          
                    '''For Existing Users ''' 
                    
                    if is_otp_validated and is_user_exists:
                        update(UserOTP, {'mobile':data['mobile']},{'is_otp_verified': True})
                        # update password with latest otp
                        update_user = get_object(User, {'mobile': data['mobile']})
                        update_user.set_password(data['otp'])
                        update_user.save()
                        token = access_token()

                        update(UserToken,{'user_id':update_user.id},{'access_token':token,'created_at':datetime.datetime.now()})
                        return AppResponse(200,access_token=token,message="OTP verified and logged successful")

                    # ''''''' For New Users '''''''''

                    elif is_otp_validated and not is_user_exists:
                        # get user current location details
                        user_location=get_geo_ip_location()
                       
                        create_user = store(
                            User, {
                            'mobile': data['mobile'],
                            'ip_address':user_location['ip'],
                            'city':user_location['city'],
                            'state':user_location['region'],
                            'country':user_location['country'],
                            'pincode':user_location['postal'],
                            'geo_locations':user_location['loc']})
                        create_user.set_password(data['otp'])
                        create_user.save()

                        #update otp status
                        update(UserOTP, {'mobile': data['mobile'], 'otp': data['otp']}, {'is_otp_verified': True})
                        token = access_token()
                        store(UserToken,{'user_id':create_user.id,'access_token':token,'created_at':datetime.datetime.now()})

                        return AppResponse(200,access_token=token,message='OTP verified,created account and logedin')
                    else:
                        return AppResponse(400,message='OTP has expired.Please generate new OTP')
                return AppResponse(400,message='Invalid otp or otp not provided')
            return AppResponse(400,message='Validation failed. Invalid OTP/Phone') 
        return AppResponse(400,message='Either otp or phone is incorrect')
    return AppResponse(400,message='Something went wrong.Please try again')


@api_view(['POST'])
@csrf_exempt
def set_UserPassword(request):
    data=request.data
    try:
        user = UserToken.objects.get(access_token=request.META['HTTP_ACCESSTOKEN']).user
    except Exception as e:
        return AppResponse(400,message="Invalid Token")
    try:
        if data['email']:
            is_user = get_object(User,{'id':user.id})
            if is_user:
                is_user.email=data['email']
                is_user.set_password(data['password'])
                is_user.save()
                return AppResponse(200,message="password has been set successfully")
    except Exception as e:
            return AppResponse(200,message="You can only change password for email")


@api_view(['POST'])
@csrf_exempt
def EmailLogin(request):
    data=request.data
    if not data['email']==None and not data['password']==None:
            is_user_exists = get_object(User,{'email':data['email']})
            if is_user_exists:
                is_authenticated = authenticate(username=data['email'],password=data['password'])
                print(is_authenticated)
                if is_authenticated:
                    return AppResponse(200,message="login successful") 
            return AppResponse(200,message="No such user exists ") 
    return AppResponse(200,message="Validation Error") 
               
                



    
