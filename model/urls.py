from django.urls import path
from . import views


app_name = 'model'
urlpatterns = [
    path('predict-score/', views.predict_score),
    path('predict-match-winner/', views.predict_match_winner),
    path('train-score-model/', views.train_score_prediction_model),
    path('train-match-winner-model/', views.train_team_win_prediction_model),
]