from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from .prediction_models.predict_score import get_score
from .prediction_models.predict_match_winner import get_match_winner
from .train_models import team_win_prediction
from .train_models import score_prediction


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def predict_score(request):
    try:
        data = request.data
        score = get_score(data)
        response = {
            'statusCode': 200,
            'isSuccess': True,
            'data': score
        }
    except Exception as ex:
        print('[ERROR][views.py:predict_score]: ', ex)
        response = {
            'statusCode': 400,
            'isSuccess': False,
            'error': ex.args
        }
    finally: return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def predict_match_winner(request):
    try:
        data = request.data
        winner = get_match_winner(data)
        response = {
            'statusCode': 200,
            'isSuccess': True,
            'data': winner
        }
    except Exception as ex:
        print('[ERROR][views.py:predict_match_winner]: ', ex)
        response = {
            'statusCode': 400,
            'isSuccess': False,
            'error': ex.args
        }
    finally: return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def train_team_win_prediction_model(request):
    try:
        result = team_win_prediction.model_1()
        response = {
            'statusCode': 200,
            'isSuccess': True,
            'data': result
        }
    except Exception as ex:
        print('[ERROR][views.py:train_team_win_prediction_model]: ', ex)
        response = {
            'statusCode': 400,
            'isSuccess': False,
            'error': ex.args
        }
    finally: return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def train_score_prediction_model(request):
    try:
        result = score_prediction.model_1()
        response = {
            'statusCode': 200,
            'isSuccess': True,
            'data': result
        }
    except Exception as ex:
        print('[ERROR][views.py:train_score_prediction_model]: ', ex)
        response = {
            'statusCode': 400,
            'isSuccess': False,
            'error': ex.args
        }
    finally: return Response(response, status=status.HTTP_200_OK)
