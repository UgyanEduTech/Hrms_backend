# urls.py
from django.urls import path
from .views import get_holidays, add_holiday, delete_holiday

urlpatterns = [
    path('holidays/', get_holidays, name='get_holidays'),
    path('holidays/add/', add_holiday, name='add_holiday'), 
    path('holidays/delete/<int:holiday_id>/',delete_holiday, name='delete_holiday')# Add this line for the POST method
]
