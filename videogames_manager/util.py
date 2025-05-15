import requests, concurrent.futures
from datetime import datetime, timezone
from .models import Games_Data, Record_Calendar, Games_Genres, Games_Platforms
from django.core.cache import cache

current_year = datetime.now().year
current_year_records = Record_Calendar.objects.filter(year=current_year)

def get_igdb_data():
    cached_data = cache.get('game_events')
    if cached_data:
        return cached_data
    
    if current_year_records.exists():
        events = []
        print("current_year_records found")

        games_data = Games_Data.objects.filter(record_year__year=current_year)
        for game in games_data:
            event = {
                "id": game.id,
                "title": game.name,
                "start": game.release_date,
                "url": game.cover_id,
                "summary": game.summary,
                "genre": [genre.name for genre in game.genres.all()],
            }
            events.append(event)
        print(len(events))
        
        cache.set('game_events', {"game_events": events}, timeout=60*60) 
        return {
            "game_events": events
        }
        
    else:
        print("no record found")

        url= "https://api.igdb.com/v4/games"
        headers = {
            "Client-ID": "i1oxiuababx6gze33atxdjv6tlclnw",
            "Authorization": get_acess_token()
        }

        data_list = []
        for month in range(1, 13):
            data = f"""fields name, release_dates.date, summary, storyline, genres.name, platforms.name, status, franchises.name, cover.image_id, release_dates.updated_at; 
            where release_dates.y = {current_year} & release_dates.m = {month} & release_dates.platform = 6;
            sort release_dates.date desc;
            limit 300;
            """
            data_list.append(data)

        futures = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in range(0, len(data_list), 4):
                batch = data_list[i:i+4]
                for data in batch:
                    futures.append(executor.submit(requests.post, url, headers=headers, data=data))
                concurrent.futures.wait(futures)
                
        responses = [future.result() for future in futures]

        unique_titles = set()
        games_stored = []
        
        for response in responses:
            for game in response.json():
                if game['name'] not in unique_titles:
                    unique_titles.add(game['name'])
        
                if "release_dates" in game:
                    for release_date in game['release_dates']:
                        new_updated_at = release_date['updated_at']
                        
                        if new_updated_at:
                            new_updated_at = datetime.fromtimestamp(new_updated_at, timezone.utc).strftime('%Y-%m-%d')
                            record, created = Record_Calendar.objects.get_or_create(year=current_year)
                            record.updated_at = new_updated_at
                            record.save()

                if game['release_dates']:
                    latest_date = max((read for read in game['release_dates'] if 'date' in read), key=lambda x: x['date'])['date']
                    latest_date_iso = datetime.fromtimestamp(latest_date, timezone.utc).strftime('%Y-%m-%d')
                        
                games_stored.append(Games_Data(
                    name=game['name'],
                    summary=game.get('summary', 'No summary avaible'),
                    storyline= game.get('storyline', 'No storyline avaible'),
                    release_date=latest_date_iso,
                    cover_id= game['cover']['image_id'] if "cover" in game else "https://www.freeiconspng.com/thumbs/no-image-icon/no-image-icon-6.png",
                    updated_at = record,
                    record_year= record
                ))    

        Games_Data.objects.bulk_create(games_stored)

        platform_cache = {}
        genre_cache = {}

        for response in responses:
            for game in response.json():            
                spec_game = Games_Data.objects.filter(name=game["name"]).first()

                if "platforms" in game:
                    platforms = []
                    for platform in game["platforms"]:
                        if platform["name"] not in platform_cache:
                            platform_cache[platform["name"]] = Games_Platforms.objects.get_or_create(name=platform["name"])[0]
                        platforms.append(platform_cache[platform["name"]])
                    spec_game.platform.set(platforms)

                if "genres" in game:
                    genres = []
                    for genre in game["genres"]:
                        if genre["name"] not in genre_cache:
                            genre_cache[genre["name"]] = Games_Genres.objects.get_or_create(name=genre["name"])[0]
                        genres.append(genre_cache[genre["name"]])
                    spec_game.genres.set(genres)
        
        events = Games_Data.objects.filter(record_year__year=current_year)
        game_events = []
        for game in events:
            event = {
                "id": game.id,
                "title": game.name,
                "start": game.release_date,
                "url": game.cover_id,
                "summary": game.summary,
                "genre": [genre.name for genre in game.genres.all()],
            }
            game_events.append(event)  
       
        print(len(events))
        return {
            "game_events": game_events
        }
    
def get_acess_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": "i1oxiuababx6gze33atxdjv6tlclnw",
        "client_secret": "j5ip40eiracc8qi1pwr68pplxv9jve",
        "grant_type": "client_credentials"
    }
    
    response = requests.post(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return f"Bearer {data.get('access_token')}"
    else:
        print("Error:", response.status_code)

def html_signup(username, activate_url):
    return f"""
            <html>
            <head>
            <style>
            .retro-style {{
                font-family: 'Trebuchet MS', sans-serif;
                background-color: #333;
                color: #fff;
                border: 2px solid #ffcc00;
                padding: 10px;
                font-size: 13px;
                box-shadow: 0 4px #ff9900;
                transition: transform 0.2s, box-shadow 0.2s;
                text-align: center;
            }}
            .retro-style a {{
            color: #333;
            text-decoration: none;
            }}
            .retro-style a:hover {{
                color: #ff9900;
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #ffcc00;
                color: #333;
                border: none;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
                font-size: 13px;
                text-transform: uppercase;
                box-shadow: 0 4px #ff9900;
                transition: transform 0.2s, box-shadow 0.2s;
                cursor: pointer;
            }}
            .button:hover {{
                background-color: #ff9900;
                box-shadow: 0 4px #cc7a00;
            }}
            </style>
            </head>
            <body>
           <div class="retro-style">
            <h1 style="font-size: 24px; color: #ffcc00;">Hello, {username}!</h1>
            <h2 style="font-size: 20px; margin-bottom: 20px; color: #ffcc00;">Welcome to Videogame Release Manager!</h2>
            <h4 style="font-size: 16px; margin-bottom: 20px; color: #ffcc00;">Please confirm your email by clicking the button below:</h4>
            <p><a href="{activate_url}" class="button">Confirm Email</a></p>
            </div>
            </body>
            </html>
            """