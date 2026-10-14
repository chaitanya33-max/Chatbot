"""Source links and the small set of profiles that cannot be loaded from feeds."""

REFERENCE_CHECKED = "2026-10-13"

SPORTS = [
    {
        "name": "Football",
        "slug": "football",
        "mode": "live-rosters",
        "description": "Current club squads from ESPN's public roster feed. Player season and career statistics link to the provider profile.",
        "source": "https://site.api.espn.com/apis/site/v2/sports/soccer/",
        "source_label": "ESPN public data feed (third-party, not a league API)",
    },
    {
        "name": "Run Club",
        "slug": "run-club",
        "mode": "directory-links",
        "description": "Athlete search, personal bests, and results are linked to World Athletics. Its terms do not permit us to scrape or republish its athlete database.",
        "source": "https://worldathletics.org/athletes",
        "source_label": "World Athletics athlete search",
    },
    {
        "name": "Basketball",
        "slug": "basketball",
        "mode": "live-rosters",
        "description": "Current NBA club squads from ESPN's public roster feed. Player season and career statistics link to the provider profile.",
        "source": "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/",
        "source_label": "ESPN public data feed (third-party, not an NBA API)",
    },
    {
        "name": "Yoga + Move",
        "slug": "yoga-move",
        "mode": "directory-links",
        "description": "A dated profile of Iyengar Yoga founder B.K.S. Iyengar and direct links to the institute and Yoga Alliance directory. No instructor credentials are inferred.",
        "source": "https://rimyi.org/",
        "source_label": "Ramamani Iyengar Memorial Yoga Institute",
    },
    {
        "name": "Cricket",
        "slug": "cricket",
        "mode": "official-links",
        "description": "Official ICC and IPL team/player references. No live squad or statistical API is configured, so current rosters and statistics are not mirrored.",
        "source": "https://www.icc-cricket.com/",
        "source_label": "International Cricket Council",
    },
]

