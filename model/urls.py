from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'teams', views.TeamViewSet)

app_name = 'model'
urlpatterns = [
    path('', include(router.urls)),
    path('get-teams/', views.get_teams),
    path('get-team/<int:id>/', views.get_team),
    path('predict-score/', views.predict_score),
    path('predict-match-winner/', views.predict_match_winner),
    path('train-score-model/', views.train_score_prediction_model),
    path('train-match-winner-model/', views.train_team_win_prediction_model),
    path('stats/<str:filter>/', views.get_stats),
]