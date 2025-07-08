from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import logging
import re
from datetime import datetime, timedelta
from cachetools import TTLCache, cached
import json

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Cache with 1-hour TTL (3600 seconds)
cache = TTLCache(maxsize=100, ttl=3600)

# YouTube API Key
API_KEY = 'AIzaSyDcgJcqp1oGvF-7rAmBwmTPnaVRnA89kkY'

# ✅ Corrected and updated team channel mappings
TEAM_CHANNELS = {
    "chelsea": "UCU2PacFf99vhb3hNiYDmxww",
    "arsenal": "UCpryVRk_VDudG8SHXgWcG0w",
    "manchester_city": "UCkzCjdRMrW2vXLx8mvPVLdQ",
    "liverpool": "UC9LQwHZoucFT94I2h6JOcjw",
    "tottenham_hotspur": "UCe0XAyBUAUAmfWvs0ExF1Dw",  # Now matches normalized name
    "manchester_united": "UC6yW44UGJJBvYTlfC7CRg2Q",  # Matches normalized name
    "newcastle_united": "UCywGl_BPp9QhD0uAcP2HsJw",  # Matches normalized name
    "aston_villa": "UCF66FQIwYFQLg7lqWYizEJA",
    "west_ham_united": "UCCNOsmurvpEit9paBOzWtUg",  # Matches normalized name
    "brighton_&_hove_albion": "UCnQpt1UxLq00NFULxTDHMww",  # Matches normalized name
    "wolverhampton_wanderers": "UCQ7Lqg5Czh5djGK6iOG53KQ",  # Matches normalized name
    "fulham": "UC2VLfz92cTT8jHIFOecC-LA",
    "crystal_palace": "UCWB9N0012fG6bGyj486Qxmg",
    "brentford": "UCAalMUm3LIf504ItA3rqfug",
    "everton": "UCtK4QAczAN2mt2ow_jlGinQ",
    "bournemouth": "UCeOCuVSSweaEj6oVtJZEKQw",
    "nottingham_forest": "UCWJpSxxlgtYPsBk_bElrB5Q",
    "burnley": "UCHTIu1ahUlByR1vnOXYAzew",
    "sheffield_united": "UCXCSB5iaSHr1vue_i8vOw9g",
    "luton_town": "UCQoDXQ4Z2Ie3fTPrpjfT97w"
}


def normalize_team_name(team_name):
    """Normalize team names to match logo dictionary keys"""
    name_mapping = {
        "Brighton": "Brighton & Hove Albion", "Newcastle": "Newcastle United", "West Ham": "West Ham United",
        "Wolves": "Wolverhampton Wanderers", "Spurs": "Tottenham Hotspur", "Tottenham": "Tottenham Hotspur",
        "Ipswich": "Ipswich Town", "Leicester": "Leicester City", "Atletico Madrid": "Atlético Madrid",
        "Athletic Club": "Athletic Bilbao", "Betis": "Real Betis", "Sociedad": "Real Sociedad",
        "Valladolid": "Real Valladolid", "Dortmund": "Borussia Dortmund", "Mönchengladbach": "Borussia Mönchengladbach",
        "Leverkusen": "Bayer Leverkusen", "Frankfurt": "Eintracht Frankfurt", "Stuttgart": "VfB Stuttgart",
        "Mainz": "Mainz 05", "AFC Bournemouth": "Bournemouth", "Burnley": "Burnley", "Leeds": "Leeds United",
        "Liverpool FC": "Liverpool", "Man City": "Manchester City", "Man United": "Manchester United",
        "Ath Madrid": "Atlético Madrid", "PSG": "Paris Saint-Germain", "Inter": "Inter Milan", "Milan": "AC Milan"
    }
    return name_mapping.get(team_name.strip(), team_name.strip())


