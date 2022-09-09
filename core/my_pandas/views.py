from http.client import HTTPResponse
from django.shortcuts import render
import pandas as pd
from accountmanager.models import User
# Create your views here.
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django_pandas.io import read_frame

@api_view(['POST'])
@csrf_exempt
def read_data_from_xls(request):
    file=pd.ExcelFile('userlist.xlsx')
    df = pd.read_excel(file)
    print(df.head(1))
    #head(1) = head method accepts no.of rows.


@api_view(['POST'])
@csrf_exempt
def write_data_into_xls(request):
    qs = User.objects.all()
    df = read_frame(qs)
    df['created_at'] = pd.to_datetime(df['created_at'],errors='coerce').dt.date
    df['last_logout'] = pd.to_datetime(df['last_logout'],errors='coerce').dt.date
    # # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('userlist.xlsx')

    #  Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='userlist', index=False)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

#------------------------------------
#Series
# df.loc[2].at['Q']  - loc[2] => specific row id    at['Q'] => at specific column 

# DataFrame
# df.at[1,'Q'] - to get value from speific row & column
# df.at[1,'Q'] - to set value
# ------------------------------------
#Series
#df.loc[0].iat[1]  - loc[0]- 