TEAMS = [
    {
        "id": "real-madrid", "name": "Real Madrid", "sport": "Football", "country": "Spain",
        "league": "Spanish LALIGA", "league_slug": "esp.1", "espn_id": "86",
        "official_url": "https://www.realmadrid.com/en-US/football/first-team/players",
        "schedule_url": "https://www.espn.com/soccer/team/fixtures/_/id/86",
    },
    {
        "id": "fc-barcelona", "name": "FC Barcelona", "sport": "Football", "country": "Spain",
        "league": "Spanish LALIGA", "league_slug": "esp.1", "espn_id": "83",
        "official_url": "https://www.fcbarcelona.com/en/football/first-team/players",
        "schedule_url": "https://www.espn.com/soccer/team/fixtures/_/id/83",
    },
    {
        "id": "manchester-city", "name": "Manchester City", "sport": "Football", "country": "England",
        "league": "English Premier League", "league_slug": "eng.1", "espn_id": "382",
        "official_url": "https://www.premierleague.com/clubs/11/Manchester-City/squad",
        "schedule_url": "https://www.espn.com/soccer/team/fixtures/_/id/382",
    },
    {
        "id": "manchester-united", "name": "Manchester United", "sport": "Football", "country": "England",
        "league": "English Premier League", "league_slug": "eng.1", "espn_id": "360",
        "official_url": "https://www.premierleague.com/clubs/12/Manchester-United/squad",
        "schedule_url": "https://www.espn.com/soccer/team/fixtures/_/id/360",
    },
    {
        "id": "inter-miami", "name": "Inter Miami CF", "sport": "Football", "country": "United States",
        "league": "MLS", "league_slug": "usa.1", "espn_id": "20232",
        "official_url": "https://www.mlssoccer.com/clubs/inter-miami-cf/roster/",
        "schedule_url": "https://www.espn.com/soccer/team/fixtures/_/id/20232",
    },
    {
        "id": "al-nassr", "name": "Al Nassr", "sport": "Football", "country": "Saudi Arabia",
        "league": "Saudi Pro League", "league_slug": "ksa.1", "espn_id": "817",
        "official_url": "https://www.espn.com/soccer/team/_/id/817/al-nassr",
        "source_label": "ESPN team reference (official club roster link unavailable)",
        "schedule_url": "https://www.espn.com/soccer/team/fixtures/_/id/817",
    },
    {
        "id": "los-angeles-lakers", "name": "Los Angeles Lakers", "sport": "Basketball", "country": "United States",
        "league": "NBA", "league_slug": "nba", "espn_id": "13",
        "official_url": "https://www.nba.com/lakers/roster",
        "schedule_url": "https://www.espn.com/nba/team/schedule/_/name/lal",
    },
    {
        "id": "golden-state-warriors", "name": "Golden State Warriors", "sport": "Basketball", "country": "United States",
        "league": "NBA", "league_slug": "nba", "espn_id": "9",
        "official_url": "https://www.nba.com/warriors/roster",
        "schedule_url": "https://www.espn.com/nba/team/schedule/_/name/gs",
    },
    {
        "id": "boston-celtics", "name": "Boston Celtics", "sport": "Basketball", "country": "United States",
        "league": "NBA", "league_slug": "nba", "espn_id": "2",
        "official_url": "https://www.nba.com/celtics/roster",
        "schedule_url": "https://www.espn.com/nba/team/schedule/_/name/bos",
    },
    {
        "id": "india-men", "name": "India", "sport": "Cricket", "country": "India",
        "league": "International cricket", "official_url": "https://www.bcci.tv/international/men/players",
        "schedule_url": "https://www.icc-cricket.com/fixtures-results",
    },
    {
        "id": "australia-men", "name": "Australia", "sport": "Cricket", "country": "Australia",
        "league": "International cricket", "official_url": "https://www.cricket.com.au/",
        "schedule_url": "https://www.cricket.com.au/fixtures",
    },
    {
        "id": "england-men", "name": "England", "sport": "Cricket", "country": "England",
        "league": "International cricket", "official_url": "https://www.ecb.co.uk/england/men",
        "schedule_url": "https://www.icc-cricket.com/fixtures-results",
    },
    {
        "id": "chennai-super-kings", "name": "Chennai Super Kings", "sport": "Cricket", "country": "India",
        "league": "Indian Premier League", "official_url": "https://www.iplt20.com/teams/chennai-super-kings",
        "schedule_url": "https://www.iplt20.com/matches/fixtures",
    },
    {
        "id": "mumbai-indians", "name": "Mumbai Indians", "sport": "Cricket", "country": "India",
        "league": "Indian Premier League", "official_url": "https://www.iplt20.com/teams/mumbai-indians",
        "schedule_url": "https://www.iplt20.com/matches/fixtures",
    },
    {
        "id": "royal-challengers-bengaluru", "name": "Royal Challengers Bengaluru",
        "sport": "Cricket", "country": "India", "league": "Indian Premier League",
        "official_url": "https://www.iplt20.com/teams/royal-challengers-bengaluru",
        "schedule_url": "https://www.iplt20.com/matches/fixtures",
    },
    {
        "id": "nn-running-team", "name": "NN Running Team", "sport": "Run Club", "country": "International",
        "league": "Professional distance running", "official_url": "https://www.nnrunningteam.com/",
        "schedule_url": "https://worldathletics.org/competition/calendar-results",
    },
    {
        "id": "bowerman-track-club", "name": "Bowerman Track Club", "sport": "Run Club", "country": "United States",
        "league": "Professional distance running", "official_url": "https://www.bowermantc.com/",
        "schedule_url": "https://worldathletics.org/competition/calendar-results",
    },
    {
        "id": "on-athletics-club", "name": "On Athletics Club", "sport": "Run Club", "country": "International",
        "league": "Professional distance running", "official_url": "https://www.on.com/en-us/athletics-club",
        "schedule_url": "https://worldathletics.org/competition/calendar-results",
    },
    {
        "id": "rimyi", "name": "Ramamani Iyengar Memorial Yoga Institute", "sport": "Yoga + Move",
        "country": "India", "league": "Iyengar Yoga", "official_url": "https://rimyi.org/",
        "schedule_url": "https://rimyi.org/",
    },
]

