from django.urls import path
from .views import index, get_all_starbucks_data, get_starbucks_data

urlpatterns = [
    path('', index),
    path('starbucks/all/', get_all_starbucks_data, name='get_all_starbucks_data'),
    path('starbucks/<str:field_name>/<str:field_value>/', get_starbucks_data, name='get_starbucks_data')
]
