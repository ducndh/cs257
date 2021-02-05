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
    Gets a cursor that contain all the games and their details sorted by year

    Returns:
        a cursor that can be iterated over with the results of the queries
    '''
    query = "\
        SELECT games.id, games.year, games.season, games.city \
        FROM games \
        ORDER BY games.year;\
        "
    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor
    except Exception as e:
        print(e)
        exit()

@app.route('/games')
def get_games():
    '''
    Returns a JSON response of games and their details sorted by year
    '''
    games_list = []
    cursor= get_games_query()
    for row in cursor:
        game_dict = {}
        game_dict['id'] = row[0]
        game_dict['year'] = row[1]
        game_dict['season'] = row[2]
        game_dict['city'] = row[3]
        games_list.append(game_dict)
    cursor.close()
    return json.dumps(games_list)

def get_nocs_query():
    '''
    Gets a cursor that contain all nocs and their full names

    Returns:
        a cursor that can be iterated over with the results of the queries
    '''
    query = "\
    SELECT noc_regions.NOC, noc_regions.region \
    FROM noc_regions;\
    "
    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor
    except Exception as e:
        print(e)
        exit()

@app.route('/nocs')
def get_nocs():
    '''
    Returns a JSON response of nocs and their full names
    '''
    nocs_list = []
    cursor=get_nocs_query()
    for row in cursor:
        noc_dict = {}
        noc_dict['abbreviation'] = row[0]
        noc_dict['name'] = row[1]
        nocs_list.append(noc_dict)
    cursor.close()
    return json.dumps(nocs_list)


def get_medalists_query(games_id):
    '''
    Gets a cursor that contains all the medalists and their respective details

    Returns:
        a cursor that can be iterated over with the results of the queries
    '''
    noc = flask.request.args.get('noc')
    query = "\
    SELECT DISTINCT athletes.id, athletes.name, athletes.sex, sports.sport, events.event, medals.medal \
    FROM athletes_events_medals, medals, sports_events, athletes_teams, athletes, teams,games,sports,events\
    WHERE medals.medal != 'NA'\
    AND medals.id = athletes_events_medals.medal_id \
    AND sports_events.id = athletes_events_medals.sport_event_id\
    AND athletes_teams.id = athletes_events_medals.athlete_team_id \
    AND athletes.id = athletes_teams.athlete_id \
    AND sports_events.sport_id = sports.id \
    AND sports_events.event_id = events.id \
    AND athletes_events_medals.game_id = games.id\
    AND games.id ="  + games_id + "\
    "


    if noc is not None:
        query += "\
        AND teams.id = athletes_teams.team_id\
        AND teams.NOC = '{}'".format(noc)

    query += ";"



    connection = connection_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor
    except Exception as e:
        print(e)
        exit()

@app.route('/medalists/games/<games_id>')
def get_medalists(games_id):
    '''
    Returns a JSON response of medalists and their respective details based on the following GET parameters:
    games_id, int : reject any games who's games_id does not match this integer
    noc, text : reject any medalist who's noc does not match this noc exactly during the specified games.

    if the noc parameter is absent, then any medalist is treated as though
    it meets the corresponding constraint.
    '''
    cursor=get_medalists_query(games_id)
    medalists_list = []
    for row in cursor:
        medalist_dict = {}
        medalist_dict['athlete_id'] = row[0]
        medalist_dict['athlete_name'] = row[1]
        medalist_dict['athlete_sex'] = row[2]
        medalist_dict['sport'] = row[3]
        medalist_dict['event'] = row[4]
        medalist_dict['medal'] = row[5]
        medalists_list.append(medalist_dict)
    cursor.close()
    return json.dumps(medalists_list)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('An API to retrieve data from the olympics database')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
