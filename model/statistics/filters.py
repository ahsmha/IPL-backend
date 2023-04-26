import pandas as pd


MATCHES_FILE_PATH = './static/data/dataset_3/IPL_Matches_2008_2022.csv'
BALLS_FILE_PATH = './static/data/dataset_3/IPL_Ball_by_Ball_2008_2022.csv'


class Stats:
    MATCHES = pd.read_csv(MATCHES_FILE_PATH)
    BALLS = pd.read_csv(BALLS_FILE_PATH)
    def __init__(self) -> None:
        self.MATCHES['Season'] = self.MATCHES['Season'].str.replace('2007/08', '2008')
        self.MATCHES['Season'] = self.MATCHES['Season'].str.replace('2009/10', '2010')
        self.MATCHES['Season'] = self.MATCHES['Season'].str.replace('2020/21', '2020')

        # Rename old names to new names
        self.MATCHES['Team1'] = self.MATCHES['Team1'].str.replace('Delhi Daredevils', 'Delhi Capitals')
        self.MATCHES['Team1'] = self.MATCHES['Team1'].str.replace('Kings XI Punjab', 'Punjab Kings')
        self.MATCHES['Team1'] = self.MATCHES['Team1'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
        self.MATCHES['Team1'] = self.MATCHES['Team1'].str.replace('Rising Pune Supergiants', 'Rising Pune Supergiant')
        self.MATCHES['Team2'] = self.MATCHES['Team2'].str.replace('Delhi Daredevils', 'Delhi Capitals')
        self.MATCHES['Team2'] = self.MATCHES['Team2'].str.replace('Kings XI Punjab', 'Punjab Kings')
        self.MATCHES['Team2'] = self.MATCHES['Team2'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
        self.MATCHES['Team2'] = self.MATCHES['Team2'].str.replace('Rising Pune Supergiants', 'Rising Pune Supergiant')
        self.MATCHES['TossWinner'] = self.MATCHES['TossWinner'].str.replace('Delhi Daredevils', 'Delhi Capitals')
        self.MATCHES['TossWinner'] = self.MATCHES['TossWinner'].str.replace('Kings XI Punjab', 'Punjab Kings')
        self.MATCHES['TossWinner'] = self.MATCHES['TossWinner'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
        self.MATCHES['TossWinner'] = self.MATCHES['TossWinner'].str.replace('Rising Pune Supergiants', 'Rising Pune Supergiant')
        self.MATCHES['WinningTeam'] = self.MATCHES['WinningTeam'].str.replace('Delhi Daredevils', 'Delhi Capitals')
        self.MATCHES['WinningTeam'] = self.MATCHES['WinningTeam'].str.replace('Kings XI Punjab', 'Punjab Kings')
        self.MATCHES['WinningTeam'] = self.MATCHES['WinningTeam'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
        self.MATCHES['WinningTeam'] = self.MATCHES['WinningTeam'].str.replace('Rising Pune Supergiants', 'Rising Pune Supergiant')
        
        self.BALLS['BattingTeam'] = self.BALLS['BattingTeam'].str.replace('Delhi Daredevils', 'Delhi Capitals')
        self.BALLS['BattingTeam'] = self.BALLS['BattingTeam'].str.replace('Kings XI Punjab', 'Punjab Kings')
        self.BALLS['BattingTeam'] = self.BALLS['BattingTeam'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
        self.BALLS['BattingTeam'] = self.BALLS['BattingTeam'].str.replace('Rising Pune Supergiants', 'Rising Pune Supergiant')

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
        self.MATCHES = self.MATCHES[self.MATCHES['Team1'].isin(current_teams)]
        self.MATCHES = self.MATCHES[self.MATCHES['Team2'].isin(current_teams)]
        self.MATCHES = self.MATCHES[self.MATCHES['TossWinner'].isin(current_teams)]
        self.MATCHES = self.MATCHES[self.MATCHES['WinningTeam'].isin(current_teams)]
        self.BALLS = self.BALLS[self.BALLS['BattingTeam'].isin(current_teams)]

        # Merge the match_df dataset with balls dataset
        self.DATA = self.MATCHES.merge(self.BALLS, on='ID')

    def get_most_fours_by_season(self, season='alltime', team='allteams'):
        try:
            if season == 'alltime' and team == 'allteams':
                most_fours = self.DATA[self.DATA['batsman_run'] == 4].groupby('batter').size().reset_index(name='count')
                most_fours = most_fours.sort_values('count')[::-1]
                return self.format_data(most_fours)
            elif season == 'alltime' and team != 'allteams':
                    new_data = self.DATA[self.DATA['BattingTeam'] == team]
                    most_fours = new_data[new_data['batsman_run'] == 4].groupby('batter').size().reset_index(name='count')[::-1]
                    most_fours = most_fours.sort_values('count')[::-1]
                    return self.format_data(most_fours)
            elif season != 'alltime' and team == 'allteams':
                most_fours = self.DATA[self.DATA['batsman_run'] == 4].groupby(['batter', 'Season']).size().reset_index(name='count')
                most_fours = most_fours[most_fours['Season'] == season].sort_values('count')[::-1]
                return self.format_data(most_fours)
            elif season != 'alltime' and team != 'allteams':
                new_data = self.DATA[self.DATA['BattingTeam'] == team]
                most_fours = new_data[new_data['batsman_run'] == 4].groupby(['batter', 'Season']).size().reset_index(name='count')
                most_fours = most_fours[most_fours['Season'] == season].sort_values('count')[::-1]
                return self.format_data(most_fours)
        except Exception as ex:
            print('[ERROR][filters.py:Stats:get_most_fours_by_season]: ', ex)
            raise ex
            
    def get_most_fours_by_inning(self, season='alltime', team='allteams'):
        try:
            if season == 'alltime' and team == 'allteams':
                most_fours = self.DATA[self.DATA['batsman_run'] == 4].groupby(['batter', 'ID', 'innings']).size().reset_index(name='count')
                most_fours = most_fours.sort_values('count')[::-1]
                return self.format_data(most_fours)
            elif season == 'alltime' and team != 'allteams':
                new_data = self.DATA[self.DATA['BattingTeam'] == team]
                most_fours = new_data[new_data['batsman_run'] == 4].groupby
                return self.format_data(most_fours)
            elif season != 'alltime' and team == 'allteams':
                most_fours = self.DATA[self.DATA['batsman_run'] == 4].groupby(['batter', 'Season', 'ID', 'innings']).size().reset_index(name='count')
                most_fours = most_fours[most_fours['Season'] == season].sort_values('count')[::-1]
                return self.format_data(most_fours)
            elif season != 'alltime' and team != 'allteams':
                new_data = self.DATA[self.DATA['BattingTeam'] == team]
                most_fours = new_data[new_data['batsman_run'] == 4].groupby(['batter', 'Season', 'ID', 'innings']).size().reset_index(name='count')
                most_fours = most_fours[most_fours['Season'] == season].sort_values('count')[::-1]
                return self.format_data(most_fours)
        except Exception as ex:
            print('[ERROR][filters.py:Stats:get_most_fours_by_inning]: ', ex)
            raise ex
        
    def get_most_sixes_by_season(self, season='alltime', team='allteams'):
        try:
            if season == 'alltime' and team == 'allteams':
                most_sixes = self.DATA[self.DATA['batsman_run'] == 6].groupby('batter').size().reset_index(name='count')
                most_sixes = most_sixes.sort_values('count')[::-1]
                return self.format_data(most_sixes)
            elif season == 'alltime' and team != 'allteams':
                new_data = self.DATA[self.DATA['BattingTeam'] == team]
                most_sixes = new_data[new_data['batsman_run'] == 6].groupby('batter').size().reset_index(name='count')[::-1]
                most_sixes = most_sixes.sort_values('count')[::-1]
                return self.format_data(most_sixes)
            elif season != 'alltime' and team == 'allteams':
                most_sixes = self.DATA[self.DATA['batsman_run'] == 6].groupby(['batter', 'Season']).size().reset_index(name='count')
                most_sixes = most_sixes[most_sixes['Season'] == season].sort_values('count')[::-1]
                return self.format_data(most_sixes)
            elif season != 'alltime' and team != 'allteams':
                new_data = self.DATA[self.DATA['BattingTeam'] == team]
                most_sixes = new_data[new_data['batsman_run'] == 6].groupby(['batter', 'Season']).size().reset_index(name='count')
                most_sixes = most_sixes[most_sixes['Season'] == season].sort_values('count')[::-1]
                return self.format_data(most_sixes)
        except Exception as ex:
            print('[ERROR][filters.py:Stats:get_most_sixes_by_season]: ', ex)
            raise ex
        
    def get_most_sixes_by_inning(self, season='alltime', team='allteams'):
        try:
            if season == 'alltime' and team == 'allteams':
                most_sixes = self.DATA[self.DATA['batsman_run'] == 6].groupby(['batter', 'ID', 'innings']).size().reset_index(name='count')
                most_sixes = most_sixes.sort_values('count')[::-1]
                return self.format_data(most_sixes)
            elif season == 'alltime' and team != 'allteams':
                new_data = self.DATA[self.DATA['BattingTeam'] == team]
                most_sixes = new_data[new_data['batsman_run'] == 6].groupby(['batter', 'ID', 'innings']).size().reset_index(name='count')[::-1]
                most_sixes = most_sixes.sort_values('count')[::-1]
                return self.format_data(most_sixes)
            elif season != 'alltime' and team == 'allteams':
                most_sixes = self.DATA[self.DATA['batsman_run'] == 6].groupby(['batter', 'Season', 'ID', 'innings']).size().reset_index(name='count')
                most_sixes = most_sixes[most_sixes['Season'] == season].sort_values('count')[::-1]
                return self.format_data(most_sixes)
            elif season != 'alltime' and team != 'allteams':
                new_data = self.DATA[self.DATA['BattingTeam'] == team]
                most_sixes = new_data[new_data['batsman_run'] == 6].groupby(['batter', 'Season', 'ID', 'innings']).size().reset_index(name='count')
                most_sixes = most_sixes[most_sixes['Season'] == season].sort_values('count')[::-1]
                return self.format_data(most_sixes)
        except Exception as ex:
            print('[ERROR][filters.py:Stats:get_most_sixes_by_inning]: ', ex)
            raise ex
        
    def get_most_fifties(self, season='alltime', team='allteams'):
        try:
            if season == 'alltime' and team == 'allteams':
                most_fifties = self.DATA.groupby(['batter', 'ID', 'innings'])['batsman_run'].sum().reset_index(name='runs')
                most_fifties = most_fifties[(most_fifties['runs'] >= 50) & (most_fifties['runs'] < 100)]
                most_fifties = most_fifties.groupby('batter').size().reset_index(name='count').sort_values('count')[::-1]
                return self.format_data(most_fifties)
            elif season == 'alltime' and team != 'allteams':
                new_data = self.DATA[self.DATA['BattingTeam'] == team]
                most_fifties = new_data.groupby(['batter', 'ID', 'innings'])['batsman_run'].sum().reset_index(name='runs')
                most_fifties = most_fifties[(most_fifties['runs'] >= 50) & (most_fifties['runs'] < 100)]
                most_fifties = most_fifties.groupby('batter').size().reset_index(name='count').sort_values('count')[::-1]
                return self.format_data(most_fifties)
            elif season != 'alltime' and team == 'allteams':
                new_data = self.DATA[self.DATA['Season'] == season]
                most_fifties = new_data.groupby(['batter', 'ID', 'innings'])['batsman_run'].sum().reset_index(name='runs')
                most_fifties = most_fifties[(most_fifties['runs'] >= 50) & (most_fifties['runs'] < 100)]
                most_fifties = most_fifties.groupby('batter').size().reset_index(name='count').sort_values('count')[::-1]
                return self.format_data(most_fifties)
            elif season != 'alltime' and team != 'allteams':
                new_data = self.DATA[(self.DATA['BattingTeam'] == team) & (self.DATA['Season'] == season)]
                most_fifties = new_data.groupby(['batter', 'ID', 'innings'])['batsman_run'].sum().reset_index(name='runs')
                most_fifties = most_fifties[(most_fifties['runs'] >= 50) & (most_fifties['runs'] < 100)]
                most_fifties = most_fifties.groupby('batter').size().reset_index(name='count').sort_values('count')[::-1]
                return self.format_data(most_fifties)
        except Exception as ex:
            print('[ERROR][filters.py:Stats:get_most_fifties]: ', ex)
            raise ex
        
    def get_most_centuries(self, season='alltime', team='allteams'):
        try:
            if season == 'alltime' and team == 'allteams':
                most_centuries = self.DATA.groupby(['batter', 'ID', 'innings'])['batsman_run'].sum().reset_index(name='runs')
                most_centuries = most_centuries[most_centuries['runs'] >= 100]
                most_centuries = most_centuries.groupby('batter').size().reset_index(name='count').sort_values('count')[::-1]
                return self.format_data(most_centuries)
            elif season == 'alltime' and team != 'allteams':
                new_data = self.DATA[self.DATA['BattingTeam'] == team]
                most_centuries = new_data.groupby(['batter', 'ID', 'innings'])['batsman_run'].sum().reset_index(name='runs')
                most_centuries = most_centuries[most_centuries['runs'] >= 100]
                most_centuries = most_centuries.groupby('batter').size().reset_index(name='count').sort_values('count')[::-1]
                return self.format_data(most_centuries)
            elif season != 'alltime' and team == 'allteams':
                new_data = self.DATA[self.DATA['Season'] == season]
                most_centuries = new_data.groupby(['batter', 'ID', 'innings'])['batsman_run'].sum().reset_index(name='runs')
                most_centuries = most_centuries[most_centuries['runs'] >= 100]
                most_centuries = most_centuries.groupby('batter').size().reset_index(name='count').sort_values('count')[::-1]
                return self.format_data(most_centuries)
            elif season != 'alltime' and team != 'allteams':
                new_data = self.DATA[(self.DATA['BattingTeam'] == team) & (self.DATA['Season'] == season)]
                most_centuries = new_data.groupby(['batter', 'ID', 'innings'])['batsman_run'].sum().reset_index(name='runs')
                most_centuries = most_centuries[most_centuries['runs'] >= 100]
                most_centuries = most_centuries.groupby('batter').size().reset_index(name='count').sort_values('count')[::-1]
                return self.format_data(most_centuries)
        except Exception as ex:
            print('[ERROR][filters.py:Stats:get_most_centuries]: ', ex)
            raise ex

    def format_data(self, data):
        try:
            result = data.values.tolist()
            return result
        except Exception as ex:
            print('[ERROR][filters.py:Stats:format_data]: ', ex)
            raise ex