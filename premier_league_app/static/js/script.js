// Team logos mapping
const teamLogos = {
    // Premier League
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
    // La Liga
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
    // Bundesliga
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
    // Ligue 1
    "Paris Saint-Germain": "https://images.fotmob.com/image_resources/logo/teamlogo/8636_small.png",
    "Marseille": "https://images.fotmob.com/image_resources/logo/teamlogo/9829_small.png",
    "Lyon": "https://images.fotmob.com/image_resources/logo/teamlogo/9830_small.png",
    "Monaco": "https://images.fotmob.com/image_resources/logo/teamlogo/9831_small.png",
    "Lille": "https://images.fotmob.com/image_resources/logo/teamlogo/9832_small.png",
    // Serie A
    "Inter Milan": "https://images.fotmob.com/image_resources/logo/teamlogo/8637_small.png",
    "AC Milan": "https://images.fotmob.com/image_resources/logo/teamlogo/8635_small.png",
    "Juventus": "https://images.fotmob.com/image_resources/logo/teamlogo/8638_small.png",
    "Roma": "https://images.fotmob.com/image_resources/logo/teamlogo/8681_small.png",
    "Napoli": "https://images.fotmob.com/image_resources/logo/teamlogo/8685_small.png",
    // Champions League
    "Manchester City": "https://images.fotmob.com/image_resources/logo/teamlogo/8456_small.png",
    "Bayern Munich": "https://images.fotmob.com/image_resources/logo/teamlogo/9823_small.png",
    "Real Madrid": "https://images.fotmob.com/image_resources/logo/teamlogo/8633_small.png",
    "Barcelona": "https://images.fotmob.com/image_resources/logo/teamlogo/8634_small.png",
    "PSG": "https://images.fotmob.com/image_resources/logo/teamlogo/8636_small.png",
    "Liverpool": "https://images.fotmob.com/image_resources/logo/teamlogo/8650_small.png"
};

// Stadiums mapping
const STADIUMS = {
    // Premier League
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
    // La Liga
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
    // Bundesliga
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
    // Ligue 1
    "Paris Saint-Germain": "Parc des Princes",
    "Marseille": "Stade Vélodrome",
    "Lyon": "Groupama Stadium",
    "Monaco": "Stade Louis II",
    "Lille": "Stade Pierre-Mauroy",
    // Serie A
    "Inter Milan": "San Siro",
    "AC Milan": "San Siro",
    "Juventus": "Allianz Stadium",
    "Roma": "Stadio Olimpico",
    "Napoli": "Diego Armando Maradona Stadium"
};

// Team facts mapping
const TEAM_FACTS = {
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
    // La Liga
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
    // Bundesliga
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
    // Ligue 1
    "Paris Saint-Germain": "Owned by Qatar Sports Investments since 2011. Dominant force in French football.",
    "Marseille": "Only French club to win Champions League (1993). Fierce rivalry with PSG.",
    "Lyon": "Won 7 consecutive Ligue 1 titles (2002-08). Excellent academy producing Benzema, Lacazette.",
    "Monaco": "Based in tax haven principality. Produced Thierry Henry, Kylian Mbappé.",
    "Lille": "From northern France. Won 2021 Ligue 1 title against PSG's dominance.",
    // Serie A
    "Inter Milan": "Nicknamed 'Nerazzurri' (Black and Blues). Won treble in 2010 under Mourinho.",
    "AC Milan": "Second most Champions League titles (7). 'Rossoneri' (Red and Blacks) nickname.",
    "Juventus": "Most successful Italian club with 36 titles. 'Old Lady' nickname. Black and white stripes.",
    "Roma": "From Italy's capital. 'Giallorossi' (Yellow-Reds) nickname. Passionate fanbase.",
    "Napoli": "From southern Italy. Diego Maradona led them to two titles in 1980s. Play in sky blue.",
    // Champions League
    "Manchester City": "Owned by Abu Dhabi United Group since 2008. Won their first Champions League in 2023.",
    "Bayern Munich": "Most successful German club with 32 league titles. Won six trophies in 2020 under Hansi Flick.",
    "Real Madrid": "Most successful club in Champions League history with 14 titles. Santiago Bernabéu is their iconic stadium.",
    "Barcelona": "Known for 'La Masia' academy producing players like Messi, Xavi, Iniesta. 'Més que un club' motto.",
    "PSG": "Owned by Qatar Sports Investments since 2011. Dominant force in French football.",
    "Liverpool": "Most successful English club in Europe with 6 Champions League titles. 'You'll Never Walk Alone' anthem."
};