REFERENCE_PLAYERS = [
    {
        "id": "231388", "name": "Kylian Mbappé", "sport": "Football",
        "team_id": "real-madrid", "team_label": "Real Madrid (roster reference)",
        "profile_url": "https://www.espn.com/soccer/player/_/id/231388/kylian-mbappe",
        "source_url": "https://www.espn.com/soccer/player/_/id/231388/kylian-mbappe",
    },
    {
        "id": "45843", "name": "Lionel Messi", "sport": "Football",
        "team_id": "inter-miami", "team_label": "Inter Miami CF (roster reference)",
        "profile_url": "https://www.espn.com/soccer/player/_/id/45843/lionel-messi",
        "source_url": "https://www.espn.com/soccer/player/_/id/45843/lionel-messi",
    },
    {
        "id": "22774", "name": "Cristiano Ronaldo", "sport": "Football",
        "team_id": "al-nassr", "team_label": "Al Nassr (roster reference)",
        "profile_url": "https://www.espn.com/soccer/player/_/id/22774/cristiano-ronaldo",
        "source_url": "https://www.espn.com/soccer/player/_/id/22774/cristiano-ronaldo",
    },
    {
        "id": "253989", "name": "Erling Haaland", "sport": "Football",
        "team_id": "manchester-city", "team_label": "Manchester City (roster reference)",
        "profile_url": "https://www.espn.com/soccer/player/_/id/253989/erling-haaland",
        "source_url": "https://www.espn.com/soccer/player/_/id/253989/erling-haaland",
    },
    {
        "id": "3975", "name": "Stephen Curry", "sport": "Basketball",
        "team_id": "golden-state-warriors", "team_label": "Golden State Warriors (roster reference)",
        "profile_url": "https://www.espn.com/nba/player/_/id/3975/stephen-curry",
        "source_url": "https://www.espn.com/nba/player/_/id/3975/stephen-curry",
    },
    {
        "id": "4065648", "name": "Jayson Tatum", "sport": "Basketball",
        "team_id": "boston-celtics", "team_label": "Boston Celtics (roster reference)",
        "profile_url": "https://www.espn.com/nba/player/_/id/4065648/jayson-tatum",
        "source_url": "https://www.espn.com/nba/player/_/id/4065648/jayson-tatum",
    },
    {
        "id": "lebron-james", "name": "LeBron James", "sport": "Basketball", "country": "United States",
        "position": "Forward", "status": "historical-reference",
        "team_id": "los-angeles-lakers", "team_label": "Los Angeles Lakers (career reference)",
        "profile_url": "https://www.nba.com/stats/player/2544",
        "bio": "NBA career profile and statistics are available from the NBA player page. This record is not presented as a current roster listing.",
        "source_url": "https://www.nba.com/stats/player/2544",
    },
    {
        "id": "virat-kohli", "name": "Virat Kohli", "sport": "Cricket", "country": "India",
        "position": "Batter", "status": "official-reference-only",
        "team_id": "india-men", "team_label": "India (international career reference)",
        "profile_url": "https://www.icc-cricket.com/rankings/mens/player-rankings/test/batting",
        "bio": "India batter. ICC rankings and match records are linked directly; no static statistics are asserted here.",
        "source_url": "https://www.icc-cricket.com/rankings/mens/player-rankings/test/batting",
        "related_team_id": "royal-challengers-bengaluru",
    },
    {
        "id": "rohit-sharma", "name": "Rohit Sharma", "sport": "Cricket", "country": "India",
        "position": "Batter", "status": "official-reference-only",
        "team_id": "india-men", "team_label": "India (international career reference)",
        "profile_url": "https://www.icc-cricket.com/rankings/mens/player-rankings/test/batting",
        "bio": "India batter. Current squad membership and career statistics are not available from a connected cricket feed.",
        "source_url": "https://www.icc-cricket.com/rankings/mens/player-rankings/test/batting",
        "related_team_id": "mumbai-indians",
    },
    {
        "id": "jasprit-bumrah", "name": "Jasprit Bumrah", "sport": "Cricket", "country": "India",
        "position": "Fast bowler", "status": "official-reference-only",
        "team_id": "india-men", "team_label": "India (international career reference)",
        "profile_url": "https://www.icc-cricket.com/rankings/mens/player-rankings/test/bowling",
        "bio": "India fast bowler. Current squad membership and career statistics are not available from a connected cricket feed.",
        "source_url": "https://www.icc-cricket.com/rankings/mens/player-rankings/test/bowling",
        "related_team_id": "mumbai-indians",
    },
    {
        "id": "ms-dhoni", "name": "MS Dhoni", "sport": "Cricket", "country": "India",
        "position": "Wicketkeeper-batter", "status": "historical-reference",
        "team_id": "india-men", "team_label": "India (international career reference)",
        "profile_url": "https://www.icc-cricket.com/",
        "bio": "Former India wicketkeeper-batter and captain. This is a historical profile, not a claim of current international selection.",
        "source_url": "https://www.icc-cricket.com/",
        "related_team_id": "chennai-super-kings",
    },
    {
        "id": "eliud-kipchoge", "name": "Eliud Kipchoge", "sport": "Run Club", "country": "Kenya",
        "position": "Marathon", "status": "official-reference-only",
        "profile_url": "https://worldathletics.org/athletes",
        "bio": "Kenyan distance runner. See World Athletics for the athlete profile, personal bests, and dated competition results.",
        "source_url": "https://worldathletics.org/athletes",
    },
    {
        "id": "sifan-hassan", "name": "Sifan Hassan", "sport": "Run Club", "country": "Netherlands",
        "position": "Distance running / marathon", "status": "official-reference-only",
        "profile_url": "https://worldathletics.org/athletes",
        "bio": "Dutch distance runner. See World Athletics for the athlete profile, personal bests, and dated competition results.",
        "source_url": "https://worldathletics.org/athletes",
    },
    {
        "id": "faith-kipyegon", "name": "Faith Kipyegon", "sport": "Run Club", "country": "Kenya",
        "position": "Middle-distance running", "status": "official-reference-only",
        "profile_url": "https://worldathletics.org/athletes",
        "bio": "Kenyan middle-distance runner. See World Athletics for the athlete profile, personal bests, and dated competition results.",
        "source_url": "https://worldathletics.org/athletes",
    },
    {
        "id": "b-k-s-iyengar", "name": "B.K.S. Iyengar", "sport": "Yoga + Move", "country": "India",
        "position": "Yoga teacher; Iyengar Yoga", "status": "historical-reference",
        "profile_url": "https://rimyi.org/",
        "bio": "Historical yoga teacher and founder of the Ramamani Iyengar Memorial Yoga Institute in Pune, established in 1975. The institute is the source for this dated reference; no current teaching credentials are claimed.",
        "source_url": "https://rimyi.org/",
    },
]

