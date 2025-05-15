"""
Project: Videogame Release Manager 

Default Filter:
    Release date: This year
    Platform: PC
    Genres: (All genres)
    Popularity type: popscore1 (need another endpoint)

Optional Filters:
    Release date: This year
    Platform: PC, Switch
    Genres: Adventure, Indie, Platform, Role-playing (RPG), Turn-based strategy (TBS), Tactical, Card & Board Game, Hack and slash/Beat 'em up, Strategy, Puzzle 

Also include videogames events!
Include webhook too!

Project's Objective:
    1. User login and Auth: django-allauth X(Funcional, pero falta retocar para ponerlo bonito)

    2. View videogame releases from all the months year in pc (5396 Games)(FullCalendar) X
        2.1. Be able to see (500 games)X 262 Games per month X

    3. When you hover an event, you will see a popover that tells you more about the game 
    (tippy and FullCalendar) X (Falta ponerle animaciones y ponerlo bonito)

    4. When you click an event, it will take you to a page that tells you more 
    about the game and has the option to add it to the watchlist. XX
        4.1. Doing so will change the color of the  background of the event. X

    5. Add the option to put a game in a watchlist (Followed Games). XX

    6. Profile that shows the games that you are following (like a wishlist) X

    7. Add a game, make a search request to see if the game is in the API, if it is,
    add it automatically (Modal, Tailwind CSS) X
        7.1. Change the already written code to make a checker to see if the game is already in the DB,
        if it is, it will tell you the date that is located, if it's not, it will tell you that is not in the
        DB. X
        
    8. Filter by genre. FullCalendar X

    9. Better search function. X

    10. Get notification if the game that you follow release that day and month (Too much trouble, left fro a later version)
    (At the end of the week or when a wanted release is coming): (Made with windows_task_manager) X
    (When deployed, it needs a broker like Redis or RabbitMQ) X

    11. Be able to update the database using a webhook. (Leaved for later when uploaded to a Domain because it
    need it for the webhook to able to work) X

from videogames_manager.models import Record_Calendar, Games_Data, Games_Genres, Games_Platforms
Record_Calendar.objects.all().delete()
Games_Data.objects.all().delete()
Games_Genres.objects.all().delete()
Games_Platforms.objects.all().delete()

from videogames_manager.models import User
User.objects.all().delete()

1. Role-playing (RPG)
2. Strategy
3. Shooter
4. Indie
5. Arcade
6. Turn-based strategy (TBS)
7. Simulator
8. Adventure
9. Sport
10. Platform
11. Racing
12. Point-and-click
13. Puzzle
14. Card & Board Game
15. Real Time Strategy (RTS)
16. Tactical
17. Hack and slash/Beat 'em up
18. Fighting
19. Music
20. MOBA
21. Visual Novel
22. Quiz/Trivia
23. Pinball
"""
