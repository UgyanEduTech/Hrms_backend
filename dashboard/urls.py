from django.urls import path
from . import views

urlpatterns = [
    path('clock-in/', views.clock_in_view, name='clock_in'),
    path('clock-out/', views.clock_out_view, name='clock_out'),
    path('reset-attempts/', views.reset_login_attempts_view, name='reset_login_attempts'),
    path('clock-in-out/', views.get_clock_in_out_data),
    path('timer/', views.timer_view, name='timer'),
    path('reminders/', views.check_reminders_view, name='check_reminders_view'),
    path('reset_reminders/', views.reset_reminders_view, name='reset_reminders_view'),
    path('save_message/', views.save_message, name='save_message'),
    path('get_messages/', views.get_messages, name='get_messages'),
    path("add-monthly-target/", views.add_monthly_target, name="add-monthly-target"),
    path('update-monthly-target/', views.update_monthly_target, name='update_monthly_target'),
    path("reset-monthly-targets/", views.reset_monthly_targets, name="reset-monthly-targets"),
    path('get-monthly-target/', views.get_monthly_target, name='get_monthly_target'),
]
