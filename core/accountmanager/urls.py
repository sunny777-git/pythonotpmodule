
from django.urls import path
from accountmanager import views
urlpatterns = [
    path('send_otp', views.Send_OTP,name="send_otp"),
    path('verify_otp', views.VerifyOTP,name="verify_otp"),
    path('setpassword', views.set_UserPassword,name="setpassword"),
    path('login', views.EmailLogin,name="login"),
    
]
