import pickle
import pandas as pd


MODEL_FILE_NAME = './static/models/ipl_score_predict_model.pkl'
TEAMS = ['Chennai Super Kings', 'Delhi Capitals', 'Punjab Kings', 'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad']

def get_score(data):
    try:
        batting_team = data['batting_team']
        bowling_team = data['bowling_team']
        overs = float(data['overs'])
        current_score = int(data['current_score'])
        runs_in_prev_5 = int(data['runs_in_prev_5'])
        wickets_in_prev_5 = int(data['wickets_in_prev_5'])
        wickets = int(data['wickets'])

        X_data = {
            'BattingTeam': batting_team,
            'BowlingTeam': bowling_team,
            'overs': overs,
            'current_score': current_score,
            'runs_in_prev_5': runs_in_prev_5,
            'wickets_in_prev_5': wickets_in_prev_5,
            'wickets': wickets
        }
        X_data = pd.DataFrame(data=X_data, index=[1])

        pipe = pickle.load(open(MODEL_FILE_NAME, 'rb'))
        result = pipe.predict(X_data)
        result = int(result[0])

        return result
    except Exception as ex:
        print('[ERROR][predict_score.py:get_score]: ', ex)
        raise ex