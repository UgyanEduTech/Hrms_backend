from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_employees, name='employee_list'),
    path('get_employee/', views.employee_detail, name='employee_detail'),
    path('add_employee/', views.create_employee, name='employee_create'),
    path('update/', views.update_employee_byId, name='employee_update'),
    path('delete/', views.delete_employee_byId, name='employee_delete'),
    path('total_employees/', views.total_employees, name='total_employees'),
    path('new-joiners/', views.new_joiners, name='new_joiners'),
    path("verify-email/", views.verify_email_and_send_otp, name="verify-email"),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('change-password/', views.change_password, name='change_password'),
    path('login/', views.login, name='login'),
]