// League logos
const leagueLogos = {
    'premier-league': 'https://upload.wikimedia.org/wikipedia/en/f/f2/Premier_League_Logo.svg',
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
    ['premierLeagueDashboard', 'laLigaDashboard', 'bundesligaDashboard', 'highlightsDashboard', 'teamHighlightsDashboard'].forEach(id => {
        const dashboard = document.getElementById(id);
        dashboard.classList.remove('visible');
        setTimeout(() => { dashboard.style.display = 'none'; }, 800);
    });
    document.getElementById('sportsSelection').style.display = 'block';
}

// Show league dashboard
function showLeagueDashboard(leagueId) {
    document.getElementById('sportsSelection').style.display = 'none';
    document.getElementById('highlightsDashboard').style.display = 'none';
    document.getElementById('teamHighlightsDashboard').style.display = 'none';
    const dashboard = document.getElementById(leagueId);
    dashboard.style.display = 'block';
    setTimeout(() => {
        dashboard.classList.add('visible');
        if (leagueId === 'premierLeagueDashboard') loadPremierLeagueData();
        else if (leagueId === 'laLigaDashboard') loadLaLigaData();
        else if (leagueId === 'bundesligaDashboard') loadBundesligaData();
    }, 50);
}

// Show highlights dashboard
function showHighlightsDashboard(league) {
    document.getElementById('sportsSelection').style.display = 'none';
    ['premierLeagueDashboard', 'laLigaDashboard', 'bundesligaDashboard', 'teamHighlightsDashboard'].forEach(id => {
        const dashboard = document.getElementById(id);
        dashboard.classList.remove('visible');
        setTimeout(() => { dashboard.style.display = 'none'; }, 800);
    });
    const highlightsDashboard = document.getElementById('highlightsDashboard');
    highlightsDashboard.style.display = 'block';
    setTimeout(() => {
        highlightsDashboard.classList.add('visible');
        loadHighlights(league);
    }, 50);
}

