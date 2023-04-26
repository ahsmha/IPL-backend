import pickle
import pandas as pd


MODEL_FILE_NAME = './static/models/ipl_match_win_predict_model.pkl'
TEAMS = ['Chennai Super Kings', 'Delhi Capitals', 'Gujarat Titans', 'Punjab Kings', 'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad', 'Lucknow Super Giants']


def get_match_winner(data):
    try:
        batting_team = data['batting_team']
        bowling_team = data['bowling_team']
        city = data['city']
        current_score = int(data['current_score'])
        balls_left = int(data['balls_left'])
        wickets = int(data['wickets'])
        target = int(data['target'])

        runs_left = target - current_score
        wickets_left = 10 - wickets
        if balls_left != 120:
            current_run_rate = (current_score * 6) / (120 - balls_left)
        else:
            current_run_rate = 0
        if balls_left:
            required_run_rate = (runs_left * 6) / balls_left
        else:
            required_run_rate = 0

        X_data = {
            'BattingTeam': batting_team,
            'BowlingTeam': bowling_team,
            'City': city,
            'runs_left': runs_left,
            'balls_left': balls_left,
            'wickets_left': wickets_left,
            'current_run_rate': current_run_rate,
            'required_run_rate': required_run_rate,
            'target': target
        }
        X_data = pd.DataFrame(data=X_data, index=[1])

        pipe = pickle.load(open(MODEL_FILE_NAME, 'rb'))
        result = pipe.predict(X_data)

        return batting_team if result[0] == 1 else bowling_team
    except Exception as ex:
        print('[ERROR][predict_match_winner.py:get_match_winner]: ', ex)
        raise ex