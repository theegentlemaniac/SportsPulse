from flask import Flask, jsonify, request, render_template
import requests
from bs4 import BeautifulSoup
import logging
import re
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

def normalize_team_name(team_name):
    """Normalize team names to match logo dictionary keys"""
    name_mapping = {
        "Brighton": "Brighton & Hove Albion",
        "Newcastle": "Newcastle United",
        "West Ham": "West Ham United",
        "Wolves": "Wolverhampton Wanderers",
        "Spurs": "Tottenham Hotspur",
        "Tottenham": "Tottenham Hotspur",
        "Ipswich": "Ipswich Town",
        "Leicester": "Leicester City",
        "Atletico Madrid": "Atlético Madrid",
        "Athletic Club": "Athletic Bilbao",
        "Betis": "Real Betis",
        "Sociedad": "Real Sociedad",
        "Valladolid": "Real Valladolid",
        "Dortmund": "Borussia Dortmund",
        "Mönchengladbach": "Borussia Mönchengladbach",
        "Leverkusen": "Bayer Leverkusen",
        "Frankfurt": "Eintracht Frankfurt",
        "Stuttgart": "VfB Stuttgart",
        "Mainz": "Mainz 05",
        "AFC Bournemouth": "Bournemouth",
        "Burnley": "Burnley",
        "Leeds": "Leeds United",
        "Liverpool": "Liverpool",
        "Liverpool FC": "Liverpool",
        "Man City": "Manchester City",
        "Man United": "Manchester United",
        "Ath Madrid": "Atlético Madrid",
        "PSG": "Paris Saint-Germain",
        "Inter": "Inter Milan",
        "Milan": "AC Milan"
    }
    return name_mapping.get(team_name.strip(), team_name.strip())

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
                normalized_home_team = normalize_team_name(home_team)
                
                fixtures_data.append({
                    'teams': formatted_teams,
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
                match_date = datetime.strptime(match_date_str, "%d/%m/%Y") if "/" in match_date_str else today
                
                if match_date < date_threshold:
                    continue
                
                team_elements = card.find_all("span", class_="MatchCard_teamName__7h4Q2")
                if len(team_elements) != 2:
                    continue
                    
                home_team = team_elements[0].text.strip()
                away_team = team_elements[1].text.strip()
                formatted_teams = f"{home_team} vs {away_team}"
                
                score = score_element.text.strip()
                
                normalized_home_team = normalize_team_name(home_team)
                
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
                'team': team_name,
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

def get_lineups_data(league, teams, date):
    try:
        home_team, away_team = teams.split(' vs ')
        return {
            'data': {
                'home_team': ['Player 1', 'Player 2', 'Player 3'],
                'away_team': ['Player A', 'Player B', 'Player C']
            }
        }
    except Exception as e:
        logging.error(f"Error fetching lineups for {teams}: {e}")
        return {'error': f"Failed to fetch lineup data. Reason: {e}"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/premier-league/table')
def api_premier_league_table():
    data = get_table_data('premier-league')
    return jsonify(data)

@app.route('/api/premier-league/fixtures')
def api_premier_league_fixtures():
    data = get_fixtures_data('premier-league')
    return jsonify(data)

@app.route('/api/premier-league/results')
def api_premier_league_results():
    data = get_results_data('premier-league')
    return jsonify(data)

@app.route('/api/premier-league/lineups')
def api_premier_league_lineups():
    teams = request.args.get('teams', '')
    date = request.args.get('date', '')
    data = get_lineups_data('premier-league', teams, date)
    return jsonify(data)

@app.route('/api/la-liga/table')
def api_la_liga_table():
    data = get_table_data('la-liga')
    return jsonify(data)

@app.route('/api/la-liga/fixtures')
def api_la_liga_fixtures():
    data = get_fixtures_data('la-liga')
    return jsonify(data)

@app.route('/api/la-liga/results')
def api_la_liga_results():
    data = get_results_data('la-liga')
    return jsonify(data)

@app.route('/api/la-liga/lineups')
def api_la_liga_lineups():
    teams = request.args.get('teams', '')
    date = request.args.get('date', '')
    data = get_lineups_data('la-liga', teams, date)
    return jsonify(data)

@app.route('/api/bundesliga/table')
def api_bundesliga_table():
    data = get_table_data('bundesliga')
    return jsonify(data)

@app.route('/api/bundesliga/fixtures')
def api_bundesliga_fixtures():
    data = get_fixtures_data('bundesliga')
    return jsonify(data)

@app.route('/api/bundesliga/results')
def api_bundesliga_results():
    data = get_results_data('bundesliga')
    return jsonify(data)

@app.route('/api/bundesliga/lineups')
def api_bundesliga_lineups():
    teams = request.args.get('teams', '')
    date = request.args.get('date', '')
    data = get_lineups_data('bundesliga', teams, date)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)