@cached(cache)
def get_youtube_highlights(team, max_results=5):
    """Searches YouTube for recent highlight videos from the team's official channel."""
    try:
        # Use the raw team name from the request to generate the lookup key
        channel_key = team.lower().replace(' & ', '_').replace(' ', '_')
        logging.info(f"Looking for channel key: '{channel_key}'")

        channel_id = TEAM_CHANNELS.get(channel_key)

        if not channel_id:
            logging.error(f"No channel ID found for key: {channel_key} (Original Team: {team})")
            return {'error': f"No YouTube channel configured for team: {team}"}

        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet", "channelId": channel_id, "q": "highlights | match", "type": "video",
            "maxResults": max_results, "order": "date", "key": API_KEY
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        videos = []
        for item in data.get("items", []):
            videos.append({
                'video_url': f"https://www.youtube.com/embed/{item['id']['videoId']}",
                'title': item['snippet']['title'],
                'date': item['snippet']['publishedAt'].split('T')[0]
            })

        return {'data': videos}
    except Exception as e:
        logging.error(f"Error fetching YouTube highlights for {team}: {e}")
        return {'error': f"Failed to fetch YouTube highlights. Reason: {e}"}


@cached(cache)
def get_fixtures_data(league):
    league_urls = {
        'premier-league': 'https://onefootball.com/en/competition/premier-league-9/fixtures',
        'la-liga': 'https://onefootball.com/en/competition/la-liga-10/fixtures',
        'bundesliga': 'https://onefootball.com/en/competition/bundesliga-1/fixtures'
    }
    try:
        url = league_urls[league]
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        fixtures_data = []
        match_cards = soup.find_all("a", class_="MatchCard_matchCard__iOv4G")

        if not match_cards:
            raise ValueError("Could not find any match cards.")

        for card in match_cards:
            raw_text = card.get_text(separator=" ").strip()
            try:
                parts = raw_text.rsplit(' ', 2)
                if len(parts) < 3:
                    continue

                team_names_raw = parts[0]
                date = parts[1]
                time = parts[2]

                if " vs " in team_names_raw:
                    formatted_teams = team_names_raw
                else:
                    team_words = team_names_raw.split()
                    if len(team_words) >= 2:
                        if "United" in team_names_raw:
                            split_index = team_names_raw.find("United") + len("United")
                            home = team_names_raw[:split_index].strip()
                            away = team_names_raw[split_index:].strip()
                            formatted_teams = f"{home} vs {away}"
                        elif "City" in team_names_raw:
                            split_index = team_names_raw.find("City") + len("City")
                            home = team_names_raw[:split_index].strip()
                            away = team_names_raw[split_index:].strip()
                            formatted_teams = f"{home} vs {away}"
                        elif "Madrid" in team_names_raw:
                            split_index = team_names_raw.find("Madrid") + len("Madrid")
                            home = team_names_raw[:split_index].strip()
                            away = team_names_raw[split_index:].strip()
                            formatted_teams = f"{home} vs {away}"
                        else:
                            formatted_teams = re.sub(r"([a-z])([A-Z])", r"\1 vs \2", team_names_raw)
                    else:
                        formatted_teams = team_names_raw

                home_team = formatted_teams.split(' vs ')[0].strip()
                away_team = formatted_teams.split(' vs ')[1].strip()
                normalized_home_team = normalize_team_name(home_team)
                normalized_away_team = normalize_team_name(away_team)

                fixtures_data.append({
                    'teams': f"{normalized_home_team} vs {normalized_away_team}",
                    'date': f"{date} {time}",
                    'venue': "Venue to be confirmed",
                    'broadcast': "TBD"
                })
            except Exception as e:
                logging.warning(f"Could not parse fixture: {raw_text}. Error: {e}")
                continue

        return {'data': fixtures_data}

    except Exception as e:
        logging.error(f"Error scraping {league} fixtures: {e}")
        return {'error': f"Failed to scrape fixtures data. Reason: {e}"}


