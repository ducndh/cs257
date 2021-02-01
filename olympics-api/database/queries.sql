'''List all the NOCs (National Olympic Committees), in alphabetical order by abbreviation. 
These entities, by the way, are mostly equivalent to countries. 
But in some cases, you might find that a portion of a country participated in a particular games 
(e.g. one guy from Newfoundland in 1904) or some other oddball situation.'''

SELECT DISTINCT teams.NOC 
FROM teams
ORDER BY NOC ASC;

'''List the names of all the athletes from Kenya. 
If your database design allows it, sort the athletes by last name.'''

SELECT DISTINCT athletes.name
FROM athletes, teams, athletes_teams
WHERE teams.NOC = 'KEN'
AND teams.id = athletes_teams.team_id
AND athletes.id = athletes_teams.athlete_id
ORDER BY athletes.name;

'''List all the medals won by Greg Louganis, sorted by year. 
Include whatever fields in this output that you think appropriate.'''

SELECT events.event, games.year, games.season, medals.medal
FROM medals, games, athletes_events_medals, athletes_teams, athletes, events
WHERE athletes.name LIKE '%Greg%'
AND athletes.name LIKE '%Louganis%'
AND medals.id != 1
AND athletes.id = athletes_teams.athlete_id
AND athletes_teams.id = athletes_events_medals.athlete_team_id
AND medals.id = athletes_events_medals.medal_id
AND games.id = athletes_events_medals.game_id
AND events.id = athletes_events_medals.sport_event_id
ORDER BY year;

'''List all the NOCs and the number of gold medals they have won, 
in decreasing order of the number of gold medals.'''

SELECT teams.NOC, COUNT(medals.medal)
FROM teams, medals, athletes_events_medals, athletes_teams
WHERE teams.id = athletes_teams.team_id
AND athletes_teams.id = athletes_events_medals.athlete_team_id
AND medals.id = athletes_events_medals.medal_id
AND medals.medal = 'Gold'
GROUP BY teams.NOC
ORDER BY COUNT(medals.medal) DESC;