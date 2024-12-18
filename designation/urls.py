from django.urls import path
from .views import *

urlpatterns = [
    path('add/', add_designation, name='add_designation'),
    path('delete_designation/', delete_designation, name='delete_designation'),
    path("floormanager/", get_floormanagers, name="get_floormanagers"),
    path("verticalmanagers-by-id/", get_vertical_managers_byId, name="get_vertical_managers"),
    path('teamleaders-by-id/', get_team_leaders_byId, name='get_team_leaders'),
    path("verticalmanager/", get_verticalmanagers, name="get_floormanagers"),
    path('teamleaders/', get_team_lead, name='get_team_leaders'),
    path('atl-by-id/', get_Atl_byId, name='get_team_leaders'),
    path('atls/', get_Atls, name='get_team_leaders'),
    path('bda-by-id/', get_bda_byId, name='get_team_leaders'),
    path('ceo/', get_ceo, name='get_team_leaders'),
    path('cto/', get_cto, name='get_team_leaders'),
    path('coo/', get_coo, name='get_team_leaders'),
    path('cfo/', get_cfo, name='get_team_leaders'),
    path('bda/', get_BDA, name='get_team_leaders'),



]
