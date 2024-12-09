from django.urls import path
from . import views

urlpatterns = [
    path('create-leave/',views.create_leave_request, name='create-leave'),
    path('detail-leave/',views.leave_request_detail, name='detail-leave'),
    path('update-leave/<int:id>/', views.update_leave_request, name='update_leave'),
    path('delete-leave/<int:id>/',views.delete_leave_request, name='delete-leave'),
    path('list-leave/',views.leave_request_list, name='list-leave'),
    path('get-leaves/', views.get_leave_requests, name='get_leave_requests'),
    path('approval/',views.approve_leave, name='approve_leave'),
    path('deny/', views.deny_leave, name='deny_leave'),
    path('get-leave-count/', views.get_leave_count, name='get_leave_count'),
    path('add-balance/', views.add_leave_balance, name='add-balance'),
    path('calculate-difference/', views.calculate_leave_differences,name='calculate-difference'),
    path('get-balance/', views.get_leave_balances, name='get-balance'),

]