
from django.urls import path
from accountmanager import views
urlpatterns = [
    path('send_otp', views.Send_OTP,name="send_otp"),
    # path('verify_otp/', views.Verify_OTP,name="verify_otp"),
]
