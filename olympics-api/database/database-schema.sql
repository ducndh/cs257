CREATE TABLE athletes (
  id SERIAL,
  name text,
  sex text,
  height int,
  weight float
);

CREATE TABLE teams (
  id SERIAL,
  team text,
  NOC text
);

CREATE TABLE sports (
  id SERIAL,
  sport text
);

CREATE TABLE games (
  id SERIAL,
  year int,
  season text,
  city text
);

CREATE TABLE events (
  id SERIAL ,
  event text
);

CREATE TABLE medals (
  id SERIAL,
  medal text
);

CREATE TABLE athletes_teams (
  id SERIAL,
  athlete_id int,
  team_id int
);

CREATE TABLE sports_events (
  id SERIAL,
  event_id int,
  sport_id int
);

CREATE TABLE athletes_events_medals (
  id SERIAL,
  athlete_team_id int,
  game_id int,
  sport_event_id int,
  medal_id int
);