from django.urls import path
from .views import get_starbucks_data

urlpatterns = [
    path('get-starbucks-data/', get_starbucks_data, name='get_starbucks_data'),
    # 다른 URL들을 여기에 추가할 수 있음
]
