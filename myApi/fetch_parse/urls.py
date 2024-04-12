from django.urls import path
from .views import fetch_and_save_starbucks_data, get_all_starbucks_data, get_starbucks_data

urlpatterns = [
    path('get-starbucks-data/', fetch_and_save_starbucks_data,),
    path('/starbucks/all', get_all_starbucks_data,),
    path('starbucks/<str:field_name>/<str:field_value>/', get_starbucks_data),
]
