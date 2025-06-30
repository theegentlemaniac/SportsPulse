from flask import Flask, render_template_string, jsonify
import requests
from bs4 import BeautifulSoup
import logging
import re
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# Team logos for all leagues (using fotmob.com for reliability)
TEAM_LOGOS = {
    # Premier League
    "Arsenal": "https://images.fotmob.com/image_resources/logo/teamlogo/9825_small.png",
    "Aston Villa": "https://images.fotmob.com/image_resources/logo/teamlogo/10252_small.png",
    "Bournemouth": "https://images.fotmob.com/image_resources/logo/teamlogo/8678_small.png",
    "Brentford": "https://images.fotmob.com/image_resources/logo/teamlogo/8602_small.png",
    "Brighton & Hove Albion": "https://images.fotmob.com/image_resources/logo/teamlogo/10204_small.png",
    "Chelsea": "https://images.fotmob.com/image_resources/logo/teamlogo/8455_small.png",
    "Crystal Palace": "https://images.fotmob.com/image_resources/logo/teamlogo/9826_small.png",
    "Everton": "https://images.fotmob.com/image_resources/logo/teamlogo/8668_small.png",
    "Fulham": "https://images.fotmob.com/image_resources/logo/teamlogo/9879_small.png",
    "Ipswich Town": "https://images.fotmob.com/image_resources/logo/teamlogo/8657_small.png",
    "Leicester City": "https://images.fotmob.com/image_resources/logo/teamlogo/8197_small.png",
    "Liverpool": "https://images.fotmob.com/image_resources/logo/teamlogo/8650_small.png",
    "Manchester City": "https://images.fotmob.com/image_resources/logo/teamlogo/8456_small.png",
    "Manchester United": "https://images.fotmob.com/image_resources/logo/teamlogo/10260_small.png",
    "Newcastle United": "https://images.fotmob.com/image_resources/logo/teamlogo/10261_small.png",
    "Nottingham Forest": "https://images.fotmob.com/image_resources/logo/teamlogo/10203_small.png",
    "Southampton": "https://images.fotmob.com/image_resources/logo/teamlogo/8466_small.png",
    "Tottenham Hotspur": "https://images.fotmob.com/image_resources/logo/teamlogo/8586_small.png",
    "West Ham United": "https://images.fotmob.com/image_resources/logo/teamlogo/8654_small.png",
    "Wolverhampton Wanderers": "https://images.fotmob.com/image_resources/logo/teamlogo/8603_small.png",
    "Burnley": "https://images.fotmob.com/image_resources/logo/teamlogo/8191_small.png",
    "Sunderland": "https://images.fotmob.com/image_resources/logo/teamlogo/8472_small.png",
    "Leeds United": "https://images.fotmob.com/image_resources/logo/teamlogo/8463_small.png",
    # La Liga
    "Real Madrid": "https://images.fotmob.com/image_resources/logo/teamlogo/8633_small.png",
    "Barcelona": "https://images.fotmob.com/image_resources/logo/teamlogo/8634_small.png",
    "Atlético Madrid": "https://images.fotmob.com/image_resources/logo/teamlogo/9906_small.png",
    "Villarreal": "https://images.fotmob.com/image_resources/logo/teamlogo/10205_small.png",
    "Athletic Bilbao": "https://images.fotmob.com/image_resources/logo/teamlogo/8315_small.png",
    "Real Betis": "https://images.fotmob.com/image_resources/logo/teamlogo/8302_small.png",
    "Osasuna": "https://images.fotmob.com/image_resources/logo/teamlogo/8370_small.png",
    "Valencia": "https://images.fotmob.com/image_resources/logo/teamlogo/10267_small.png",
    "Sevilla": "https://images.fotmob.com/image_resources/logo/teamlogo/9835_small.png",
    "Celta Vigo": "https://images.fotmob.com/image_resources/logo/teamlogo/8388_small.png",
    "Real Sociedad": "https://images.fotmob.com/image_resources/logo/teamlogo/9910_small.png",
    "Girona": "https://images.fotmob.com/image_resources/logo/teamlogo/8384_small.png",
    "Rayo Vallecano": "https://images.fotmob.com/image_resources/logo/teamlogo/8371_small.png",
    "Mallorca": "https://images.fotmob.com/image_resources/logo/teamlogo/8305_small.png",
    "Alavés": "https://images.fotmob.com/image_resources/logo/teamlogo/8311_small.png",
    "Espanyol": "https://images.fotmob.com/image_resources/logo/teamlogo/8396_small.png",
    "Getafe": "https://images.fotmob.com/image_resources/logo/teamlogo/8398_small.png",
    "Real Valladolid": "https://images.fotmob.com/image_resources/logo/teamlogo/8381_small.png",
    "Leganés": "https://images.fotmob.com/image_resources/logo/teamlogo/8402_small.png",
    "Las Palmas": "https://images.fotmob.com/image_resources/logo/teamlogo/8399_small.png",
    # Bundesliga
    "Bayern Munich": "https://images.fotmob.com/image_resources/logo/teamlogo/9823_small.png",
    "Borussia Dortmund": "https://images.fotmob.com/image_resources/logo/teamlogo/9789_small.png",
    "RB Leipzig": "https://images.fotmob.com/image_resources/logo/teamlogo/10147_small.png",
    "Bayer Leverkusen": "https://images.fotmob.com/image_resources/logo/teamlogo/9821_small.png",
    "Eintracht Frankfurt": "https://images.fotmob.com/image_resources/logo/teamlogo/9810_small.png",
    "VfB Stuttgart": "https://images.fotmob.com/image_resources/logo/teamlogo/9816_small.png",
    "Borussia Mönchengladbach": "https://images.fotmob.com/image_resources/logo/teamlogo/9788_small.png",
    "Wolfsburg": "https://images.fotmob.com/image_resources/logo/teamlogo/9817_small.png",
    "Werder Bremen": "https://images.fotmob.com/image_resources/logo/teamlogo/9811_small.png",
    "Freiburg": "https://images.fotmob.com/image_resources/logo/teamlogo/9815_small.png",
    "Augsburg": "https://images.fotmob.com/image_resources/logo/teamlogo/9812_small.png",
    "Hoffenheim": "https://images.fotmob.com/image_resources/logo/teamlogo/10145_small.png",
    "Mainz 05": "https://images.fotmob.com/image_resources/logo/teamlogo/9814_small.png",
    "Union Berlin": "https://images.fotmob.com/image_resources/logo/teamlogo/10146_small.png",
    "Heidenheim": "https://images.fotmob.com/image_resources/logo/teamlogo/10148_small.png",
    "Bochum": "https://images.fotmob.com/image_resources/logo/teamlogo/9813_small.png",
    "St. Pauli": "https://images.fotmob.com/image_resources/logo/teamlogo/9818_small.png",
    "Holstein Kiel": "https://images.fotmob.com/image_resources/logo/teamlogo/10149_small.png",
    # Ligue 1
    "Paris Saint-Germain": "https://images.fotmob.com/image_resources/logo/teamlogo/8636_small.png",
    "Marseille": "https://images.fotmob.com/image_resources/logo/teamlogo/9829_small.png",
    "Lyon": "https://images.fotmob.com/image_resources/logo/teamlogo/9830_small.png",
    "Monaco": "https://images.fotmob.com/image_resources/logo/teamlogo/9831_small.png",
    "Lille": "https://images.fotmob.com/image_resources/logo/teamlogo/9832_small.png",
    # Serie A
    "Inter Milan": "https://images.fotmob.com/image_resources/logo/teamlogo/8637_small.png",
    "AC Milan": "https://images.fotmob.com/image_resources/logo/teamlogo/8635_small.png",
    "Juventus": "https://images.fotmob.com/image_resources/logo/teamlogo/8638_small.png",
    "Roma": "https://images.fotmob.com/image_resources/logo/teamlogo/8681_small.png",
    "Napoli": "https://images.fotmob.com/image_resources/logo/teamlogo/8685_small.png",
    # Champions League
    "Manchester City": "https://images.fotmob.com/image_resources/logo/teamlogo/8456_small.png",
    "Bayern Munich": "https://images.fotmob.com/image_resources/logo/teamlogo/9823_small.png",
    "Real Madrid": "https://images.fotmob.com/image_resources/logo/teamlogo/8633_small.png",
    "Barcelona": "https://images.fotmob.com/image_resources/logo/teamlogo/8634_small.png",
    "PSG": "https://images.fotmob.com/image_resources/logo/teamlogo/8636_small.png",
    "Liverpool": "https://images.fotmob.com/image_resources/logo/teamlogo/8650_small.png"
}

