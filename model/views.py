from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from .serializers import TeamSerializer
from .models import Team
from .prediction_models.predict_score import get_score
from .prediction_models.predict_match_winner import get_match_winner
from .train_models import team_win_prediction
from .train_models import score_prediction
from .statistics.filters import Stats


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_teams(request):
    try:
        data = Team.objects.all()
        if data:
            serializer = TeamSerializer(data, many=True)
            response = {
                'statusCode': 200,
                'isSuccess': True,
                'data': serializer.data
            }
        else: raise Exception('No teams found!')
    except Exception as ex:
        print('[ERROR][views.py:get_teams]: ', ex)
        response = {
            'statusCode': 400,
            'isSuccess': False,
            'error': ex.args
        }
    finally: return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_team(request, id):
    try:
        data = Team.objects.get(pk=id)
        if data:
            serializer = TeamSerializer(data)
            response = {
                'statusCode': 200,
                'isSuccess': True,
                'data': serializer.data
            }
        else: raise Exception(f'Team with id {id} not found!')
    except Exception as ex:
        print('[ERROR][views.py:get_team]: ', ex)
        response = {
            'statusCode': 400,
            'isSuccess': False,
            'error': ex.args
        }
    finally: return Response(response, status=status.HTTP_200_OK)


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


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_stats(request, filter):
    try:
        season, team = request.GET.get('season', 'alltime'), request.GET.get('team', 'allteams')
        stats = Stats()
        if filter == 'most-fours':
            result = stats.get_most_fours_by_season(season=season, team=team)
        elif filter == 'most-fours-innings':
            result = stats.get_most_fours_by_inning(season=season, team=team)
        elif filter == 'most-sixes':
            result = stats.get_most_sixes_by_season(season=season, team=team)
        elif filter == 'most-sixes-innings':
            result = stats.get_most_sixes_by_inning(season=season, team=team)
        elif filter == 'most-fifties':
            result = stats.get_most_fifties(season=season, team=team)
        elif filter == 'most-centuries':
            result = stats.get_most_centuries(season=season, team=team)
        else:
            raise Exception('Bad Request')
            
        response = {
            'statusCode': 200,
            'isSuccess': True,
            'data': result
        }
    except Exception as ex:
        print('[ERROR][views.py:get_stats]: ', ex)
        response = {
            'statusCode': 400,
            'isSuccess': False,
            'error': ex.args
        }
    finally: return Response(response, status=status.HTTP_200_OK)