import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn import metrics
import pickle


def overs(row):
    over = str(row['over'])
    ball = str(row['ballnumber'])
    overs = over + '.' + ball if int(ball) < 6 else int(over) + 1
    return float(overs)

# Helper function for calculating runs in last 5 overs
def runs_rolling_sum_(df):
    df['runs_in_prev_5'] = df['total_run'].rolling(window=30).sum()
    return df

# Helper function for calculating wickets in last 5 overs
def wickets_rolling_sum_(df):
    df['wickets_in_prev_5'] = df['isWicketDelivery'].rolling(window=30).sum()
    return df

def decimal_to_int_for_runs(row):
    return int(row['runs_in_prev_5'])
    
def decimal_to_int_for_wickets(row):
    return int(row['wickets_in_prev_5'])


def model_1(balls_file_path='./static/data/dataset_3/IPL_Ball_by_Ball_2008_2022.csv', matches_file_path='./static/data/dataset_3//IPL_Matches_2008_2022.csv'):
    try:
        data = pd.read_csv(balls_file_path)

        # Rename overs to over
        data = data.rename(columns={'overs': 'over'})

        # Add new feature overs in place of over and ballnumber
        data['overs'] = data.apply(overs, axis=1)

        # Add new feature current_score
        data['current_score'] = data.groupby(['ID', 'innings'])['total_run'].cumsum()

        # Add new feature wickets
        data['wickets'] = data.groupby(['ID', 'innings'])['isWicketDelivery'].cumsum()  

        # Add new feature runs_in_prev_5
        data = data.groupby(['ID', 'innings']).apply(runs_rolling_sum_)
        data = data.reset_index(drop=True)

        # Add new feature wickets_in_prev_5
        data = data.groupby(['ID', 'innings']).apply(wickets_rolling_sum_)
        data = data.reset_index(drop=True)

        # Now filter the data based on 5 overs, we have to keep data of after 5 overs
        data = data[data['over'] >= 5]


        # Since values of runs_in_prev_5 and wickets_in_prev_5 are in decimal, we have to make these values to integer
        data['runs_in_prev_5'] = data.apply(decimal_to_int_for_runs, axis=1)
        data['wickets_in_prev_5'] = data.apply(decimal_to_int_for_wickets, axis=1)

        # Finding total score of the innings
        total_score = data.groupby(['ID', 'innings']).sum()['total_run'].reset_index()
        
        # Rename the total_run feature to total_score
        total_score = total_score.rename(columns={'total_run': 'total_score'})

        # Add new feature total_score
        data = data.merge(total_score[['ID', 'innings', 'total_score']], on=['ID', 'innings'])

        matches = pd.read_csv(matches_file_path)
        data = data.merge(matches[['ID', 'Team1', 'Team2']], on='ID')

        index1 = data[data['Team2'] == data['BattingTeam']]['Team1'].index
        index2 = data[data['Team1'] == data['BattingTeam']]['Team2'].index

        data.loc[index1, 'BowlingTeam'] = data.loc[index1, 'Team1']
        data.loc[index2, 'BowlingTeam'] = data.loc[index2, 'Team2']

        # Rename old team names to new names
        data['BattingTeam'] = data['BattingTeam'].str.replace('Delhi Daredevils', 'Delhi Capitals')
        data['BattingTeam'] = data['BattingTeam'].str.replace('Kings XI Punjab', 'Punjab Kings')
        data['BattingTeam'] = data['BattingTeam'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
        data['BattingTeam'] = data['BattingTeam'].str.replace('Rising Pune Supergiants', 'Rising Pune Supergiant')

        data['BowlingTeam'] = data['BowlingTeam'].str.replace('Delhi Daredevils', 'Delhi Capitals')
        data['BowlingTeam'] = data['BowlingTeam'].str.replace('Kings XI Punjab', 'Punjab Kings')
        data['BowlingTeam'] = data['BowlingTeam'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
        data['BowlingTeam'] = data['BowlingTeam'].str.replace('Rising Pune Supergiants', 'Rising Pune Supergiant')

        # Current teams in IPl
        current_teams = [ 'Rajasthan Royals',
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

        # Keep data only of current teams in ipl
        data = data[data['BattingTeam'].isin(current_teams)]
        data = data[data['BowlingTeam'].isin(current_teams)]

        # Important Features
        features_to_set = ['BattingTeam', 'BowlingTeam', 'overs', 'current_score', 'total_score', 'wickets', 'runs_in_prev_5', 'wickets_in_prev_5']
        final_data = data[features_to_set]

        transformer = ColumnTransformer([('transformer', OneHotEncoder(sparse_output=False,drop='first'), ['BattingTeam','BowlingTeam'])], remainder = 'passthrough')

        X = final_data.drop('total_score', axis=1)
        y = final_data['total_score']

        # Split data into training data and testing data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=42)

        pipe = Pipeline(steps=[('step1',transformer), ('step2',RandomForestRegressor())])

        # Train the model
        pipe.fit(X_train, y_train)

        # make predictions
        y_predictions = pipe.predict(X_test)

        # Using Evaluation Metrics
        # Mean Absolute Error
        print('MAE: ', metrics.mean_absolute_error(y_test , y_predictions))

        # Mean Squared Error
        print('MSE: ', metrics.mean_squared_error(y_test, y_predictions))

        # Root Mean Squared Error
        print('RMSE: ', np.sqrt(metrics.mean_squared_error(y_test, y_predictions)))

        # Saving the IPL Score Predictor Model
        file_name = './static/models/ipl_score_predict_model.pkl'
        pickle.dump(pipe , open(file_name,'wb'))

        return 'Model Trained Successfully'
    except Exception as ex:
        print('[Error][score_prediction.py:model_1]: ', ex)
        raise ex