# Stadiums for all leagues
STADIUMS = {
    # Premier League
    "Arsenal": "Emirates Stadium",
    "Aston Villa": "Villa Park",
    "Bournemouth": "Vitality Stadium",
    "Brentford": "Brentford Community Stadium",
    "Brighton & Hove Albion": "Amex Stadium",
    "Chelsea": "Stamford Bridge",
    "Crystal Palace": "Selhurst Park",
    "Everton": "Goodison Park",
    "Fulham": "Craven Cottage",
    "Ipswich Town": "Portman Road",
    "Leicester City": "King Power Stadium",
    "Liverpool": "Anfield",
    "Manchester City": "Etihad Stadium",
    "Manchester United": "Old Trafford",
    "Newcastle United": "St. James' Park",
    "Nottingham Forest": "City Ground",
    "Southampton": "St Mary's Stadium",
    "Tottenham Hotspur": "Tottenham Hotspur Stadium",
    "West Ham United": "London Stadium",
    "Wolverhampton Wanderers": "Molineux Stadium",
    # La Liga
    "Real Madrid": "Santiago Bernabéu",
    "Barcelona": "Camp Nou",
    "Atlético Madrid": "Cívitas Metropolitano",
    "Villarreal": "Estadio de la Cerámica",
    "Athletic Bilbao": "San Mamés",
    "Real Betis": "Benito Villamarín",
    "Osasuna": "El Sadar",
    "Valencia": "Mestalla",
    "Sevilla": "Ramón Sánchez-Pizjuán",
    "Celta Vigo": "Balaídos",
    "Real Sociedad": "Reale Arena",
    "Girona": "Montilivi",
    "Rayo Vallecano": "Vallecas",
    "Mallorca": "Son Moix",
    "Alavés": "Mendizorrotza",
    "Espanyol": "RCDE Stadium",
    "Getafe": "Coliseum Alfonso Pérez",
    "Real Valladolid": "José Zorrilla",
    "Leganés": "Butarque",
    "Las Palmas": "Gran Canaria",
    # Bundesliga
    "Bayern Munich": "Allianz Arena",
    "Borussia Dortmund": "Signal Iduna Park",
    "RB Leipzig": "Red Bull Arena",
    "Bayer Leverkusen": "BayArena",
    "Eintracht Frankfurt": "Deutsche Bank Park",
    "VfB Stuttgart": "Mercedes-Benz Arena",
    "Borussia Mönchengladbach": "Borussia-Park",
    "Wolfsburg": "Volkswagen Arena",
    "Werder Bremen": "Weserstadion",
    "Freiburg": "Europa-Park Stadion",
    "Augsburg": "WWK Arena",
    "Hoffenheim": "PreZero Arena",
    "Mainz 05": "Mewa Arena",
    "Union Berlin": "Stadion An der Alten Försterei",
    "Heidenheim": "Voith-Arena",
    "Bochum": "Vonovia Ruhrstadion",
    "St. Pauli": "Millerntor-Stadion",
    "Holstein Kiel": "Holstein-Stadion",
    # Ligue 1
    "Paris Saint-Germain": "Parc des Princes",
    "Marseille": "Stade Vélodrome",
    "Lyon": "Groupama Stadium",
    "Monaco": "Stade Louis II",
    "Lille": "Stade Pierre-Mauroy",
    # Serie A
    "Inter Milan": "San Siro",
    "AC Milan": "San Siro",
    "Juventus": "Allianz Stadium",
    "Roma": "Stadio Olimpico",
    "Napoli": "Diego Armando Maradona Stadium"
}

