from django.urls import path
from . import views

urlpatterns = [
    path('clock-in/', views.clock_in_view, name='clock_in'),
    path('clock-out/', views.clock_out_view, name='clock_out'),
    path('reset-attempts/', views.reset_login_attempts_view, name='reset_login_attempts'),
    path('timer/', views.timer_view, name='timer'),
    path('target/',views.track_monthly_targets,name='target'),
    path('add-target/',views.add_monthly_target,name='add-target'),
    path('update-target/',views.update_monthly_target,name='update-target'),
    path('reminders/', views.check_reminders_view, name='check_reminders_view'),
    path('reset_reminders/', views.reset_reminders_view, name='reset_reminders_view'),
    path('save_message/', views.save_message, name='save_message'),
    path('get_messages/', views.get_messages, name='get_messages'),
]