@cached(cache)
def get_results_data(league):
    league_urls = {
        'premier-league': 'https://onefootball.com/en/competition/premier-league-9/fixtures',
        'la-liga': 'https://onefootball.com/en/competition/la-liga-10/fixtures',
        'bundesliga': 'https://onefootball.com/en/competition/bundesliga-1/fixtures'
    }
    try:
        url = league_urls[league]
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        results_data = []

        match_cards = soup.find_all("a", class_="MatchCard_matchCard__iOv4G")

        if not match_cards:
            raise ValueError("Could not find any match cards.")

        today = datetime.now()
        date_threshold = today - timedelta(days=7)

        for card in match_cards:
            score_element = card.find("span", class_="MatchCard_score__U7HuZ")
            if not score_element:
                continue

            try:
                date_element = card.find("span", class_="MatchCard_matchTime___f5yW")
                if not date_element:
                    continue

                match_date_str = date_element.text.strip()
                try:
                    match_date = datetime.strptime(match_date_str, "%d/%m/%Y")
                except ValueError:
                    match_date = today

                if match_date < date_threshold:
                    continue

                team_elements = card.find_all("span", class_="MatchCard_teamName__7h4Q2")
                if len(team_elements) != 2:
                    continue

                home_team = team_elements[0].text.strip()
                away_team = team_elements[1].text.strip()
                normalized_home_team = normalize_team_name(home_team)
                normalized_away_team = normalize_team_name(away_team)
                formatted_teams = f"{normalized_home_team} vs {normalized_away_team}"

                score = score_element.text.strip()

                results_data.append({
                    'teams': formatted_teams,
                    'score': score,
                    'date': match_date_str,
                    'venue': "Venue to be confirmed",
                    'broadcast': "TBD"
                })
            except Exception as e:
                logging.warning(f"Could not parse result: {e}")
                continue

        return {'data': results_data}

    except Exception as e:
        logging.error(f"Error scraping {league} results: {e}")
        return {'error': f"Failed to scrape results data. Reason: {e}"}


@cached(cache)
def get_table_data(league):
    league_urls = {
        'premier-league': 'https://onefootball.com/en/competition/premier-league-9/table',
        'la-liga': 'https://onefootball.com/en/competition/la-liga-10/table',
        'bundesliga': 'https://onefootball.com/en/competition/bundesliga-1/table'
    }
    try:
        url = league_urls[league]
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        rows = soup.find_all("li", class_="Standing_standings__row__5sdZG")
        if not rows:
            raise ValueError("Could not find table rows.")

        table_data = []
        season_started = False

        for row in rows:
            team_elem = row.find("p", class_="Standing_standings__teamName__psv61")
            if not team_elem:
                continue

            team_name = team_elem.text.strip()
            normalized_name = normalize_team_name(team_name)

            position_elem = row.find("p", class_="Standing_standings__position__13iT8")
            stats_cells = row.find_all("div", class_="Standing_standings__cell__5Kd0W")

            played = stats_cells[2].text.strip() if len(stats_cells) > 2 else '0'
            if played != '0':
                season_started = True

            table_data.append({
                'position': position_elem.text.strip() if position_elem else '-',
                'team': normalized_name,
                'played': played,
                'wins': stats_cells[3].text.strip() if len(stats_cells) > 3 else '0',
                'draws': stats_cells[4].text.strip() if len(stats_cells) > 4 else '0',
                'losses': stats_cells[5].text.strip() if len(stats_cells) > 5 else '0',
                'goal_difference': stats_cells[6].text.strip() if len(stats_cells) > 6 else '0',
                'points': stats_cells[7].text.strip() if len(stats_cells) > 7 else '0'
            })

        result = {'data': table_data}
        if not season_started and table_data:
            result['status'] = 'The new season hasn\'t started yet. Showing team list.'
        return result

    except Exception as e:
        logging.error(f"Error scraping {league} table: {e}")
        return {'error': f"Failed to scrape table data. Reason: {e}"}


@cached(cache)
def get_teams_data(league):
    try:
        table_data = get_table_data(league)
        if 'error' in table_data:
            return table_data

        teams = [team['team'] for team in table_data['data']]
        return {'data': teams}
    except Exception as e:
        logging.error(f"Error fetching {league} teams: {e}")
        return {'error': f"Failed to fetch teams data. Reason: {e}"}