# Team interesting facts
TEAM_FACTS = {
    "Arsenal": "Founded in 1886 as Dial Square. Nicknamed 'The Gunners' due to their origins in the Royal Arsenal.",
    "Aston Villa": "One of the oldest clubs in England, founded in 1874. Won the European Cup in 1982.",
    "Bournemouth": "Nicknamed 'The Cherries' due to their cherry-red striped shirts and a cherry orchard near their stadium.",
    "Brentford": "Known as 'The Bees', their stadium is called the 'Hive'. First promoted to Premier League in 2021.",
    "Brighton & Hove Albion": "Nicknamed 'The Seagulls'. Their mascot is Gully the Seagull.",
    "Chelsea": "Founded in 1905. Won their first Champions League in 2012 against Bayern Munich.",
    "Crystal Palace": "Nicknamed 'The Eagles'. Their stadium Selhurst Park has been home since 1924.",
    "Everton": "One of the founding members of the Football League in 1888. Nicknamed 'The Toffees'.",
    "Fulham": "London's oldest professional football club, founded in 1879. Played at Craven Cottage since 1896.",
    "Ipswich Town": "Nicknamed 'The Tractor Boys'. Won the UEFA Cup in 1981 under Bobby Robson.",
    "Leicester City": "Pulled off the greatest sporting upset by winning the 2015-16 Premier League at 5000-1 odds.",
    "Liverpool": "Most successful English club in Europe with 6 Champions League titles. 'You'll Never Walk Alone' anthem.",
    "Manchester City": "Owned by Abu Dhabi United Group since 2008. Won their first Champions League in 2023.",
    "Manchester United": "Most successful English club with 20 league titles. 'The Theatre of Dreams' nickname for Old Trafford.",
    "Newcastle United": "Nicknamed 'The Magpies' due to their black and white stripes. St James' Park is their iconic home.",
    "Nottingham Forest": "Won back-to-back European Cups in 1979 and 1980 under Brian Clough.",
    "Southampton": "Nicknamed 'The Saints'. Produced many England internationals through their academy.",
    "Tottenham Hotspur": "First British club to win a European trophy (1963). 'To Dare is To Do' motto.",
    "West Ham United": "Known as 'The Hammers' or 'The Irons'. Won the World Cup for England in 1966 (3 key players).",
    "Wolverhampton Wanderers": "Nicknamed 'Wolves'. One of the founders of the Football League. Famous for their orange kits in the 1970s.",
    # La Liga
    "Real Madrid": "Most successful club in Champions League history with 14 titles. Santiago Bernabéu is their iconic stadium.",
    "Barcelona": "Known for 'La Masia' academy producing players like Messi, Xavi, Iniesta. 'Més que un club' motto.",
    "Atlético Madrid": "Nicknamed 'Los Colchoneros' (The Mattress Makers) due to their striped kits resembling old-fashioned mattresses.",
    "Villarreal": "Nicknamed 'The Yellow Submarine' due to their yellow kits and a Beatles song played at matches.",
    "Athletic Bilbao": "Unique policy of only fielding players from the Basque region. One of three clubs never relegated from La Liga.",
    "Real Betis": "Based in Seville. Known for passionate fans. Won their only La Liga title in 1935.",
    "Osasuna": "From Pamplona. Name means 'health' in Basque. Known for passionate home support at El Sadar.",
    "Valencia": "Nicknamed 'Los Che'. Mestalla is one of Spain's most atmospheric stadiums.",
    "Sevilla": "Most successful club in Europa League history with 7 titles. Fierce rivalry with Real Betis.",
    "Celta Vigo": "From Galicia. Nicknamed 'Os Celestes' (The Sky Blues). Known for attractive attacking football.",
    "Real Sociedad": "Based in San Sebastián. Won back-to-back La Liga titles in 1981 and 1982.",
    "Girona": "Surprise title challengers in 2023-24. Part of City Football Group. Play in red and white stripes.",
    "Rayo Vallecano": "From Madrid's working-class Vallecas district. Known for left-wing political activism among fans.",
    "Mallorca": "From the Balearic Islands. Won their only major trophy (Copa del Rey) in 2003.",
    "Alavés": "Based in Vitoria-Gasteiz. Reached UEFA Cup final in 2001. Play in blue and white stripes.",
    "Espanyol": "Barcelona's 'other' club. Nicknamed 'Periquitos' (Parakeets) due to their striped kits.",
    "Getafe": "From Madrid's southern suburbs. Known for physical style under José Bordalás.",
    "Real Valladolid": "Owned by Ronaldo Nazário since 2018. Play in purple shirts at José Zorrilla stadium.",
    "Leganés": "From Madrid's southern suburbs. Nicknamed 'Los Pepineros' (The Cucumber Growers).",
    "Las Palmas": "From Canary Islands. Play in yellow and blue. Known for attractive football.",
    # Bundesliga
    "Bayern Munich": "Most successful German club with 32 league titles. Won six trophies in 2020 under Hansi Flick.",
    "Borussia Dortmund": "Famous 'Yellow Wall' at Signal Iduna Park holds 25,000 fans. Won 1997 Champions League.",
    "RB Leipzig": "Founded in 2009. Controversial due to Red Bull ownership. Rapid rise to Bundesliga contention.",
    "Bayer Leverkusen": "Nicknamed 'Neverkusen' for near misses in title races. Sponsored by Bayer pharmaceutical company.",
    "Eintracht Frankfurt": "Won 2022 Europa League. Known for passionate fans and excellent atmosphere.",
    "VfB Stuttgart": "Nicknamed 'Die Schwaben' (The Swabians). Produced players like Sami Khedira and Joshua Kimmich.",
    "Borussia Mönchengladbach": "Successful 1970s team. Known for attacking football. Rivalry with Köln.",
    "Wolfsburg": "Owned by Volkswagen. Won 2009 Bundesliga. Nicknamed 'Die Wölfe' (The Wolves).",
    "Werder Bremen": "From northern Germany. Won 2004 double. Green-white kits. Produced Mesut Özil.",
    "Freiburg": "Known for excellent youth development and eco-friendly stadium with solar panels.",
    "Augsburg": "From Bavaria. Nicknamed 'Fuggerstädter'. Smallest city with a Bundesliga team.",
    "Hoffenheim": "Owned by SAP co-founder Dietmar Hopp. Rapid rise from amateur leagues to Bundesliga.",
    "Mainz 05": "Known for gegenpressing style. Produced Jürgen Klopp as manager.",
    "Union Berlin": "From East Berlin. Known for fan culture and stadium rebuilt by fans. Iron in badge symbolizes resilience.",
    "Heidenheim": "First Bundesliga season in 2023-24. Small-town club with just 25,000 inhabitants.",
    "Bochum": "From the Ruhr. Nicknamed 'Die Unabsteigbaren' (The Unrelegatables) in the 1990s.",
    "St. Pauli": "From Hamburg. Famous for left-wing politics and skull-and-crossbones logo. Cult club worldwide.",
    "Holstein Kiel": "Northernmost Bundesliga club. Nicknamed 'The Storks' due to stork nests near stadium.",
    # Ligue 1
    "Paris Saint-Germain": "Owned by Qatar Sports Investments since 2011. Dominant force in French football.",
    "Marseille": "Only French club to win Champions League (1993). Fierce rivalry with PSG.",
    "Lyon": "Won 7 consecutive Ligue 1 titles (2002-08). Excellent academy producing Benzema, Lacazette.",
    "Monaco": "Based in tax haven principality. Produced Thierry Henry, Kylian Mbappé.",
    "Lille": "From northern France. Won 2021 Ligue 1 title against PSG's dominance.",
    # Serie A
    "Inter Milan": "Nicknamed 'Nerazzurri' (Black and Blues). Won treble in 2010 under Mourinho.",
    "AC Milan": "Second most Champions League titles (7). 'Rossoneri' (Red and Blacks) nickname.",
    "Juventus": "Most successful Italian club with 36 titles. 'Old Lady' nickname. Black and white stripes.",
    "Roma": "From Italy's capital. 'Giallorossi' (Yellow-Reds) nickname. Passionate fanbase.",
    "Napoli": "From southern Italy. Diego Maradona led them to two titles in 1980s. Play in sky blue.",
    # Champions League
    "Manchester City": "Owned by Abu Dhabi United Group since 2008. Won their first Champions League in 2023.",
    "Bayern Munich": "Most successful German club with 32 league titles. Won six trophies in 2020 under Hansi Flick.",
    "Real Madrid": "Most successful club in Champions League history with 14 titles. Santiago Bernabéu is their iconic stadium.",
    "Barcelona": "Known for 'La Masia' academy producing players like Messi, Xavi, Iniesta. 'Més que un club' motto.",
    "PSG": "Owned by Qatar Sports Investments since 2011. Dominant force in French football.",
    "Liverpool": "Most successful English club in Europe with 6 Champions League titles. 'You'll Never Walk Alone' anthem."
}

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

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SportPulse - Your Ultimate Sports Hub</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(-45deg, #0a0a0a, #1a1a2e, #16213e, #0f3460);
            background-size: 400% 400%;
            animation: gradientBG 20s ease infinite;
            min-height: 100vh;
            color: white;
            overflow-x: hidden;
        }
        
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Loader Styles */
        .loader-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(-45deg, #0a0a0a, #1a1a2e, #16213e, #0f3460);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 10000;
            animation: gradientBG 20s ease infinite;
        }
        
        .loader-container.fade-out {
            animation: fadeOut 1s ease forwards;
        }
        
        @keyframes fadeOut {
            to { opacity: 0; visibility: hidden; }
        }

        .ball-loader {
            margin-bottom: 30px;
        }

        @keyframes rotateBall {
            0% { transform: rotateY(0deg) rotateX(0deg) rotateZ(0deg); }
            50% { transform: rotateY(360deg) rotateX(360deg) rotateZ(0deg); }
            100% { transform: rotateY(720deg) rotateX(720deg) rotateZ(360deg); }
        }

        @keyframes bounceBall {
            0% { transform: translateY(-70px) scale(1, 1); }
            15% { transform: translateY(-56px) scale(1, 1); }
            45% { transform: translateY(70px) scale(1, 1); }
            50% { transform: translateY(73.5px) scale(1, 0.92); }
            55% { transform: translateY(70px) scale(1, 0.95); }
            85% { transform: translateY(-56px) scale(1, 1); }
            95% { transform: translateY(-70px) scale(1, 1); }
            100% { transform: translateY(-70px) scale(1, 1); }
        }

        .ball {
            animation: bounceBall 1.2s infinite cubic-bezier(0.42, 0, 0.58, 1);
            border-radius: 50%;
            height: 60px;
            position: relative;
            transform: translateY(-70px);
            transform-style: preserve-3d;
            width: 60px;
            z-index: 1;
        }

        .ball::before {
            background: radial-gradient(circle at 36px 20px, #e94560, #ff6b6b);
            border: 2px solid #333;
            border-radius: 50%;
            content: "";
            height: calc(100% + 6px);
            left: -6px;
            position: absolute;
            top: -3px;
            transform: translateZ(1px);
            width: calc(100% + 6px);
        }

        .ball .inner {
            animation: rotateBall 25s infinite linear;
            border-radius: 50%;
            height: 100%;
            position: absolute;
            transform-style: preserve-3d;
            width: 100%;
        }

        .ball .line::before, .ball .line::after {
            border: 2px solid #333;
            border-radius: 50%;
            content: "";
            height: 99%;
            position: absolute;
            width: 99%;
        }

        .ball .line::before { transform: rotate3d(0, 0, 0, 0); }
        .ball .line::after { transform: rotate3d(1, 0, 0, 90deg); }
        .ball .line--two::before { transform: rotate3d(0, 0, 0, 2deg); }
        .ball .line--two::after { transform: rotate3d(1, 0, 0, 88deg); }

        .ball .oval::before, .ball .oval::after {
            border-top: 4px solid #333;
            border-radius: 50%;
            content: "";
            height: 99%;
            position: absolute;
            width: 99%;
        }

        .ball .oval::before { transform: rotate3d(1, 0, 0, 45deg) translate3d(0, 0, 6px); }
        .ball .oval::after { transform: rotate3d(1, 0, 0, -45deg) translate3d(0, 0, -6px); }
        .ball .oval--two::before { transform: rotate3d(1, 0, 0, 135deg) translate3d(0, 0, -6px); }
        .ball .oval--two::after { transform: rotate3d(1, 0, 0, -135deg) translate3d(0, 0, 6px); }

        @keyframes bounceShadow {
            0% { filter: blur(3px); opacity: 0.6; transform: translateY(73px) scale(0.5, 0.5); }
            45% { filter: blur(1px); opacity: 0.9; transform: translateY(73px) scale(1, 1); }
            55% { filter: blur(1px); opacity: 0.9; transform: translateY(73px) scale(1, 1); }
            100% { filter: blur(3px); opacity: 0.6; transform: translateY(73px) scale(0.5, 0.5); }
        }

        .shadow {
            animation: bounceShadow 1.2s infinite cubic-bezier(0.42, 0, 0.58, 1);
            background: black;
            filter: blur(2px);
            border-radius: 50%;
            height: 6px;
            transform: translateY(73px);
            width: 54px;
        }

        .loader-text {
            font-size: 1.5rem;
            font-weight: 600;
            background: linear-gradient(45deg, #e94560, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 0.7; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.05); }
        }

        /* Main Content Styles */
        .main-content {
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.8s ease;
        }
        
        .main-content.visible {
            opacity: 1;
            transform: translateY(0);
        }

        .container { 
            max-width: 1600px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        
        header {
            text-align: center;
            margin-bottom: 60px;
        }
        
        h1 { 
            font-size: 4rem;
            margin-bottom: 15px;
            background: linear-gradient(45deg, #e94560, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 2px 20px rgba(233, 69, 96, 0.3);
            animation: typeWriter 2s steps(20) forwards;
            white-space: nowrap;
            overflow: hidden;
            display: inline-block;
        }
        
        @keyframes typeWriter {
            from { width: 0; }
            to { width: 100%; }
        }
        
        .tagline {
            font-size: 1.3rem;
            opacity: 0;
            margin-bottom: 30px;
            font-weight: 300;
            animation: slideInTagline 1s ease 2s forwards;
        }
        
        @keyframes slideInTagline {
            from { opacity: 0; transform: translateX(-50px); }
            to { opacity: 0.9; transform: translateX(0); }
        }

        /* Sports Selection */
        .sports-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
            margin-bottom: 50px;
            animation: fadeInUp 1s ease 0.8s both;
        }
        
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .sport-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 25px;
            padding: 40px 30px;
            text-align: center;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 2px solid transparent;
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }
        
        .sport-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left 0.5s;
        }
        
        .sport-card:hover::before {
            left: 100%;
        }
        
        .sport-card:hover {
            transform: translateY(-10px) scale(1.02);
            border-color: rgba(233, 69, 96, 0.5);
            box-shadow: 0 20px 60px rgba(233, 69, 96, 0.3);
        }
        
        .sport-card.active {
            background: rgba(233, 69, 96, 0.2);
            border-color: #e94560;
            transform: scale(1.05);
        }
        
        .sport-card.disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .sport-card.disabled:hover {
            transform: none;
            border-color: transparent;
            box-shadow: none;
        }
        
        .sport-icon {
            width: 50px;
            height: 50px;
            margin-bottom: 20px;
            display: block;
            object-fit: contain;
            transition: all 0.3s ease;
        }
        
        .sport-card:hover .sport-icon {
            transform: scale(1.2) rotate(10deg);
        }
        
        .sport-card h3 {
            font-size: 1.5rem;
            margin-bottom: 10px;
            color: white;
        }
        
        .sport-card p {
            opacity: 0.7;
            font-size: 0.95rem;
        }
        
        .coming-soon {
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 600;
            animation: shimmer 2s infinite;
        }
        
        @keyframes shimmer {
            0%, 100% { opacity: 0.7; }
            50% { opacity: 1; }
        }

        /* League Dashboard */
        .league-dashboard {
            display: none;
            animation: slideIn 0.8s ease;
        }
        
        .league-dashboard.visible {
            display: block;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(30px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        .back-btn {
            background: rgba(255, 255, 255, 0.1);
            border: none;
            color: white;
            padding: 12px 20px;
            border-radius: 25px;
            cursor: pointer;
            margin-bottom: 30px;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }
        
        .back-btn:hover {
            background: rgba(233, 69, 96, 0.3);
            transform: translateX(-5px);
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1.5fr 1fr 1fr;
            gap: 40px;
            margin-bottom: 30px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 25px;
            padding: 35px;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 20px 50px rgba(0,0,0,0.3);
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }
        
        .card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(from 0deg, transparent, rgba(233, 69, 96, 0.1), transparent, rgba(78, 205, 196, 0.1), transparent);
            animation: rotate 8s linear infinite;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .card:hover::before {
            opacity: 1;
        }
        
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .card:hover {
            transform: translateY(-8px);
            box-shadow: 0 30px 70px rgba(233, 69, 96, 0.4);
        }
        
        .card h2 {
            font-size: 1.8rem;
            margin-bottom: 25px;
            color: white;
            display: flex;
            align-items: center;
            gap: 12px;
            padding-bottom: 15px;
            border-bottom: 2px solid rgba(233, 69, 96, 0.3);
            position: relative;
            z-index: 1;
        }
        
        .table-container, .fixtures-container, .results-container {
            position: relative;
            z-index: 1;
        }
        
        .table-container {
            overflow-x: auto;
            border-radius: 15px;
            max-height: 600px;
            overflow-y: auto;
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
            padding: 18px 12px;
            text-align: center;
            position: sticky;
            top: 0;
            z-index: 2;
        }
        
        td {
            padding: 15px 12px;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
            position: relative;
        }
        
        tr:hover {
            background: rgba(233, 69, 96, 0.15);
            transform: scale(1.01);
        }
        
        .team-cell {
            display: flex;
            align-items: center;
            gap: 12px;
            text-align: left !important;
            position: relative;
        }
        
        .team-cell:hover .team-tooltip {
            visibility: visible;
            opacity: 1;
            transform: translateY(0);
        }
        
        .team-tooltip {
            position: absolute;
            left: 50%;
            transform: translateX(-50%) translateY(10px);
            bottom: 100%;
            background: rgba(30, 30, 50, 0.95);
            color: white;
            padding: 15px;
            border-radius: 10px;
            width: 300px;
            font-size: 0.9rem;
            visibility: hidden;
            opacity: 0;
            transition: all 0.3s ease;
            z-index: 10;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(233, 69, 96, 0.3);
            pointer-events: none;
        }
        
        .team-tooltip::after {
            content: '';
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -10px;
            border-width: 10px;
            border-style: solid;
            border-color: rgba(30, 30, 50, 0.95) transparent transparent transparent;
        }
        
        .team-logo {
            width: 28px;
            height: 28px;
            object-fit: contain;
            border-radius: 50%;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }
        
        .fixtures-container, .results-container {
            max-height: 600px;
            overflow-y: auto;
            padding-right: 10px;
        }
        
        .fixture, .result {
            background: rgba(255,255,255,0.06);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.4s ease;
            border-left: 4px solid #e94560;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .result {
            border-left-color: #4ecdc4;
        }
        
        .fixture::before, .result::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left 0.6s ease;
        }
        
        .fixture:hover::before, .result:hover::before {
            left: 100%;
        }
        
        .fixture:hover {
            background: rgba(233, 69, 96, 0.2);
            transform: translateX(8px) scale(1.02);
            border-left-width: 6px;
        }
        
        .result:hover {
            background: rgba(78, 205, 196, 0.2);
            transform: translateX(8px) scale(1.02);
            border-left-width: 6px;
        }
        
        .fixture-teams, .result-teams {
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 600;
            font-size: 1.1rem;
            position: relative;
            z-index: 1;
        }
        
        .fixture-date, .result-date {
            background: rgba(233, 69, 96, 0.3);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            position: relative;
            z-index: 1;
        }
        
        .result-date {
            background: rgba(78, 205, 196, 0.3);
        }
        
        .result-score {
            font-weight: bold;
            margin: 0 10px;
            color: #e94560;
        }
        
        .refresh-btn {
            background: linear-gradient(135deg, #e94560, #ff6b6b);
            color: white;
            border: none;
            padding: 18px 45px;
            border-radius: 30px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            display: block;
            margin: 30px auto 0;
            transition: all 0.4s ease;
            box-shadow: 0 8px 25px rgba(233, 69, 96, 0.4);
            position: relative;
            overflow: hidden;
        }
        
        .refresh-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.6s;
        }
        
        .refresh-btn:hover::before {
            left: 100%;
        }
        
        .refresh-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 35px rgba(233, 69, 96, 0.5);
        }
        
        .loading, .error {
            text-align: center;
            padding: 20px;
            border-radius: 10px;
        }
        
        .loading {
            background: rgba(78, 205, 196, 0.1);
            color: #4ecdc4;
        }
        
        .error {
            background: rgba(231, 76, 60, 0.1);
            color: #e74c3c;
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(8px);
            z-index: 1000;
            animation: fadeIn 0.3s ease;
        }
        
        .modal-content {
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            width: 90%;
            max-width: 600px;
            margin: 5vh auto;
            padding: 35px;
            border-radius: 25px;
            box-shadow: 0 30px 80px rgba(0,0,0,0.6);
            border: 1px solid rgba(255,255,255,0.1);
            position: relative;
            animation: slideUp 0.5s ease;
            max-height: 90vh;
            overflow-y: auto;
        }
        
        @keyframes slideUp {
            from { transform: translateY(100px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .close-modal {
            position: absolute;
            top: 25px;
            right: 25px;
            font-size: 1.8rem;
            cursor: pointer;
            color: rgba(255,255,255,0.5);
            transition: all 0.3s ease;
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
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
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
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .players {
            list-style: none;
        }
        
        .players li {
            padding: 8px 0;
            border-bottom: 1px dashed rgba(255,255,255,0.05);
        }

        .highlights-section {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid rgba(255,255,255,0.1);
        }

        .highlights-section h3 {
            margin-bottom: 15px;
            color: #e94560;
        }

        .highlight-placeholder {
            background: rgba(255,255,255,0.05);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            opacity: 0.7;
        }

        .team-highlights-btn {
            background: rgba(78, 205, 196, 0.2);
            border: none;
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
            margin: 10px 5px;
            transition: all 0.3s ease;
        }

        .team-highlights-btn:hover {
            background: rgba(78, 205, 196, 0.4);
            transform: translateY(-2px);
        }

        @media (max-width: 1400px) {
            .dashboard-grid {
                grid-template-columns: 1.2fr 1fr 1fr;
            }
        }

        @media (max-width: 1200px) {
            .dashboard-grid {
                grid-template-columns: 1fr 1fr;
            }
        }

        @media (max-width: 768px) {
            .dashboard-grid, .sports-grid {
                grid-template-columns: 1fr;
            }
            .card {
                padding: 25px;
            }
            h1 {
                font-size: 2.5rem;
            }
            .modal-content {
                width: 95%;
                margin: 2vh auto;
                padding: 25px;
            }
            .team-lineups {
                grid-template-columns: 1fr;
            }
            .sport-icon {
                width: 40px;
                height: 40px;
            }
            .team-tooltip {
                width: 250px;
                font-size: 0.8rem;
            }
        }
    </style>
</head>
<body>
    <!-- Loader -->
    <div class="loader-container" id="loader">
        <div class="ball-loader">
            <div class="ball">
                <div class="inner">
                    <div class="line"></div>
                    <div class="line line--two"></div>
                    <div class="oval"></div>
                    <div class="oval oval--two"></div>
                </div>
            </div>
            <div class="shadow"></div>
        </div>
        <div class="loader-text">Loading SportPulse...</div>
    </div>

    <!-- Main Content -->
    <div class="main-content" id="mainContent">
        <div class="container">
            <!-- Sports Selection -->
            <div id="sportsSelection">
                <header>
                    <h1><i class="fas fa-trophy"></i> SportPulse</h1>
                    <p class="tagline">Your ultimate destination for real-time sports updates</p>
                </header>
                
                <div class="sports-grid">
                    <div class="sport-card" data-sport="premier-league">
                        <img src="https://www.premierleague.com/resources/rebrand/v7.153.78/i/elements/pl-main-logo.png" alt="Premier League" class="sport-icon">
                        <h3>Premier League</h3>
                        <p>Live scores, tables & fixtures</p>
                    </div>
                    
                    <div class="sport-card" data-sport="la-liga">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/5/54/LaLiga_EA_Sports_2023_Vertical_Logo.svg" alt="La Liga" class="sport-icon">
                        <h3>La Liga</h3>
                        <p>Live scores, tables & fixtures</p>
                    </div>
                    
                    <div class="sport-card" data-sport="bundesliga">
                        <img src="https://upload.wikimedia.org/wikipedia/en/d/df/Bundesliga_logo_%282017%29.svg" alt="Bundesliga" class="sport-icon">
                        <h3>Bundesliga</h3>
                        <p>Live scores, tables & fixtures</p>
                    </div>
                    
                    <div class="sport-card disabled" data-sport="ligue-1">
                        <img src="https://images.fotmob.com/image_resources/logo/leaguelogo/dark/53.png" alt="Ligue 1" class="sport-icon">
                        <h3>Ligue 1</h3>
                        <p class="coming-soon">Coming Soon</p>
                    </div>
                    
                    <div class="sport-card disabled" data-sport="serie-a">
                        <img src="https://images.fotmob.com/image_resources/logo/leaguelogo/dark/55.png" alt="Serie A" class="sport-icon">
                        <h3>Serie A</h3>
                        <p class="coming-soon">Coming Soon</p>
                    </div>
                    
                    <div class="sport-card disabled" data-sport="champions-league">
                        <img src="https://images.fotmob.com/image_resources/logo/leaguelogo/dark/42.png" alt="Champions League" class="sport-icon">
                        <h3>Champions League</h3>
                        <p class="coming-soon">Coming Soon</p>
                    </div>
                    
                    <div class="sport-card disabled" data-sport="nba">
                        <img src="https://cdn.nba.com/logos/leagues/logo-nba.svg" alt="NBA" class="sport-icon">
                        <h3>NBA</h3>
                        <p class="coming-soon">Coming Soon</p>
                    </div>
                    
                    <div class="sport-card disabled" data-sport="f1">
                        <img src="https://www.formula1.com/etc/designs/fom-website/images/f1_logo.svg" alt="Formula 1" class="sport-icon">
                        <h3>Formula 1</h3>
                        <p class="coming-soon">Coming Soon</p>
                    </div>
                </div>
            </div>

            <!-- Premier League Dashboard -->
            <div id="premierLeagueDashboard" class="league-dashboard">
                <button class="back-btn" onclick="showSportsSelection()">
                    <i class="fas fa-arrow-left"></i> Back to Sports
                </button>
                
                <header>
                    <h1><img src="https://www.premierleague.com/resources/rebrand/v7.153.78/i/elements/pl-main-logo.png" alt="Premier League" style="width: 40px; height: 40px; object-fit: contain;"> Premier League</h1>
                    <p class="tagline">Live updates from England's top flight</p>
                </header>
                
                <div class="dashboard-grid">
                    <div class="card">
                        <h2><i class="fas fa-table"></i> League Table</h2>
                        <div id="pl-table-status-container"></div>
                        <div class="table-container">
                            <div id="pl-table-loading" class="loading">Loading table data...</div>
                            <div id="pl-table-error" class="error" style="display: none;"></div>
                            <table id="pl-league-table" style="display: none;">
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
                                <tbody id="pl-table-body"></tbody>
                            </table>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h2><i class="far fa-calendar-alt"></i> Upcoming Fixtures</h2>
                        <div class="fixtures-container">
                            <div id="pl-fixtures-loading" class="loading">Loading fixtures...</div>
                            <div id="pl-fixtures-error" class="error" style="display: none;"></div>
                            <div id="pl-fixtures-list"></div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h2><i class="fas fa-history"></i> Recent Results</h2>
                        <div class="results-container">
                            <div id="pl-results-loading" class="loading">Loading results...</div>
                            <div id="pl-results-error" class="error" style="display: none;"></div>
                            <div id="pl-results-list"></div>
                        </div>
                    </div>
                </div>
                
                <button class="refresh-btn" onclick="loadPremierLeagueData()">
                    <i class="fas fa-sync-alt"></i> Refresh Data
                </button>
            </div>

            <!-- La Liga Dashboard -->
            <div id="laLigaDashboard" class="league-dashboard">
                <button class="back-btn" onclick="showSportsSelection()">
                    <i class="fas fa-arrow-left"></i> Back to Sports
                </button>
                
                <header>
                    <h1><img src="https://upload.wikimedia.org/wikipedia/commons/5/54/LaLiga_EA_Sports_2023_Vertical_Logo.svg" alt="La Liga" style="width: 40px; height: 40px; object-fit: contain;"> La Liga</h1>
                    <p class="tagline">Live updates from Spain's top flight</p>
                </header>
                
                <div class="dashboard-grid">
                    <div class="card">
                        <h2><i class="fas fa-table"></i> League Table</h2>
                        <div id="ll-table-status-container"></div>
                        <div class="table-container">
                            <div id="ll-table-loading" class="loading">Loading table data...</div>
                            <div id="ll-table-error" class="error" style="display: none;"></div>
                            <table id="ll-league-table" style="display: none;">
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
                                <tbody id="ll-table-body"></tbody>
                            </table>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h2><i class="far fa-calendar-alt"></i> Upcoming Fixtures</h2>
                        <div class="fixtures-container">
                            <div id="ll-fixtures-loading" class="loading">Loading fixtures...</div>
                            <div id="ll-fixtures-error" class="error" style="display: none;"></div>
                            <div id="ll-fixtures-list"></div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h2><i class="fas fa-history"></i> Recent Results</h2>
                        <div class="results-container">
                            <div id="ll-results-loading" class="loading">Loading results...</div>
                            <div id="ll-results-error" class="error" style="display: none;"></div>
                            <div id="ll-results-list"></div>
                        </div>
                    </div>
                </div>
                
                <button class="refresh-btn" onclick="loadLaLigaData()">
                    <i class="fas fa-sync-alt"></i> Refresh Data
                </button>
            </div>

            <!-- Bundesliga Dashboard -->
            <div id="bundesligaDashboard" class="league-dashboard">
                <button class="back-btn" onclick="showSportsSelection()">
                    <i class="fas fa-arrow-left"></i> Back to Sports
                </button>
                
                <header>
                    <h1><img src="https://www.bundesliga.com/assets/logo-bundesliga.svg" alt="Bundesliga" style="width: 40px; height: 40px; object-fit: contain;"> Bundesliga</h1>
                    <p class="tagline">Live updates from Germany's top flight</p>
                </header>
                
                <div class="dashboard-grid">
                    <div class="card">
                        <h2><i class="fas fa-table"></i> League Table</h2>
                        <div id="bl-table-status-container"></div>
                        <div class="table-container">
                            <div id="bl-table-loading" class="loading">Loading table data...</div>
                            <div id="bl-table-error" class="error" style="display: none;"></div>
                            <table id="bl-league-table" style="display: none;">
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
                                <tbody id="bl-table-body"></tbody>
                            </table>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h2><i class="far fa-calendar-alt"></i> Upcoming Fixtures</h2>
                        <div class="fixtures-container">
                            <div id="bl-fixtures-loading" class="loading">Loading fixtures...</div>
                            <div id="bl-fixtures-error" class="error" style="display: none;"></div>
                            <div id="bl-fixtures-list"></div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h2><i class="fas fa-history"></i> Recent Results</h2>
                        <div class="results-container">
                            <div id="bl-results-loading" class="loading">Loading results...</div>
                            <div id="bl-results-error" class="error" style="display: none;"></div>
                            <div id="bl-results-list"></div>
                        </div>
                    </div>
                </div>
                
                <button class="refresh-btn" onclick="loadBundesligaData()">
                    <i class="fas fa-sync-alt"></i> Refresh Data
                </button>
            </div>
        </div>
    </div>

    <!-- Fixture Modal -->
    <div id="fixture-modal" class="modal">
        <div class="modal-content">
            <span class="close-modal" onclick="closeModal()">×</span>
            <div class="fixture-details" id="modal-content">
                <!-- Dynamic content will be inserted here -->
            </div>
        </div>
    </div>

    <script>
        // Team logos mapping
        const teamLogos = {{ team_logos|tojson }};

        // Stadiums mapping
        const STADIUMS = {{ stadiums|tojson }};

        // Team facts mapping
        const TEAM_FACTS = {{ team_facts|tojson }};

        // League logos
        const leagueLogos = {
            'premier-league': 'https://resources.premierleague.com/premierleague/badges/logo.png',
            'la-liga': 'https://www.laliga.com/assets/logo-laliga-blanco.svg',
            'bundesliga': 'https://www.bundesliga.com/assets/logo-bundesliga.svg'
        };

        // Function to normalize team names with debug
        function normalizeTeamName(teamName) {
            const nameMap = {
                'Brighton': 'Brighton & Hove Albion',
                'Newcastle': 'Newcastle United',
                'West Ham': 'West Ham United',
                'Wolves': 'Wolverhampton Wanderers',
                'Spurs': 'Tottenham Hotspur',
                'Tottenham': 'Tottenham Hotspur',
                'Ipswich': 'Ipswich Town',
                'Leicester': 'Leicester City',
                'Atletico Madrid': 'Atlético Madrid',
                'Athletic Club': 'Athletic Bilbao',
                'Betis': 'Real Betis',
                'Sociedad': 'Real Sociedad',
                'Valladolid': 'Real Valladolid',
                'Dortmund': 'Borussia Dortmund',
                'Mönchengladbach': 'Borussia Mönchengladbach',
                'Leverkusen': 'Bayer Leverkusen',
                'Frankfurt': 'Eintracht Frankfurt',
                'Stuttgart': 'VfB Stuttgart',
                'Mainz': 'Mainz 05',
                'AFC Bournemouth': 'Bournemouth',
                'Burnley': 'Burnley',
                'Leeds': 'Leeds United',
                'Liverpool': 'Liverpool',
                'Liverpool FC': 'Liverpool',
                'Man City': 'Manchester City',
                'Man United': 'Manchester United',
                'Ath Madrid': 'Atlético Madrid',
                'PSG': 'Paris Saint-Germain',
                'Inter': 'Inter Milan',
                'Milan': 'AC Milan'
            };
            const normalized = nameMap[teamName] || teamName;
            console.log(`Normalizing "${teamName}" to "${normalized}"`);
            return normalized;
        }

        // Loader control
        function hideLoader() {
            const loader = document.getElementById('loader');
            loader.classList.add('fade-out');
            setTimeout(() => {
                loader.style.display = 'none';
                document.getElementById('mainContent').classList.add('visible');
            }, 1000);
        }

        // Show sports selection
        function showSportsSelection() {
            ['premierLeagueDashboard', 'laLigaDashboard', 'bundesligaDashboard'].forEach(id => {
                const dashboard = document.getElementById(id);
                dashboard.classList.remove('visible');
                setTimeout(() => { dashboard.style.display = 'none'; }, 800);
            });
            document.getElementById('sportsSelection').style.display = 'block';
        }

        // Show league dashboard
        function showLeagueDashboard(leagueId) {
            document.getElementById('sportsSelection').style.display = 'none';
            document.getElementById(leagueId).style.display = 'block';
            setTimeout(() => {
                document.getElementById(leagueId).classList.add('visible');
                if (leagueId === 'premierLeagueDashboard') loadPremierLeagueData();
                else if (leagueId === 'laLigaDashboard') loadLaLigaData();
                else if (leagueId === 'bundesligaDashboard') loadBundesligaData();
            }, 50);
        }

        // Load league table data with debug
        async function loadTable(league, prefix) {
            const tableBody = document.getElementById(`${prefix}-table-body`);
            const tableLoading = document.getElementById(`${prefix}-table-loading`);
            const tableError = document.getElementById(`${prefix}-table-error`);
            const table = document.getElementById(`${prefix}-league-table`);
            const statusContainer = document.getElementById(`${prefix}-table-status-container`);
            
            try {
                tableLoading.style.display = 'block';
                table.style.display = 'none';
                tableError.style.display = 'none';
                
                const response = await fetch(`/api/${league}/table`);
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
                    const normalizedTeam = normalizeTeamName(team.team);
                    const logo = teamLogos[normalizedTeam];
                    const fact = TEAM_FACTS[normalizedTeam] || 'Interesting facts about this team coming soon';
                    
                    if (!logo) {
                        console.error(`No logo found for team: ${normalizedTeam}`);
                    }
                    
                    row.innerHTML = `
                        <td>${team.position}</td>
                        <td class="team-cell">
                            <img src="${logo}" alt="${team.team}" class="team-logo" onerror="this.onerror=null;this.src='https://via.placeholder.com/25';">
                            ${team.team}
                            <div class="team-tooltip">
                                <strong>${team.team}</strong>
                                <p>${fact}</p>
                            </div>
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
                console.error(`Error loading ${league} table:`, error);
                tableLoading.style.display = 'none';
                tableError.textContent = `Failed to load table data: ${error.message}`;
                tableError.style.display = 'block';
            }
        }

        // Load fixtures data with debug
        async function loadFixtures(league, prefix) {
            const fixturesList = document.getElementById(`${prefix}-fixtures-list`);
            const fixturesLoading = document.getElementById(`${prefix}-fixtures-loading`);
            const fixturesError = document.getElementById(`${prefix}-fixtures-error`);
            
            try {
                fixturesLoading.style.display = 'block';
                fixturesList.innerHTML = '';
                fixturesError.style.display = 'none';
                
                const response = await fetch(`/api/${league}/fixtures`);
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                
                const result = await response.json();
                if (result.error) throw new Error(result.error);
                
                if (result.data.length === 0) {
                    fixturesList.innerHTML = '<div class="status">No upcoming fixtures found.</div>';
                } else {
                    result.data.forEach(fixture => {
                        const fixtureDiv = document.createElement('div');
                        fixtureDiv.className = 'fixture';
                        const [homeTeam, awayTeam] = fixture.teams.split(' vs ');
                        const normalizedHomeTeam = normalizeTeamName(homeTeam);
                        const normalizedAwayTeam = normalizeTeamName(awayTeam);
                        const homeLogo = teamLogos[normalizedHomeTeam];
                        const awayLogo = teamLogos[normalizedAwayTeam];
                        
                        if (!homeLogo) console.error(`No logo for home team: ${normalizedHomeTeam}`);
                        if (!awayLogo) console.error(`No logo for away team: ${normalizedAwayTeam}`);
                        
                        fixtureDiv.innerHTML = `
                            <div class="fixture-teams">
                                <img src="${homeLogo}" alt="${homeTeam}" class="team-logo" onerror="this.onerror=null;this.src='https://via.placeholder.com/25';">
                                <span>${homeTeam}</span>
                                <span>vs</span>
                                <span>${awayTeam}</span>
                                <img src="${awayLogo}" alt="${awayTeam}" class="team-logo" onerror="this.onerror=null;this.src='https://via.placeholder.com/25';">
                            </div>
                            <div class="fixture-date">${fixture.date}</div>
                        `;
                        fixtureDiv.addEventListener('click', () => showFixtureDetails(fixture, league));
                        fixturesList.appendChild(fixtureDiv);
                    });
                }
                
                fixturesLoading.style.display = 'none';
            } catch (error) {
                console.error(`Error loading ${league} fixtures:`, error);
                fixturesLoading.style.display = 'none';
                fixturesError.textContent = `Failed to load fixtures: ${error.message}`;
                fixturesError.style.display = 'block';
            }
        }

        // Load results data with debug
        async function loadResults(league, prefix) {
            const resultsList = document.getElementById(`${prefix}-results-list`);
            const resultsLoading = document.getElementById(`${prefix}-results-loading`);
            const resultsError = document.getElementById(`${prefix}-results-error`);
            
            try {
                resultsLoading.style.display = 'block';
                resultsList.innerHTML = '';
                resultsError.style.display = 'none';
                
                const response = await fetch(`/api/${league}/results`);
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                
                const result = await response.json();
                if (result.error) throw new Error(result.error);
                
                if (result.data.length === 0) {
                    resultsList.innerHTML = '<div class="status">No recent results found.</div>';
                } else {
                    result.data.forEach(result => {
                        const resultDiv = document.createElement('div');
                        resultDiv.className = 'result';
                        const [homeTeam, awayTeam] = result.teams.split(' vs ');
                        const normalizedHomeTeam = normalizeTeamName(homeTeam);
                        const normalizedAwayTeam = normalizeTeamName(awayTeam);
                        const homeLogo = teamLogos[normalizedHomeTeam];
                        const awayLogo = teamLogos[normalizedAwayTeam];
                        
                        if (!homeLogo) console.error(`No logo for home team: ${normalizedHomeTeam}`);
                        if (!awayLogo) console.error(`No logo for away team: ${normalizedAwayTeam}`);
                        
                        resultDiv.innerHTML = `
                            <div class="result-teams">
                                <img src="${homeLogo}" alt="${homeTeam}" class="team-logo" onerror="this.onerror=null;this.src='https://via.placeholder.com/25';">
                                <span>${homeTeam}</span>
                                <span class="result-score">${result.score}</span>
                                <span>${awayTeam}</span>
                                <img src="${awayLogo}" alt="${awayTeam}" class="team-logo" onerror="this.onerror=null;this.src='https://via.placeholder.com/25';">
                            </div>
                            <div class="result-date">${result.date}</div>
                        `;
                        resultDiv.addEventListener('click', () => showFixtureDetails(result, league));
                        resultsList.appendChild(resultDiv);
                    });
                }
                
                resultsLoading.style.display = 'none';
            } catch (error) {
                console.error(`Error loading ${league} results:`, error);
                resultsLoading.style.display = 'none';
                resultsError.textContent = `Failed to load results: ${error.message}`;
                resultsError.style.display = 'block';
            }
        }

        // Show fixture details in modal with debug
        function showFixtureDetails(fixture, league) {
            const modal = document.getElementById('fixture-modal');
            const modalContent = document.getElementById('modal-content');
            
            const [homeTeam, awayTeam] = fixture.teams.split(' vs ');
            const normalizedHomeTeam = normalizeTeamName(homeTeam);
            const normalizedAwayTeam = normalizeTeamName(awayTeam);
            const homeLogo = teamLogos[normalizedHomeTeam];
            const awayLogo = teamLogos[normalizedAwayTeam];
            const venue = STADIUMS[normalizedHomeTeam] || 'Venue to be confirmed';
            const leagueLogo = leagueLogos[league];
            
            modalContent.innerHTML = `
                <h2>
                    <img src="${homeLogo}" class="team-logo" onerror="this.onerror=null;this.src='https://via.placeholder.com/25';">${homeTeam} vs ${awayTeam}<img src="${awayLogo}" class="team-logo" onerror="this.onerror=null;this.src='https://via.placeholder.com/25';">
                </h2>
                <div style="text-align: center; margin-bottom: 20px;">
                    <img src="${leagueLogo}" alt="${league}" style="width: 40px; height: 40px; object-fit: contain;">
                </div>
                
                <div class="detail-row">
                    <div class="detail-icon"><i class="far fa-calendar"></i></div>
                    <div class="detail-text">${fixture.date}</div>
                </div>
                
                ${fixture.score ? `
                <div class="detail-row">
                    <div class="detail-icon"><i class="fas fa-futbol"></i></div>
                    <div class="detail-text">Final Score: <strong>${fixture.score}</strong></div>
                </div>
                ` : ''}
                
                <div class="detail-row">
                    <div class="detail-icon"><i class="fas fa-map-marker-alt"></i></div>
                    <div class="detail-text">${venue}</div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-icon"><i class="fas fa-tv"></i></div>
                    <div class="detail-text">${fixture.broadcast || 'Broadcast information not available'}</div>
                </div>
                
                <div class="team-lineups">
                    <div>
                        <h3>
                            <img src="${homeLogo}" class="team-logo" onerror="this.onerror=null;this.src='https://via.placeholder.com/25';">${homeTeam}
                        </h3>
                        <ul class="players">
                            <li>Starting XI loading...</li>
                        </ul>
                    </div>
                    <div>
                        <h3>
                            <img src="${awayLogo}" class="team-logo" onerror="this.onerror=null;this.src='https://via.placeholder.com/25';">${awayTeam}
                        </h3>
                        <ul class="players">
                            <li>Starting XI loading...</li>
                        </ul>
                    </div>
                </div>
                
                <div class="highlights-section">
                    <h3>Match Highlights</h3>
                    <div class="highlight-placeholder">Match highlights coming soon</div>
                    <h3>Team Highlights</h3>
                    <button class="team-highlights-btn" onclick="alert('View recent ${homeTeam} highlights coming soon!')">
                        View ${homeTeam} Highlights
                    </button>
                    <button class="team-highlights-btn" onclick="alert('View recent ${awayTeam} highlights coming soon!')">
                        View ${awayTeam} Highlights
                    </button>
                </div>
                
                <div class="detail-row" style="margin-top: 20px;">
                    <div class="detail-icon"><i class="fas fa-info-circle"></i></div>
                    <div class="detail-text">Click outside to close</div>
                </div>
            `;
            
            modal.style.display = 'block';
            
            // Simulate loading lineups
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

        // Close modal
        function closeModal() {
            document.getElementById('fixture-modal').style.display = 'none';
        }

        // Load league data
        function loadPremierLeagueData() {
            loadTable('premier-league', 'pl');
            loadFixtures('premier-league', 'pl');
            loadResults('premier-league', 'pl');
        }

        function loadLaLigaData() {
            loadTable('la-liga', 'll');
            loadFixtures('la-liga', 'll');
            loadResults('la-liga', 'll');
        }

        function loadBundesligaData() {
            loadTable('bundesliga', 'bl');
            loadFixtures('bundesliga', 'bl');
            loadResults('bundesliga', 'bl');
        }

        // Event listeners
        document.querySelectorAll('.sport-card').forEach(card => {
            card.addEventListener('click', () => {
                const sport = card.dataset.sport;
                if (!card.classList.contains('disabled')) {
                    if (sport === 'premier-league') showLeagueDashboard('premierLeagueDashboard');
                    else if (sport === 'la-liga') showLeagueDashboard('laLigaDashboard');
                    else if (sport === 'bundesliga') showLeagueDashboard('bundesligaDashboard');
                }
            });
        });

        window.addEventListener('click', (event) => {
            const modal = document.getElementById('fixture-modal');
            if (event.target === modal) {
                closeModal();
            }
        });

        // Initial load
        window.addEventListener('load', () => {
            setTimeout(hideLoader, 2000); // Show loader for 2 seconds
        });
    </script>
</body>
</html>
'''

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
                
                # Improved team name parsing
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
                venue = STADIUMS.get(normalized_home_team, "Venue to be confirmed")
                
                fixtures_data.append({
                    'teams': formatted_teams,
                    'date': f"{date} {time}",
                    'venue': venue,
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
        
        # Find completed matches (they have a score)
        match_cards = soup.find_all("a", class_="MatchCard_matchCard__iOv4G")
        
        if not match_cards:
            raise ValueError("Could not find any match cards.")
        
        # Get the current date to filter recent results (last 7 days)
        today = datetime.now()
        date_threshold = today - timedelta(days=7)
        
        for card in match_cards:
            # Check if the match has a score (completed match)
            score_element = card.find("span", class_="MatchCard_score__U7HuZ")
            if not score_element:
                continue
                
            try:
                # Get the match date
                date_element = card.find("span", class_="MatchCard_matchTime___f5yW")
                if not date_element:
                    continue
                    
                match_date_str = date_element.text.strip()
                match_date = datetime.strptime(match_date_str, "%d/%m/%Y") if "/" in match_date_str else today
                
                # Skip if the match is too old
                if match_date < date_threshold:
                    continue
                
                # Get team names
                team_elements = card.find_all("span", class_="MatchCard_teamName__7h4Q2")
                if len(team_elements) != 2:
                    continue
                    
                home_team = team_elements[0].text.strip()
                away_team = team_elements[1].text.strip()
                formatted_teams = f"{home_team} vs {away_team}"
                
                # Get the score
                score = score_element.text.strip()
                
                normalized_home_team = normalize_team_name(home_team)
                venue = STADIUMS.get(normalized_home_team, "Venue to be confirmed")
                
                results_data.append({
                    'teams': formatted_teams,
                    'score': score,
                    'date': match_date_str,
                    'venue': venue,
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
                'logo': TEAM_LOGOS.get(normalized_name, ""),
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

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, team_logos=TEAM_LOGOS, stadiums=STADIUMS, team_facts=TEAM_FACTS)

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
