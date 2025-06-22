from flask import Flask, render_template_string, jsonify
import requests
from bs4 import BeautifulSoup
import logging
import re

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SportPulse - Premier League Dashboard</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(-45deg, #1a1a2e, #16213e, #0f3460, #4a6fa5);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            min-height: 100vh;
            color: white;
        }
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .container { 
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        header {
            text-align: center;
            margin-bottom: 40px;
            animation: fadeIn 1s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        h1 { 
            font-size: 3rem;
            margin-bottom: 10px;
            background: linear-gradient(to right, #e94560, #ff6b6b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        .tagline {
            font-size: 1.2rem;
            opacity: 0.8;
            margin-bottom: 20px;
        }
        .dashboard {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        .card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 30px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            animation: cardGlow 8s infinite alternate;
        }
        @keyframes cardGlow {
            0% { box-shadow: 0 0 20px rgba(233, 69, 96, 0.3); }
            50% { box-shadow: 0 0 40px rgba(233, 69, 96, 0.5); }
            100% { box-shadow: 0 0 20px rgba(233, 69, 96, 0.3); }
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(233, 69, 96, 0.4);
        }
        .card h2 {
            font-size: 1.8rem;
            margin-bottom: 25px;
            color: white;
            display: flex;
            align-items: center;
            gap: 10px;
            padding-bottom: 15px;
            border-bottom: 2px solid rgba(233, 69, 96, 0.5);
        }
        .table-container {
            overflow-x: auto;
            border-radius: 10px;
        }
        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
        }
        th {
            background: linear-gradient(135deg, #e94560, #ff6b6b);
            color: white;
            font-weight: 600;
            padding: 15px;
            text-align: center;
            position: sticky;
            top: 0;
        }
        td {
            padding: 12px 15px;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        tr:hover {
            background: rgba(233, 69, 96, 0.1);
        }
        .team-cell {
            display: flex;
            align-items: center;
            gap: 10px;
            text-align: left !important;
        }
        .team-logo {
            width: 25px;
            height: 25px;
            object-fit: contain;
        }
        .fixtures-container {
            max-height: 600px;
            overflow-y: auto;
            padding-right: 10px;
        }
        .fixture {
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
            border-left: 4px solid #e94560;
            cursor: pointer;
        }
        .fixture:hover {
            background: rgba(233, 69, 96, 0.2);
            transform: translateX(5px);
        }
        .fixture-teams {
            font-weight: 600;
            font-size: 1.1rem;
        }
        .fixture-date {
            background: rgba(233, 69, 96, 0.3);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.9rem;
        }
        .refresh-btn {
            background: linear-gradient(135deg, #e94560, #ff6b6b);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 30px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            display: block;
            margin: 30px auto 0;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(233, 69, 96, 0.3);
        }
        .refresh-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(233, 69, 96, 0.4);
        }
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(5px);
            z-index: 1000;
            animation: fadeIn 0.3s ease;
        }
        .modal-content {
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            width: 90%;
            max-width: 500px;
            margin: 10vh auto;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.1);
            position: relative;
            animation: slideUp 0.4s ease;
        }
        @keyframes slideUp {
            from { transform: translateY(50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        .close-modal {
            position: absolute;
            top: 20px;
            right: 20px;
            font-size: 1.5rem;
            cursor: pointer;
            color: rgba(255,255,255,0.5);
            transition: all 0.2s ease;
        }
        .close-modal:hover {
            color: #e94560;
            transform: rotate(90deg);
        }
        .fixture-details h2 {
            margin-bottom: 20px;
            color: white;
            font-size: 1.8rem;
            text-align: center;
        }
        .detail-row {
            display: flex;
            margin-bottom: 15px;
            align-items: center;
        }
        .detail-icon {
            width: 30px;
            text-align: center;
            margin-right: 15px;
            color: #e94560;
        }
        .detail-text {
            flex: 1;
        }
        .team-lineups {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 30px;
        }
        .team-lineups h3 {
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .players {
            list-style: none;
        }
        .players li {
            padding: 8px 0;
            border-bottom: 1px dashed rgba(255,255,255,0.05);
        }
        @media (max-width: 768px) {
            .dashboard {
                grid-template-columns: 1fr;
            }
            .card {
                padding: 20px;
            }
            h1 {
                font-size: 2.2rem;
            }
            .modal-content {
                width: 95%;
                margin: 5vh auto;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1><i class="fas fa-futbol"></i> SportPulse</h1>
            <p class="tagline">Your premier source for real-time football updates</p>
        </header>
        
        <div class="dashboard">
            <div class="card">
                <h2><i class="fas fa-table"></i> League Table</h2>
                <div id="table-status-container"></div>
                <div class="table-container">
                    <div id="table-loading" class="loading">Loading table data...</div>
                    <div id="table-error" class="error" style="display: none;"></div>
                    <table id="league-table" style="display: none;">
                        <thead>
                            <tr>
                                <th>Pos</th>
                                <th>Team</th>
                                <th>P</th>
                                <th>W</th>
                                <th>D</th>
                                <th>L</th>
                                <th>GD</th>
                                <th>Pts</th>
                            </tr>
                        </thead>
                        <tbody id="table-body"></tbody>
                    </table>
                </div>
            </div>
            
            <div class="card">
                <h2><i class="far fa-calendar-alt"></i> Upcoming Fixtures</h2>
                <div class="fixtures-container">
                    <div id="fixtures-loading" class="loading">Loading fixtures...</div>
                    <div id="fixtures-error" class="error" style="display: none;"></div>
                    <div id="fixtures-list"></div>
                </div>
            </div>
        </div>
        
        <button class="refresh-btn" onclick="loadData()">
            <i class="fas fa-sync-alt"></i> Refresh Data
        </button>
    </div>
    
    <div id="fixture-modal" class="modal">
        <div class="modal-content">
            <span class="close-modal" onclick="closeModal()">&times;</span>
            <div class="fixture-details" id="modal-content">
                <!-- Dynamic content will be inserted here -->
            </div>
        </div>
    </div>

    <script>
        // Team logos mapping
        const teamLogos = {
            "Arsenal": "https://resources.premierleague.com/premierleague/badges/25/t3.png",
            "Aston Villa": "https://resources.premierleague.com/premierleague/badges/25/t7.png",
            "Bournemouth": "https://resources.premierleague.com/premierleague/badges/25/t91.png",
            "Brentford": "https://resources.premierleague.com/premierleague/badges/25/t94.png",
            "Brighton": "https://resources.premierleague.com/premierleague/badges/25/t36.png",
            "Burnley": "https://resources.premierleague.com/premierleague/badges/25/t90.png",
            "Chelsea": "https://resources.premierleague.com/premierleague/badges/25/t8.png",
            "Crystal Palace": "https://resources.premierleague.com/premierleague/badges/25/t31.png",
            "Everton": "https://resources.premierleague.com/premierleague/badges/25/t11.png",
            "Fulham": "https://resources.premierleague.com/premierleague/badges/25/t54.png",
            "Liverpool": "https://resources.premierleague.com/premierleague/badges/25/t14.png",
            "Luton Town": "https://resources.premierleague.com/premierleague/badges/25/t102.png",
            "Manchester City": "https://resources.premierleague.com/premierleague/badges/25/t43.png",
            "Manchester United": "https://resources.premierleague.com/premierleague/badges/25/t1.png",
            "Newcastle": "https://resources.premierleague.com/premierleague/badges/25/t4.png",
            "Nottingham Forest": "https://resources.premierleague.com/premierleague/badges/25/t17.png",
            "Sheffield United": "https://resources.premierleague.com/premierleague/badges/25/t49.png",
            "Tottenham": "https://resources.premierleague.com/premierleague/badges/25/t6.png",
            "West Ham": "https://resources.premierleague.com/premierleague/badges/25/t21.png",
            "Wolves": "https://resources.premierleague.com/premierleague/badges/25/t39.png"
        };

        async function loadTable() {
            const tableBody = document.getElementById('table-body');
            const tableLoading = document.getElementById('table-loading');
            const tableError = document.getElementById('table-error');
            const table = document.getElementById('league-table');
            const statusContainer = document.getElementById('table-status-container');
            
            try {
                tableLoading.style.display = 'block';
                table.style.display = 'none';
                tableError.style.display = 'none';
                
                const response = await fetch('/api/table');
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                
                const result = await response.json();
                if (result.error) throw new Error(result.error);
                
                tableBody.innerHTML = '';
                statusContainer.innerHTML = '';
                
                if (result.status) {
                    const statusDiv = document.createElement('div');
                    statusDiv.className = 'status';
                    statusDiv.textContent = result.status;
                    statusContainer.appendChild(statusDiv);
                }
                
                result.data.forEach(team => {
                    const row = document.createElement('tr');
                    const logo = teamLogos[team.team] || 'https://via.placeholder.com/25';
                    row.innerHTML = `
                        <td>${team.position}</td>
                        <td class="team-cell">
                            <img src="${logo}" alt="${team.team}" class="team-logo">
                            ${team.team}
                        </td>
                        <td>${team.played}</td>
                        <td>${team.wins}</td>
                        <td>${team.draws}</td>
                        <td>${team.losses}</td>
                        <td>${team.goal_difference}</td>
                        <td>${team.points}</td>
                    `;
                    tableBody.appendChild(row);
                });
                
                tableLoading.style.display = 'none';
                table.style.display = 'table';
            } catch (error) {
                console.error('Error loading table:', error);
                tableLoading.style.display = 'none';
                tableError.textContent = `Failed to load table data: ${error.message}`;
                tableError.style.display = 'block';
            }
        }

        async function loadFixtures() {
            const fixturesList = document.getElementById('fixtures-list');
            const fixturesLoading = document.getElementById('fixtures-loading');
            const fixturesError = document.getElementById('fixtures-error');
            
            try {
                fixturesLoading.style.display = 'block';
                fixturesList.innerHTML = '';
                fixturesError.style.display = 'none';
                
                const response = await fetch('/api/fixtures');
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                
                const result = await response.json();
                if (result.error) throw new Error(result.error);
                
                if (result.data.length === 0) {
                    fixturesList.innerHTML = '<div class="status">No upcoming fixtures found.</div>';
                } else {
                    result.data.forEach(fixture => {
                        const fixtureDiv = document.createElement('div');
                        fixtureDiv.className = 'fixture';
                        fixtureDiv.innerHTML = `
                            <div class="fixture-teams">${fixture.teams}</div>
                            <div class="fixture-date">${fixture.date}</div>
                        `;
                        fixtureDiv.addEventListener('click', () => showFixtureDetails(fixture));
                        fixturesList.appendChild(fixtureDiv);
                    });
                }
                
                fixturesLoading.style.display = 'none';
            } catch (error) {
                console.error('Error loading fixtures:', error);
                fixturesLoading.style.display = 'none';
                fixturesError.textContent = `Failed to load fixtures: ${error.message}`;
                fixturesError.style.display = 'block';
            }
        }

        function showFixtureDetails(fixture) {
            const modal = document.getElementById('fixture-modal');
            const modalContent = document.getElementById('modal-content');
            
            // Split teams for lineups
            const [homeTeam, awayTeam] = fixture.teams.split(' vs ');
            
            modalContent.innerHTML = `
                <h2>${fixture.teams}</h2>
                
                <div class="detail-row">
                    <div class="detail-icon"><i class="far fa-calendar"></i></div>
                    <div class="detail-text">${fixture.date}</div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-icon"><i class="fas fa-map-marker-alt"></i></div>
                    <div class="detail-text">${fixture.venue || 'Venue to be confirmed'}</div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-icon"><i class="fas fa-tv"></i></div>
                    <div class="detail-text">${fixture.broadcast || 'Broadcast information not available'}</div>
                </div>
                
                <div class="team-lineups">
                    <div>
                        <h3>${homeTeam}</h3>
                        <ul class="players">
                            <li>Starting XI loading...</li>
                        </ul>
                    </div>
                    <div>
                        <h3>${awayTeam}</h3>
                        <ul class="players">
                            <li>Starting XI loading...</li>
                        </ul>
                    </div>
                </div>
                
                <div class="detail-row" style="margin-top: 20px;">
                    <div class="detail-icon"><i class="fas fa-info-circle"></i></div>
                    <div class="detail-text">Click outside to close</div>
                </div>
            `;
            
            modal.style.display = 'block';
            
            // Simulate loading lineups (in a real app, you'd fetch this from an API)
            setTimeout(() => {
                const homePlayers = modalContent.querySelectorAll('.players')[0];
                const awayPlayers = modalContent.querySelectorAll('.players')[1];
                
                homePlayers.innerHTML = `
                    <li>Goalkeeper</li>
                    <li>Defender 1</li>
                    <li>Defender 2</li>
                    <li>Defender 3</li>
                    <li>Defender 4</li>
                    <li>Midfielder 1</li>
                    <li>Midfielder 2</li>
                    <li>Midfielder 3</li>
                    <li>Forward 1</li>
                    <li>Forward 2</li>
                    <li>Forward 3</li>
                `;
                
                awayPlayers.innerHTML = `
                    <li>Goalkeeper</li>
                    <li>Defender 1</li>
                    <li>Defender 2</li>
                    <li>Defender 3</li>
                    <li>Defender 4</li>
                    <li>Midfielder 1</li>
                    <li>Midfielder 2</li>
                    <li>Midfielder 3</li>
                    <li>Forward 1</li>
                    <li>Forward 2</li>
                    <li>Forward 3</li>
                `;
            }, 1000);
        }

        function closeModal() {
            document.getElementById('fixture-modal').style.display = 'none';
        }

        function loadData() {
            loadTable();
            loadFixtures();
        }

        // Close modal when clicking outside
        window.addEventListener('click', (event) => {
            const modal = document.getElementById('fixture-modal');
            if (event.target === modal) {
                closeModal();
            }
        });

        // Initial load
        window.addEventListener('load', loadData);
    </script>
</body>
</html>
'''

# Premier League team logos
TEAM_LOGOS = {
    "Arsenal": "https://resources.premierleague.com/premierleague/badges/25/t3.png",
    "Aston Villa": "https://resources.premierleague.com/premierleague/badges/25/t7.png",
    "Bournemouth": "https://resources.premierleague.com/premierleague/badges/25/t91.png",
    "Brentford": "https://resources.premierleague.com/premierleague/badges/25/t94.png",
    "Brighton": "https://resources.premierleague.com/premierleague/badges/25/t36.png",
    "Burnley": "https://resources.premierleague.com/premierleague/badges/25/t90.png",
    "Chelsea": "https://resources.premierleague.com/premierleague/badges/25/t8.png",
    "Crystal Palace": "https://resources.premierleague.com/premierleague/badges/25/t31.png",
    "Everton": "https://resources.premierleague.com/premierleague/badges/25/t11.png",
    "Fulham": "https://resources.premierleague.com/premierleague/badges/25/t54.png",
    "Liverpool": "https://resources.premierleague.com/premierleague/badges/25/t14.png",
    "Luton Town": "https://resources.premierleague.com/premierleague/badges/25/t102.png",
    "Manchester City": "https://resources.premierleague.com/premierleague/badges/25/t43.png",
    "Manchester United": "https://resources.premierleague.com/premierleague/badges/25/t1.png",
    "Newcastle": "https://resources.premierleague.com/premierleague/badges/25/t4.png",
    "Nottingham Forest": "https://resources.premierleague.com/premierleague/badges/25/t17.png",
    "Sheffield United": "https://resources.premierleague.com/premierleague/badges/25/t49.png",
    "Tottenham": "https://resources.premierleague.com/premierleague/badges/25/t6.png",
    "West Ham": "https://resources.premierleague.com/premierleague/badges/25/t21.png",
    "Wolves": "https://resources.premierleague.com/premierleague/badges/25/t39.png"
}

def get_table_data():
    try:
        url = "https://onefootball.com/en/competition/premier-league-9/table"
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
            position_elem = row.find("p", class_="Standing_standings__position__13iT8")
            stats_cells = row.find_all("div", class_="Standing_standings__cell__5Kd0W")
            
            played = stats_cells[2].text.strip() if len(stats_cells) > 2 else '0'
            if played != '0':
                season_started = True
                
            table_data.append({
                'position': position_elem.text.strip() if position_elem else '-',
                'team': team_name,
                'logo': TEAM_LOGOS.get(team_name, ""),
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
        logging.error(f"Error scraping table: {e}")
        return {'error': f"Failed to scrape table data. Reason: {e}"}

def get_fixtures_data():
    try:
        url = "https://onefootball.com/en/competition/premier-league-9/fixtures"
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
                
                # Improved team name parsing (Python version)
                if " vs " in team_names_raw:
                    formatted_teams = team_names_raw
                else:
                    team_words = team_names_raw.split()
                    if len(team_words) >= 2:
                        # Look for common team name patterns
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
                        else:
                            # Fallback - split at last capital letter
                            formatted_teams = re.sub(r"([a-z])([A-Z])", r"\1 vs \2", team_names_raw)
                    else:
                        formatted_teams = team_names_raw
                
                fixtures_data.append({
                    'teams': formatted_teams,
                    'date': f"{date} {time}",
                    'venue': "TBD",
                    'broadcast': "TBD"
                })
            except Exception as e:
                logging.warning(f"Could not parse fixture: {raw_text}. Error: {e}")
                continue
                
        return {'data': fixtures_data}
        
    except Exception as e:
        logging.error(f"Error scraping fixtures: {e}")
        return {'error': f"Failed to scrape fixtures data. Reason: {e}"}

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/table')
def api_table():
    data = get_table_data()
    return jsonify(data)

@app.route('/api/fixtures')
def api_fixtures():
    data = get_fixtures_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)