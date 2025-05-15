from django.core.management.base import BaseCommand
from videogames_manager.models import User
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from datetime import datetime
from django.conf import settings
from videogames_manager.util import get_acess_token
import requests, concurrent.futures
from datetime import datetime, timezone
from videogames_manager.models import Games_Data, Record_Calendar, Games_Genres, Games_Platforms

class Command(BaseCommand):

    help = 'Update the Database'

    def handle(self, *args, **kwargs):
        time = datetime.now()
        if time.day == 1:
            current_month = datetime.now().month
            users = User.objects.all()
            for user in users:
                games = user.followed_games.filter(release_date__month=current_month).order_by('release_date')

                try: 
                    email_subject = "Monthly Game Updates"
                    email_body = f"{user.username},\n\nHere are the games you're following that are releasing this month:\n"
                    for game in games:
                        email_body += f"\n{game.name} on {game.release_date}\n"
                    email_body += "\nBest regards,\nYour Videogame Release Manager"

                    html_message = f"""
                    <html>
                    <head>
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
                    body {{
                        font-family: 'Press Start 2P', sans-serif;
                        color: #000; /* White text */
                    }}
                    .container {{
                        padding: 20px;
                        margin: 20px auto;
                        border: 2px solid #ffcc00; /* Yellow border */
                        border-radius: 10px;
                        max-width: 600px;
                    }}
                    h1 {{
                        color: #ffcc00; /* Yellow text */
                    }}
                    ul {{
                        list-style-type: none;
                        padding: 0;
                        color: #fff;
                    }}
                    li {{
                        background: #555; /* Darker background for list items */
                        margin: 5px 0;
                        padding: 10px;
                        border-radius: 5px;
                        border: 1px solid #ffcc00; /* Yellow border for list items */
                    }}
                    </style>
                    </head>
                    <body>
                    <div class="container">
                    <h1>Hello, {user.username}!</h1>
                    <p>Here are the games you're following that are releasing this month:</p>
                    <ul>
                    """
                    if games:
                        for game in games:
                            html_message += f"<li>{game.name} on {game.release_date}</li>"
                    else:
                        html_message += "<li>No games that you are following releases this month, try looking for some games!</li>"
                    html_message += """
                    </ul>
                    <p>Best regards,<br>Your Videogame Release Manager</p>
                    </div>
                    </body>
                    </html>
                    """
                    
                    send_mail(
                        email_subject,
                        email_body,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False,
                        html_message=html_message,
                    )

                except BadHeaderError:
                    return HttpResponse("Invalid header found.")

        url= "https://api.igdb.com/v4/games"
        headers = {
            "Client-ID": "i1oxiuababx6gze33atxdjv6tlclnw",
            "Authorization": get_acess_token()
        }

        current_year = datetime.now().year
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
        games_data = []
        for response in responses:
            for game in response.json():
                if game['name'] not in unique_titles:
                    unique_titles.add(game['name'])
                    games_data.append(game)

        for game in games_data:
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

                    if record.updated_at is None or record.updated_at != new_updated_at:
                        record.updated_at = new_updated_at
                        record.save()

                    existing_game = Games_Data.objects.filter(name=game['name']).first()

                    if existing_game:
                        
                        if existing_game.updated_at and str(existing_game.updated_at.updated_at) == new_updated_at:
                            continue

                        elif existing_game.updated_at and str(existing_game.updated_at.updated_at) != new_updated_at:
                            existing_game.summary = game.get('summary', 'No summary avaible')
                            existing_game.storyline = game.get('storyline', 'No storyline avaible')
                            existing_game.release_date = latest_date_iso
                            existing_game.cover_id = game['cover']['image_id'] if "cover" in game else "https://www.freeiconspng.com/thumbs/no-image-icon/no-image-icon-6.png"
                            existing_game.updated_at.updated_at = new_updated_at
                            existing_game.updated_at.save()
                            existing_game.save()

                            if "platforms" in game:
                                platforms = []
                                for platform_dict in game['platforms']:
                                    platform_name = platform_dict['name']
                                    platform, created = Games_Platforms.objects.get_or_create(name=platform_name)
                                    platforms.append(platform)
                                existing_game.platform.set(platforms)

                            if "genres" in game:
                                genres = []
                                for genre_dict in game['genres']:
                                    genre_name = genre_dict['name']
                                    genre, created = Games_Genres.objects.get_or_create(name=genre_name)
                                    genres.append(genre)
                                existing_game.genres.set(genres)
                        
                    else:       
                            new_game = Games_Data.objects.create(
                                name=game['name'],
                                summary=game.get('summary', 'No summary avaible'),
                                storyline= game.get('storyline', 'No storyline avaible'),
                                release_date=latest_date_iso,
                                cover_id= game['cover']['image_id'] if "cover" in game else "https://www.freeiconspng.com/thumbs/no-image-icon/no-image-icon-6.png",
                                updated_at = record,
                                record_year= record
                            )

                            if "platforms" in game:
                                platforms = []
                                for platform_dict in game['platforms']:
                                    platform_name = platform_dict['name']
                                    platform, created = Games_Platforms.objects.get_or_create(name=platform_name)
                                    platforms.append(platform)
                                new_game.platform.set(platforms)

                            if "genres" in game:
                                genres = []
                                for genre_dict in game['genres']:
                                    genre_name = genre_dict['name']
                                    genre, created = Games_Genres.objects.get_or_create(name=genre_name)
                                    genres.append(genre)
                                new_game.genres.set(genres)