def get_lineups_data(league, teams, date):
    try:
        home_team, away_team = teams.split(' vs ')
        normalized_home_team = normalize_team_name(home_team)
        normalized_away_team = normalize_team_name(away_team)

        # Mock lineup data (replace with actual scraping/API call if needed)
        home_lineup = [f"{normalized_home_team} Player {i+1}" for i in range(11)]
        away_lineup = [f"{normalized_away_team} Player {i+1}" for i in range(11)]

        return {
            'data': {
                'home_team': home_lineup,
                'away_team': away_lineup
            }
        }
    except Exception as e:
        logging.error(f"Error fetching lineups for {teams}: {e}")
        return {'error': f"Failed to fetch lineup data. Reason: {e}"}


# Placeholder for league-wide highlights (not implemented in your original code)
def get_highlights_data(league):
    return {'data': [], 'error': f"League-wide highlights not implemented for {league}"}


@app.route('/')
def home():
    return render_template('index.html')


# --- Premier League API ---
@app.route('/api/premier-league/table')
def api_premier_league_table():
    return jsonify(get_table_data('premier-league'))


@app.route('/api/premier-league/fixtures')
def api_premier_league_fixtures():
    return jsonify(get_fixtures_data('premier-league'))


@app.route('/api/premier-league/results')
def api_premier_league_results():
    return jsonify(get_results_data('premier-league'))


@app.route('/api/premier-league/teams')
def api_premier_league_teams():
    return jsonify(get_teams_data('premier-league'))


@app.route('/api/premier-league/highlights')
def api_premier_league_highlights():
    return jsonify(get_highlights_data('premier-league'))


@app.route('/api/premier-league/lineups')
def api_premier_league_lineups():
    return jsonify(get_lineups_data('premier-league', request.args.get('teams', ''), request.args.get('date', '')))


@app.route('/api/premier-league/team-highlights')
def api_premier_league_team_highlights():
    team = request.args.get('team', '')
    return jsonify(get_youtube_highlights(team))


# --- La Liga API ---
@app.route('/api/la-liga/table')
def api_la_liga_table():
    return jsonify(get_table_data('la-liga'))


@app.route('/api/la-liga/fixtures')
def api_la_liga_fixtures():
    return jsonify(get_fixtures_data('la-liga'))


@app.route('/api/la-liga/results')
def api_la_liga_results():
    return jsonify(get_results_data('la-liga'))


@app.route('/api/la-liga/teams')
def api_la_liga_teams():
    return jsonify(get_teams_data('la-liga'))


@app.route('/api/la-liga/highlights')
def api_la_liga_highlights():
    return jsonify(get_highlights_data('la-liga'))


@app.route('/api/la-liga/lineups')
def api_la_liga_lineups():
    return jsonify(get_lineups_data('la-liga', request.args.get('teams', ''), request.args.get('date', '')))


@app.route('/api/la-liga/team-highlights')
def api_la_liga_team_highlights():
    team = request.args.get('team', '')
    return jsonify(get_youtube_highlights(team))


# --- Bundesliga API ---
@app.route('/api/bundesliga/table')
def api_bundesliga_table():
    return jsonify(get_table_data('bundesliga'))


@app.route('/api/bundesliga/fixtures')
def api_bundesliga_fixtures():
    return jsonify(get_fixtures_data('bundesliga'))


@app.route('/api/bundesliga/results')
def api_bundesliga_results():
    return jsonify(get_results_data('bundesliga'))


@app.route('/api/bundesliga/teams')
def api_bundesliga_teams():
    return jsonify(get_teams_data('bundesliga'))


@app.route('/api/bundesliga/highlights')
def api_bundesliga_highlights():
    return jsonify(get_highlights_data('bundesliga'))


@app.route('/api/bundesliga/lineups')
def api_bundesliga_lineups():
    return jsonify(get_lineups_data('bundesliga', request.args.get('teams', ''), request.args.get('date', '')))


@app.route('/api/bundesliga/team-highlights')
def api_bundesliga_team_highlights():
    team = request.args.get('team', '')
    return jsonify(get_youtube_highlights(team))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