// Show team highlights dashboard
function showTeamHighlightsDashboard(team, league) {
    document.getElementById('sportsSelection').style.display = 'none';
    ['premierLeagueDashboard', 'laLigaDashboard', 'bundesligaDashboard', 'highlightsDashboard'].forEach(id => {
        const dashboard = document.getElementById(id);
        dashboard.classList.remove('visible');
        setTimeout(() => { dashboard.style.display = 'none'; }, 800);
    });
    const teamHighlightsDashboard = document.getElementById('teamHighlightsDashboard');
    teamHighlightsDashboard.style.display = 'block';
    setTimeout(() => {
        teamHighlightsDashboard.classList.add('visible');
        loadTeamHighlights(team, league);
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
        
        result.data.forEach((team, index) => {
            const row = document.createElement('tr');
            const normalizedTeam = normalizeTeamName(team.team);
            const logo = teamLogos[normalizedTeam] || 'https://via.placeholder.com/25';
            const fact = TEAM_FACTS[normalizedTeam] || 'Interesting facts about this team coming soon';
            
            if (!teamLogos[normalizedTeam]) {
                console.error(`No logo found for team: ${normalizedTeam}`);
            }
            
            row.innerHTML = `
                <td>${team.position}</td>
                <td class="team-cell">
                    <img src="${logo}" alt="${team.team}" class="team-logo" onerror="this.src='https://via.placeholder.com/25';">
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
            row.style.animationDelay = `${index * 0.05}s`;
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
            result.data.forEach((fixture, index) => {
                const fixtureDiv = document.createElement('div');
                fixtureDiv.className = 'fixture';
                const [homeTeam, awayTeam] = fixture.teams.split(' vs ');
                const normalizedHomeTeam = normalizeTeamName(homeTeam);
                const normalizedAwayTeam = normalizeTeamName(awayTeam);
                const homeLogo = teamLogos[normalizedHomeTeam] || 'https://via.placeholder.com/25';
                const awayLogo = teamLogos[normalizedAwayTeam] || 'https://via.placeholder.com/25';
                
                if (!teamLogos[normalizedHomeTeam]) console.error(`No logo for home team: ${normalizedHomeTeam}`);
                if (!teamLogos[normalizedAwayTeam]) console.error(`No logo for away team: ${normalizedAwayTeam}`);
                
                fixtureDiv.innerHTML = `
                    <div class="fixture-teams">
                        <img src="${homeLogo}" alt="${homeTeam}" class="team-logo" onerror="this.src='https://via.placeholder.com/25';">
                        <span>${homeTeam}</span>
                        <span>vs</span>
                        <span>${awayTeam}</span>
                        <img src="${awayLogo}" alt="${awayTeam}" class="team-logo" onerror="this.src='https://via.placeholder.com/25';">
                    </div>
                    <div class="fixture-date">${fixture.date}</div>
                `;
                fixtureDiv.style.animationDelay = `${index * 0.1}s`;
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
            result.data.forEach((result, index) => {
                const resultDiv = document.createElement('div');
                resultDiv.className = 'result';
                const [homeTeam, awayTeam] = result.teams.split(' vs ');
                const normalizedHomeTeam = normalizeTeamName(homeTeam);
                const normalizedAwayTeam = normalizeTeamName(awayTeam);
                const homeLogo = teamLogos[normalizedHomeTeam] || 'https://via.placeholder.com/25';
                const awayLogo = teamLogos[normalizedAwayTeam] || 'https://via.placeholder.com/25';
                
                if (!teamLogos[normalizedHomeTeam]) console.error(`No logo for home team: ${normalizedHomeTeam}`);
                if (!teamLogos[normalizedAwayTeam]) console.error(`No logo for away team: ${normalizedAwayTeam}`);
                
                resultDiv.innerHTML = `
                    <div class="result-teams">
                        <img src="${homeLogo}" alt="${homeTeam}" class="team-logo" onerror="this.src='https://via.placeholder.com/25';">
                        <span>${homeTeam}</span>
                        <span class="result-score">${result.score}</span>
                        <span>${awayTeam}</span>
                        <img src="${awayLogo}" alt="${awayTeam}" class="team-logo" onerror="this.src='https://via.placeholder.com/25';">
                    </div>
                    <div class="result-date">${result.date}</div>
                `;
                resultDiv.style.animationDelay = `${index * 0.1}s`;
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

// Load highlights data
async function loadHighlights(league) {
    const highlightsList = document.getElementById('highlights-list');
    const highlightsLoading = document.getElementById('highlights-loading');
    const highlightsError = document.getElementById('highlights-error');
    const teamGrid = document.getElementById('team-grid');
    
    try {
        highlightsLoading.style.display = 'block';
        highlightsList.innerHTML = '';
        highlightsError.style.display = 'none';
        teamGrid.innerHTML = '';
        
        // Fetch highlights
        const highlightsResponse = await fetch(`/api/${league}/highlights`);
        if (!highlightsResponse.ok) throw new Error(`HTTP error! status: ${highlightsResponse.status}`);
        const highlightsResult = await highlightsResponse.json();
        if (highlightsResult.error) throw new Error(highlightsResult.error);
        
        if (highlightsResult.data.length === 0) {
            highlightsList.innerHTML = '<div class="status">No highlights available.</div>';
        } else {
            highlightsResult.data.forEach((highlight, index) => {
                const videoDiv = document.createElement('div');
                videoDiv.className = 'video-item';
                videoDiv.style.animationDelay = `${index * 0.1}s`;
                videoDiv.innerHTML = `
                    <iframe src="${highlight.video_url}" frameborder="0" allowfullscreen></iframe>
                    <div class="video-info">
                        <h3>${highlight.title}</h3>
                        <p>${highlight.date}</p>
                    </div>
                `;
                highlightsList.appendChild(videoDiv);
            });
        }
        
        // Fetch teams for selector
        const teamsResponse = await fetch(`/api/${league}/teams`);
        if (!teamsResponse.ok) throw new Error(`HTTP error! status: ${teamsResponse.status}`);
        const teamsResult = await teamsResponse.json();
        if (teamsResult.error) throw new Error(teamsResult.error);
        
        teamsResult.data.forEach((team, index) => {
            const normalizedTeam = normalizeTeamName(team);
            const logo = teamLogos[normalizedTeam] || 'https://via.placeholder.com/60';
            const teamDiv = document.createElement('div');
            teamDiv.className = 'team-icon';
            teamDiv.style = `--index: ${index};`;
            teamDiv.innerHTML = `<img src="${logo}" alt="${team}" class="team-icon" onerror="this.src='https://via.placeholder.com/60';">`;
            teamDiv.addEventListener('click', () => showTeamHighlightsDashboard(normalizedTeam, league));
            teamGrid.appendChild(teamDiv);
        });
        
        highlightsLoading.style.display = 'none';
    } catch (error) {
        console.error(`Error loading ${league} highlights:`, error);
        highlightsLoading.style.display = 'none';
        highlightsError.textContent = `Failed to load highlights: ${error.message}`;
        highlightsError.style.display = 'block';
    }
}

// Load team highlights
async function loadTeamHighlights(team, league) {
    const teamLogo = document.getElementById('team-logo');
    const teamName = document.getElementById('team-name');
    const teamNameTagline = document.getElementById('team-name-tagline');
    const featuredVideo = document.getElementById('featured-video');
    const teamHighlightsList = document.getElementById('team-highlights-list');
    const featuredLoading = document.getElementById('featured-video-loading');
    const featuredError = document.getElementById('featured-video-error');
    const highlightsLoading = document.getElementById('team-highlights-loading');
    const highlightsError = document.getElementById('team-highlights-error');
    
    const normalizedTeam = normalizeTeamName(team);
    teamLogo.src = teamLogos[normalizedTeam] || 'https://via.placeholder.com/40';
    teamName.textContent = normalizedTeam;
    teamNameTagline.textContent = normalizedTeam;
    
    try {
        featuredLoading.style.display = 'block';
        highlightsLoading.style.display = 'block';
        featuredVideo.innerHTML = '';
        teamHighlightsList.innerHTML = '';
        featuredError.style.display = 'none';
        highlightsError.style.display = 'none';
        
        const response = await fetch(`/api/${league}/team-highlights?team=${encodeURIComponent(normalizedTeam)}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        
        const result = await response.json();
        if (result.error) throw new Error(result.error);
        
        if (result.data.length === 0) {
            featuredVideo.innerHTML = '<div class="status">No featured video available.</div>';
            teamHighlightsList.innerHTML = '<div class="status">No highlights available.</div>';
        } else {
            const featured = result.data[0];
            featuredVideo.innerHTML = `
                <iframe src="${featured.video_url}" frameborder="0" allowfullscreen></iframe>
            `;
            
            result.data.slice(1).forEach((highlight, index) => {
                const videoDiv = document.createElement('div');
                videoDiv.className = 'video-item';
                videoDiv.style.animationDelay = `${index * 0.1}s`;
                videoDiv.innerHTML = `
                    <iframe src="${highlight.video_url}" frameborder="0" allowfullscreen></iframe>
                    <div class="video-info">
                        <h3>${highlight.title}</h3>
                        <p>${highlight.date}</p>
                    </div>
                `;
                teamHighlightsList.appendChild(videoDiv);
            });
        }
        
        featuredLoading.style.display = 'none';
        highlightsLoading.style.display = 'none';
    } catch (error) {
        console.error(`Error loading highlights for ${normalizedTeam}:`, error);
        featuredLoading.style.display = 'none';
        highlightsLoading.style.display = 'none';
        featuredError.textContent = `Failed to load featured video: ${error.message}`;
        highlightsError.textContent = `Failed to load highlights: ${error.message}`;
        featuredError.style.display = 'block';
        highlightsError.style.display = 'block';
    }
}

// Show fixture details in modal
async function showFixtureDetails(fixture, league) {
    const modal = document.getElementById('fixture-modal');
    const modalContent = document.getElementById('modal-content');
    const [homeTeam, awayTeam] = fixture.teams.split(' vs ');
    const normalizedHomeTeam = normalizeTeamName(homeTeam);
    const normalizedAwayTeam = normalizeTeamName(awayTeam);
    const homeLogo = teamLogos[normalizedHomeTeam] || 'https://via.placeholder.com/25';
    const awayLogo = teamLogos[normalizedAwayTeam] || 'https://via.placeholder.com/25';
    const leagueLogo = leagueLogos[league] || '';
    const homeStadium = STADIUMS[normalizedHomeTeam] || 'TBC';
    const awayStadium = STADIUMS[normalizedAwayTeam] || 'TBC';

    modalContent.innerHTML = `
        <h2>
            <img src="${homeLogo}" alt="${homeTeam}" class="team-logo">
            ${homeTeam} vs ${awayTeam}
            <img src="${awayLogo}" alt="${awayTeam}" class="team-logo">
            ${leagueLogo ? `<img src="${leagueLogo}" alt="${league}" class="league-logo" style="width: 30px; height: 30px;">` : ''}
        </h2>
        <div class="detail-row">
            <span class="detail-icon"><i class="far fa-calendar-alt"></i></span>
            <span class="detail-text"><strong>Date:</strong> ${fixture.date}</span>
        </div>
        <div class="detail-row">
            <span class="detail-icon"><i class="fas fa-map-marker-alt"></i></span>
            <span class="detail-text"><strong>Venue:</strong> ${homeStadium}</span>
        </div>
        ${fixture.score ? `
            <div class="detail-row">
                <span class="detail-icon"><i class="fas fa-futbol"></i></span>
                <span class="detail-text"><strong>Score:</strong> ${fixture.score}</span>
            </div>
        ` : ''}
        <div class="team-lineups">
            <div>
                <h3><img src="${homeLogo}" alt="${homeTeam}" class="team-logo"> ${homeTeam}</h3>
                <ul class="players">
                    <li>Loading lineup...</li>
                </ul>
            </div>
            <div>
                <h3><img src="${awayLogo}" alt="${awayTeam}" class="team-logo"> ${awayTeam}</h3>
                <ul class="players">
                    <li>Loading lineup...</li>
                </ul>
            </div>
        </div>
        <div class="highlights-section">
            <h3>Match Highlights</h3>
            <div class="highlight-placeholder">Video highlights coming soon...</div>
            <button class="team-highlights-btn" onclick="showTeamHighlightsDashboard('${normalizedHomeTeam}', '${league}')">View ${homeTeam} Highlights</button>
            <button class="team-highlights-btn" onclick="showTeamHighlightsDashboard('${normalizedAwayTeam}', '${league}')">View ${awayTeam} Highlights</button>
        </div>
    `;

    modal.style.display = 'block';

    // Fetch lineups
    try {
        const response = await fetch(`/api/${league}/lineups?teams=${encodeURIComponent(fixture.teams)}&date=${encodeURIComponent(fixture.date)}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const result = await response.json();
        if (result.error) throw new Error(result.error);

        const homePlayers = modalContent.querySelector('.team-lineups .players:first-child');
        const awayPlayers = modalContent.querySelector('.team-lineups .players:last-child');

        homePlayers.innerHTML = result.data.home_team.length > 0
            ? result.data.home_team.map((player, index) => `<li style="animation-delay: ${index * 0.05}s">${player}</li>`).join('')
            : '<li>No lineup available</li>';
        awayPlayers.innerHTML = result.data.away_team.length > 0
            ? result.data.away_team.map((player, index) => `<li style="animation-delay: ${index * 0.05}s">${player}</li>`).join('')
            : '<li>No lineup available</li>';
    } catch (error) {
        console.error(`Error loading lineups for ${fixture.teams}:`, error);
        modalContent.querySelectorAll('.players').forEach(players => {
            players.innerHTML = '<li>Failed to load lineup</li>';
        });
    }
}

// Close modal
function closeModal() {
    const modal = document.getElementById('fixture-modal');
    modal.style.display = 'none';
}

// Load Premier League data
function loadPremierLeagueData() {
    loadTable('premier-league', 'pl');
    loadFixtures('premier-league', 'pl');
    loadResults('premier-league', 'pl');
}

// Load La Liga data
function loadLaLigaData() {
    loadTable('la-liga', 'll');
    loadFixtures('la-liga', 'll');
    loadResults('la-liga', 'll');
}

// Load Bundesliga data
function loadBundesligaData() {
    loadTable('bundesliga', 'bl');
    loadFixtures('bundesliga', 'bl');
    loadResults('bundesliga', 'bl');
}

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(hideLoader, 2000);

    // Add click event listeners to sport cards
    document.querySelectorAll('.sport-card').forEach(card => {
        if (!card.classList.contains('disabled')) {
            card.addEventListener('click', () => {
                const league = card.getAttribute('data-sport');
                const dashboardMap = {
                    'premier-league': 'premierLeagueDashboard',
                    'la-liga': 'laLigaDashboard',
                    'bundesliga': 'bundesligaDashboard'
                };
                if (dashboardMap[league]) {
                    showLeagueDashboard(dashboardMap[league]);
                }
            });
        }
    });

    // Add click event listeners to highlights dropdown
    document.querySelectorAll('.dropdown-menu a').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const league = item.getAttribute('data-league');
            showHighlightsDashboard(league);
        });
    });

    // Hamburger menu toggle
    const hamburger = document.querySelector('.hamburger input');
    const navMenu = document.querySelector('.nav-menu');
    hamburger.addEventListener('change', () => {
        navMenu.classList.toggle('active');
    });

    // Theme toggle
    const themeToggle = document.getElementById('toggle');
    themeToggle.addEventListener('change', () => {
        document.body.classList.toggle('light-mode', themeToggle.checked);
        localStorage.setItem('theme', themeToggle.checked ? 'light' : 'dark');
    });
    
    // Load saved theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        themeToggle.checked = true;
        document.body.classList.add('light-mode');
    }
});
