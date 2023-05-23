from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'teams', views.TeamViewSet)

app_name = 'stats'
urlpatterns = [
    path('', include(router.urls)),
    path('get-teams/', views.get_teams),
    path('get-team/<int:id>/', views.get_team),
    path('stats/<str:filter>/', views.get_stats),
]