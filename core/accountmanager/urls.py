
from django.urls import path
from accountmanager import views
urlpatterns = [
    path('send_otp', views.Send_OTP,name="send_otp"),
    path('verify_otp', views.VerifyOTP,name="verify_otp"),
    path('setpassword', views.EmailLogin,name="setpassword"),
    path('login', views.Email_Login,name="login"),
    
]
