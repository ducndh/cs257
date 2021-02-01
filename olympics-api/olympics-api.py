'''
Author: Duc Nguyen, Kevin Phung
Date: 2/1/2021
'''

import argparse
import sys
import flask
import json
import psycopg2
import datetime

# Please create your config file
from config import password
from config import database
from config import user


app = flask.Flask(__name__)


def connection_to_database():
    '''
    Return a connection object to the postgres database
    '''
    try:
        connection = psycopg2.connect(database = database, user= user, password = password)
        return connection
    except Exception as e:
        print(e)
        exit()

@app.route('/help')
def get_help():
    return flask.render_template('help.html')

def get_games_query():
    '''
    Get a cursor that contain all the games sort by year
    Returns:
        cursor: the cursor object to iterate over
    '''
    query = "\
        SELECT games.id, games.year, games.season, games.city \
        FROM games.csv \
        ORDER BY games.year;\
        "
    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.close()
        return cursor
    except Exception as e:
        print(e)
        exit()

@app.route('/games')
def get_games(cursor):
    games_list = []
    for row in cursor:
        game_dict = {}
        game_dict['id'] = row[0]
        game_dict['year'] = row[1]
        game_dict['season'] = row[2]
        game_dict['city'] = row[3]
    # cursor.close()
    return json.dump(games_list)
        
def get_nocs_query():
    query = "\
    SELECT teams.NOC, teams.team \
    FROM teams \
    ORDER BY teams.team; \
    "
    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.close()
        return cursor
    except Exception as e:
        print(e)
        exit()

@app.route('/nocs')
def get_nocs(cursor):
    nocs_list = []
    for row in cursor:
        noc_dict = {}
        noc_dict['NOC'] = row[0]
        noc_dict['team'] = row[1]
    # cursor.close()
    return json.dump(nocs_list)


def get_medalists_query():
    noc = flask.request.args.get('noc')
    query = "\
    SELECT athletes.id, athletes.name, athletes.sex, sports_events.sport, sports_events.event, medals.medal \
    FROM athletes_events_medals, medals, sports_events, athletes_teams, athletes, teams\
    WHERE medals.medal != 'NA'\
    AND medals.id = athletes_events_medals.medal_id \
    AND sports_events.id = athletes_events_medals.sport_event_id\
    AND athletes_teams.id = athletes_events_medals.athlete_id \
    AND athletes.id = athletes_teams.athlete_id \
    "

    if noc is not None:
        query += "\
        AND teams.NOC = '{}'".format(noc)

    query += ';'
        
    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.close()
        return cursor
    except Exception as e:
        print(e)
        exit()
        
@app.route('/medalists/games/<games_id>?[noc=noc_abbreviation]')
def get_medalists(cursor):
    medalists_list = []
    for row in cursor:
        medalist_dict = {}
        medalist_dict['id'] = row[0]
        medalist_dict['name'] = row[1]
        medalist_dict['sex'] = row[2]
        medalist_dict['sport'] = row[3]
        medalist_dict['event'] = row[4]
        medalist_dict['medal'] = row[5]
    # cursor.close()
    return json.dump(medalists_list)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('An API to retrieve data from the olympics database')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)