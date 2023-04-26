import sqlite3
import pandas as pd
from get_data import get_teams


CONNECTION = sqlite3.connect('./db.sqlite3')
CURSOR = CONNECTION.cursor()

def insert_teams(file_path: str = './static/data/dataset_1/Teams.csv') -> bool:
    try:
        teams = get_teams(file_path)
        teams.to_sql('teams', CONNECTION, if_exists='append', index = False)
    except Exception as ex:
        print('[Error][import_data:insert_teams]: ', ex)
        return False
    else: return True
    

def get_all_rows(table: str) -> str:
    try:
        output = CURSOR.execute(f'''SELECT * FROM {table}''').fetchall()
    except Exception as ex:
        print('[ERROR][import_data:get_all_rows]: ', ex)
        return ''
    else: return output


def remove_all_rows(table: str) -> bool:
    try:
        CURSOR.execute(f'''DELETE FROM {table}''')
        CONNECTION.commit()
    except Exception as ex:
        print('[ERROR][import_data:remove_all_data]: ', ex)
        return False
    else: return True


def remove_table(table: str) -> bool:
    try:
        CURSOR.execute(f'''DROP TABLE {table}''')
        CONNECTION.commit()
    except Exception as ex:
        print('[ERROR][import_data:remove_table]: ', ex)
        return False
    else: return True


def all_table_names():
    try:
        table_names = CURSOR.execute(f'''SELECT name FROM sqlite_schema WHERE type = 'table' AND name NOT LIKE 'sqlite_%';''').fetchall()
    except Exception as ex:
        print('[ERROR][import_data:all_table_names]: ', ex)
        return None
    else: return table_names


if __name__ == '__main__':
    # print(insert_teams(file_path='./static/data/dataset_1/Teams.csv'))
    # print(remove_table('teams'))
    print('output >>>', get_all_rows('teams'))
    # print('remove >>>>', remove_all_rows('teams'))
    # print('Table Names >>>', all_table_names())