DIRECTORIES = [
    {
        "sport": "Run Club", "name": "World Athletics athlete search",
        "url": "https://worldathletics.org/athletes",
        "note": "Official profiles, personal bests, and competition results. Profile data is linked rather than scraped or republished.",
    },
    {
        "sport": "Run Club", "name": "World Athletics competition calendar",
        "url": "https://worldathletics.org/competition/calendar-results",
        "note": "Official competition schedule and result search.",
    },
    {
        "sport": "Yoga + Move", "name": "Yoga Alliance directory",
        "url": "https://www.yogaalliance.org/Directory",
        "note": "Check a professional's current registration in the official directory. Credentials are not inferred or copied.",
    },
    {
        "sport": "Yoga + Move", "name": "RIMYI classes and institute",
        "url": "https://rimyi.org/",
        "note": "Official institute information. Check the institute for current classes and eligibility; no schedule is mirrored here.",
    },
    {
        "sport": "Cricket", "name": "ICC rankings and player records",
        "url": "https://www.icc-cricket.com/rankings",
        "note": "Official international rankings and player records.",
    },
    {
        "sport": "Cricket", "name": "IPL fixtures and team pages",
        "url": "https://www.iplt20.com/",
        "note": "Official franchise, roster, and fixture references; no live feed is configured.",
    },
]
