import pandas as pd


def get_matches_data(path='./static/data/dataset_1/IPL Matches 2008-2020.csv'):
    data = pd.read_csv(path)
    # As there old names of some teams, changing the old name to the newer one.
    # for Delhi Capitals
    data['team1']=data['team1'].str.replace('Delhi Daredevils','Delhi Capitals')
    data['team2']=data['team2'].str.replace('Delhi Daredevils','Delhi Capitals')
    data['winner']=data['winner'].str.replace('Delhi Daredevils','Delhi Capitals')
    # for sunrisers Hyderabad
    data['team1']=data['team1'].str.replace('Deccan Chargers','Sunrisers Hyderabad')
    data['team2']=data['team2'].str.replace('Deccan Chargers','Sunrisers Hyderabad')
    data['winner']=data['winner'].str.replace('Deccan Chargers','Sunrisers Hyderabad')

    return data


def get_teams(path='./static/data/dataset_1/Teams.csv'):
    data = pd.read_csv(path)

    return data


def get_ball_by_ball(path='./static/data/dataset_2/ipl_scores.csv'):
    data = pd.read_csv(path)

    return data



if __name__ == '__main__':
    # print(get_matches_data())
    # print(get_teams('../../static/data/dataset_1/Teams.csv'))
    print(get_ball_by_ball('../../static/data/dataset_2/ipl_scores.csv'))