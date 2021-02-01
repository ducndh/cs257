# Winter 2021 CS257 - Daeyeon Kim, Duc Nguyen

import psycopg2
import argparse
import sys
from config import database
from config import user
from config import password

def get_parsed_args():
    '''
    Get the user input and check the amount of arguments
    '''
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description='''Take one type of argument only''') 
    group = parser.add_mutually_exclusive_group()

    group.add_argument("--athletes_by_NOC", "-a", help = '''
    Example: python3 olympics.py -a USA
    Prints the list of names of all the athletes from a specified NOC that contain the search string. Specified NOC must be capitalized.
    ''', type = str, dest= 'NOC', nargs = 1)

    group.add_argument("--NOC_gold_medals", '-g' , help = '''
    Example: python3 olympics.py -g
    Lists all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals.
    '''
    , action = "store_true")

    group.add_argument("--events_of_athletes", "-e", help = '''
    Example: python3 olympics.py -a Aaland
    List all the events that the player containing the search string has played in the Olympic. The search string is case-sensitive. \
    To search for the fullname of the player, use parentheses around the search string like below.
    Example: python3 olympics.py -a "Per Knut Aaland"    
    '''
    , type = str, dest= 'athlete', nargs = 1)

    args = parser.parse_args()
    return args

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

def get_athletes_by_NOC(NOC,connection):
    '''
    Get a cursor that contain all athletes of the specified NOC
    Parameters:
        NOC: the NOC to search athletes from
        connection: the connection object to the database
    Returns:
        cursor: the cursor object to iterate over
    '''
    query = "\
        SELECT teams.NOC, athletes.name \
        FROM athletes, teams, athletes_teams \
        WHERE teams.NOC = %s \
        AND teams.id = athletes_teams.team_id \
        AND athletes.id = athletes_teams.athlete_id; \
        "
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, (NOC,))
        return cursor
    except Exception as e:
        print(e)
        exit()

def get_NOC_gold_medals(connection):
    '''
    Get a cursor that contain all the gold medals of each NOCS
    Parameters:
        connection: the connection object to the database
    Returns:
        cursor: the cursor object that can be used to iterate rows over the specified query
    '''
    query = "\
        SELECT teams.NOC, COUNT(medals.medal) \
        FROM teams, medals, athletes_events_medals, athletes_teams \
        WHERE teams.id = athletes_teams.team_id \
        AND athletes_teams.id = athletes_events_medals.athlete_team_id \
        AND medals.id = athletes_events_medals.medal_id \
        AND medals.medal = 'Gold' \
        GROUP BY teams.NOC \
        ORDER BY COUNT(medals.medal) DESC; \
        "

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor
    except Exception as e:
        print(e)
        exit()

def get_events_of_athletes(athlete, connection):
    '''
    Get a cursor that contain the events of players that has the search string in their name
    Parameters:
        connection: the connection object to the database
    Returns:
        cursor: the cursor object that can be used to iterate rows over the specified query
    '''
    query = "\
        SELECT athletes.name, events.event, games.year, games.season, medals.medal \
        FROM medals, games, athletes_events_medals, athletes_teams, athletes, events\
        WHERE athletes.name LIKE '%" + athlete + "%' \
        AND athletes.id = athletes_teams.athlete_id \
        AND athletes_teams.id = athletes_events_medals.athlete_team_id \
        AND medals.id = athletes_events_medals.medal_id \
        AND games.id = athletes_events_medals.game_id \
        AND events.id = athletes_events_medals.sport_event_id \
        ORDER BY year; \
    "

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor
    except Exception as e:
        print(e)
        exit()

def print_athletes_by_NOC(cursor, query_name):
    '''
    Formats and prints out the list of athletes by NOC.
    Parameters: 
        cursor: A cursor object to iterate through the list seacrched by query
        query_name: Argument from the command line to specify the printed output.
    Return:
        Prints out the list of athletes searched by NOC.
    '''
    print(query_name + '\n')
    ahtletes_count = 0
    for row in cursor:
        ahtletes_count += 1
        print(row[1])
    print('\nNumber of athletes :', ahtletes_count)
    print('=' * 50)

def print_NOC_of_gold_medal(cursor, query_name):
    '''
    Formats and prints out the list of NOCs and the number of their gold medals.
    Parameters: 
        cursor: A cursor object to iterate through the list seacrched by query
        query_name: Argument from the command line to specify the printed output.
    Return:
        Prints out the list of NOCs and their gold medals.
    '''
    print(query_name + '\n')
    for row in cursor:
        print(row[0] + ': ' + str(row[1]))
    print('=' * 50)

def print_events_of_athletes(cursor, query_name):
    '''
    Formats and prints out the list of events, games, and medals by athlete.
    Parameters: 
        cursor: A cursor object to iterate through the list seacrched by query
        query_name: Argument from the command line to specify the printed output.
    Return:
        Prints out the list of events, games, and medals by athlete.
    '''
    print(query_name + '\n')
    athlete_dict = {}
    for row in cursor:
        if row[0] not in athlete_dict:
            athlete_dict[row[0]] = [[row[1], row[2], row[3], row[4]]]
        else:
            athlete_dict[row[0]].append([row[1], row[2], row[3], row[4]])
    for athlete in athlete_dict:
        print(athlete + "\n")
        for event in athlete_dict[athlete]:
            print(event[0] + ' | ' + str(event[1]) + ' ' + event[2] + ' | ' + event[3])
        print('-' * 50 + '\n')
    print('=' * 50)
    
def main():
    connection = connection_to_database()
    args = get_parsed_args()
    if args.NOC != None:
        print_athletes_by_NOC(get_athletes_by_NOC(args.NOC[0], connection), 'List of all athletes of ' + args.NOC[0])
    elif args.NOC_gold_medals == True:
        print_NOC_of_gold_medal(get_NOC_gold_medals(connection), 'List of all gold medals won by all NOCs descending')
    elif args.athlete != None:
        print_events_of_athletes(get_events_of_athletes(args.athlete[0], connection), 'List of all events played by ' + args.athlete[0])
    else:
        print("No arguments specified. Type --help for more information.", file=sys.stderr)
    connection.close()
    
if __name__ == "__main__":
    main()