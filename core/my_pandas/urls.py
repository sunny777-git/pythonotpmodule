
from django.urls import path
from my_pandas import views
urlpatterns = [
    path('read_xls', views.read_data_from_xls,name="read_data_from_xls"),
    path('write_xls', views.write_data_into_xls,name="write_data_into_xls")
]
