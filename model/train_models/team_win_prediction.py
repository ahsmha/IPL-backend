import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import pickle



def result(row):
            return 1 if row['BattingTeam'] == row['WinningTeam'] else 0

def model_1(balls_file_path='./static/data/dataset_3/IPL_Ball_by_Ball_2008_2022.csv', matches_file_path='./static/data/dataset_3//IPL_Matches_2008_2022.csv'):
    try:
        balls = pd.read_csv(balls_file_path)

        # Rename old names to new names
        balls['BattingTeam'] = balls['BattingTeam'].str.replace('Delhi Daredevils', 'Delhi Capitals')
        balls['BattingTeam'] = balls['BattingTeam'].str.replace('Kings XI Punjab', 'Punjab Kings')
        balls['BattingTeam'] = balls['BattingTeam'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
        balls['BattingTeam'] = balls['BattingTeam'].str.replace('Rising Pune Supergiants', 'Rising Pune Supergiant')

        matches = pd.read_csv(matches_file_path)

        # Rename the city where single city has different names present
        matches['City'] = matches['City'].str.replace('Bengaluru', 'Bangalore')

        # Rename old names to new names
        matches['Team1'] = matches['Team1'].str.replace('Delhi Daredevils', 'Delhi Capitals')
        matches['Team1'] = matches['Team1'].str.replace('Kings XI Punjab', 'Punjab Kings')
        matches['Team1'] = matches['Team1'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
        matches['Team1'] = matches['Team1'].str.replace('Rising Pune Supergiants', 'Rising Pune Supergiant')


        matches['Team2'] = matches['Team2'].str.replace('Delhi Daredevils', 'Delhi Capitals')
        matches['Team2'] = matches['Team2'].str.replace('Kings XI Punjab', 'Punjab Kings')
        matches['Team2'] = matches['Team2'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
        matches['Team2'] = matches['Team2'].str.replace('Rising Pune Supergiants', 'Rising Pune Supergiant')


        matches['TossWinner'] = matches['TossWinner'].str.replace('Delhi Daredevils', 'Delhi Capitals')
        matches['TossWinner'] = matches['TossWinner'].str.replace('Kings XI Punjab', 'Punjab Kings')
        matches['TossWinner'] = matches['TossWinner'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
        matches['TossWinner'] = matches['TossWinner'].str.replace('Rising Pune Supergiants', 'Rising Pune Supergiant')


        matches['WinningTeam'] = matches['WinningTeam'].str.replace('Delhi Daredevils', 'Delhi Capitals')
        matches['WinningTeam'] = matches['WinningTeam'].str.replace('Kings XI Punjab', 'Punjab Kings')
        matches['WinningTeam'] = matches['WinningTeam'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
        matches['WinningTeam'] = matches['WinningTeam'].str.replace('Rising Pune Supergiants', 'Rising Pune Supergiant')

        # Finding total score of the innings
        total_score = balls.groupby(['ID', 'innings']).sum()['total_run'].reset_index()

        # We only need score of 1st innings
        # Our target is winner prediction so we only need the score of first innings
        total_score = total_score[total_score['innings']==1]

        # Adding new feature to total_score
        total_score['target'] = total_score['total_run'] + 1

        # Merge total_score with the mathces dataset
        match_df = matches.merge(total_score[['ID','target']], on='ID')

        # Current teams in IPl
        current_teams = [
            'Rajasthan Royals',
            'Royal Challengers Bangalore',
            'Sunrisers Hyderabad', 
            'Delhi Capitals', 
            'Chennai Super Kings',
            'Gujarat Titans', 
            'Lucknow Super Giants', 
            'Kolkata Knight Riders',
            'Punjab Kings', 
            'Mumbai Indians'
        ]

        # Setting data of current teams only
        match_df = match_df[match_df['Team1'].isin(current_teams)]
        match_df = match_df[match_df['Team2'].isin(current_teams)]
        match_df = match_df[match_df['TossWinner'].isin(current_teams)]
        match_df = match_df[match_df['WinningTeam'].isin(current_teams)]

        # We want only the matches where D/L is not applied
        # Removing all matches effected due to rain
        match_df = match_df[match_df['method'].isna()]

        match_df = match_df[['ID','City','Team1','Team2','WinningTeam','target']].dropna()

        # Merge the match_df dataset with balls dataset
        balls_df = match_df.merge(balls, on='ID')

        # Only select rows where we are in 2nd innings
        balls_df = balls_df[balls_df['innings']==2]

        # Create new feature current_score after each ball
        balls_df['current_score'] = balls_df.groupby('ID')['total_run'].cumsum()

        # Adding other new feature
        balls_df['runs_left'] = np.where(balls_df['target']-balls_df['current_score']>=0, balls_df['target']-balls_df['current_score'], 0)
        balls_df['balls_left'] = np.where(120 - balls_df['overs']*6 - balls_df['ballnumber']>=0,120 - balls_df['overs']*6 - balls_df['ballnumber'], 0)
        balls_df['wickets_left'] = 10 - balls_df.groupby('ID')['isWicketDelivery'].cumsum()
        balls_df['current_run_rate'] = (balls_df['current_score']*6)/(120-balls_df['balls_left'])
        balls_df['required_run_rate'] = np.where(balls_df['balls_left']>0, balls_df['runs_left']*6/balls_df['balls_left'], 0)

        # Adding output variable result
        balls_df['result'] = balls_df.apply(result, axis=1)

        index1 = balls_df[balls_df['Team2']==balls_df['BattingTeam']]['Team1'].index
        index2 = balls_df[balls_df['Team1']==balls_df['BattingTeam']]['Team2'].index

        balls_df.loc[index1, 'BowlingTeam'] = balls_df.loc[index1, 'Team1']
        balls_df.loc[index2, 'BowlingTeam'] = balls_df.loc[index2, 'Team2'] 

        final_data = balls_df[['BattingTeam', 'BowlingTeam','City','runs_left','balls_left','wickets_left','current_run_rate','required_run_rate','target','result']]

        transformer = ColumnTransformer([('transformer', OneHotEncoder(sparse_output=False,drop='first'), ['BattingTeam','BowlingTeam','City'])], remainder = 'passthrough')

        X = final_data.drop('result', axis=1)
        y = final_data['result']

        # Split data into training data and testing data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=42)

        pipe = Pipeline(steps=[('step1', transformer), ('step2', RandomForestClassifier())])

        # Train the model
        pipe.fit(X_train, y_train)

        y_predictions = pipe.predict(X_test)

        accuracy = accuracy_score(y_predictions, y_test)
        print('Accuracy of the Model: >>>', accuracy)

        proba = pipe.predict_proba(X_test)

        # Saving the IPL Team Win Predictor Model
        file_name = './static/models/ipl_match_win_predict_model.pkl'
        pickle.dump(pipe, open(file_name,'wb'))

        return 'Model Trained Successfully'
    except Exception as ex:
        print('[Error][team_win_prediction.py:model_1]: ', ex)
        raise ex

