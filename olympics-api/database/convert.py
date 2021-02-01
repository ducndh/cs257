# CS257 - Daeyeon Kim, Duc Nguyen
import csv

def create_csv(created_collection, field_names, file_to_write):
    with open("archive/" + file_to_write, "w") as csv_file:
        writer = csv.writer(csv_file)
        for data in created_collection:
            writer.writerow(created_collection[data])

def main():
    athletes_dict = {}
    sports_dict = {}
    games_dict = {}
    events_dict = {}
    medals_dict = {}
    teams_dict = {}
    athletes_teams_dict = {}
    sports_events_dict = {}
    athletes_events_medals_dict = {}
    with open("archive/athlete_events.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter = ",")
        athlete_id = 0
        sport_id = 0 
        game_id = 0
        event_id = 0
        medal_id = 0
        team_id = 0
        row_id = 0
        athlete_team_id = 0
        sport_event_id = 0
        next(reader)
        for row in reader:
            # athletes table
            if row[1] not in athletes_dict:
                athlete_id += 1
                if row[4] == "NA":
                    height = "NULL"
                else:
                    height = row[4]

                if row[5] == "NA":
                    weight = "NULL"
                else:
                    weight = row[5]
                athletes_dict[row[1]] = [athlete_id, row[1], row[2], height, weight]
            
            # teams table
            if (row[6], row[7]) not in teams_dict:
                team_id += 1
                teams_dict[(row[6], row[7])] = [team_id, row[6], row[7]]
                current_team_id = team_id
            else:
                current_team_id = teams_dict[(row[6], row[7])][0]

            # sports table
            if row[12] not in sports_dict:
                sport_id += 1
                sports_dict[row[12]] = [sport_id, row[12]]
                current_sport_id = sport_id
            else:
                current_sport_id = sports_dict[row[12]][0]

            # games table
            if (row[9], row[10]) not in games_dict:
                game_id += 1
                games_dict[(row[9], row[10])] = [game_id, row[9], row[10], row[11]]
                current_game_id = game_id
            else:
                current_game_id = games_dict[(row[9], row[10])][0]

            # events table
            if row[13] not in events_dict:
                event_id += 1
                events_dict[row[13]] = [event_id, row[13]]
                current_event_id = event_id
            else:
                current_event_id = events_dict[row[13]][0]    
            
            # medals table
            if row[14] not in medals_dict:
                medal_id += 1
                medals_dict[row[14]] = [medal_id, row[14]]
                current_medal_id = medal_id
            else:
                current_medal_id = medals_dict[row[14]][0]   
            
            # athletes_teams table
            if (athlete_id, current_team_id) not in athletes_teams_dict:
                athlete_team_id += 1
                athletes_teams_dict[(athlete_id, current_team_id)] = \
                [athlete_team_id, athlete_id, current_team_id]
                current_athlete_team_id = athlete_team_id
            else:
                current_athlete_team_id = athletes_teams_dict[(athlete_id, current_team_id)][0]

            # sports_events table
            if (current_event_id, current_sport_id) not in sports_events_dict:
                sport_event_id += 1
                sports_events_dict[(current_event_id, current_sport_id)] = \
                [sport_event_id, current_event_id, current_sport_id]
                current_sport_event_id = sport_event_id
            else:
                current_sport_event_id = sports_events_dict[(current_event_id, current_sport_id)][0]

            # athletes_events_medals table
            row_id += 1
            athletes_events_medals_dict[row_id] = \
            [row_id, current_athlete_team_id, current_game_id, current_sport_event_id, current_medal_id]
    
    create_csv(athletes_dict, "athletes.csv")
    
    create_csv(teams_dict, "teams.csv")
    
    create_csv(sports_dict, "sports.csv")
    
    create_csv(games_dict, "games.csv")
    
    create_csv(events_dict, "events.csv")
    
    create_csv(medals_dict, "medals.csv")

    create_csv(athletes_teams_dict, "athletes_teams.csv")
    
    create_csv(sports_events_dict, "sports_events.csv")

    create_csv(athletes_events_medals_dict, "athletes_events_medals.csv")
if __name__ == "__main__":
    main()
            