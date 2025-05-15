## License

This project is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0).  
You may view the code for educational purposes only.  
You may not copy, distribute, or modify it without explicit permission.

[Read the full license here](https://creativecommons.org/licenses/by-nc-nd/4.0/)

## Distinctiveness and Complexity

First before I start describing the Distinctiveness and complexity of this project, I would like to thank all the CS50 team for offering so much good information and classes for free. Thanks to this I was able to find my passion for code design that has allowed me to learn a lot these weeks that I have been focused doing this course, without more to add, I will begin to explain the project that I did.

### Distinctiveness

When I was thinking about which project I should do, something prominent in my mind was that it should be a project that would solve a problem or that would be useful to someone in the future because, personally I do not find exciting a big project that even if it works properly, is not useful to me so I would have it stored in a drawer for a long time. 

It is for that reason that I thought of joining one of my passions which are the Videogames so that somehow, I could get information about the hundreds of games that come out every month and to be able to visualize them when I need it, it is from there where I came up with this project which I called it as a Videogame Release Manager. Through this project, I want the user to be able to visualize a large amount of games, to have the comfort of being able to know more about a specific game just by hovering the mouse over a game to see a summary of what the game is about, and if you are very interested in it, then you can add it to a list of games followed that if you click on the wishlist, then you can see all the games that the user is currently following.

Justifying a little more in the distinctiveness part of my project, I am always aware of each release of a video game whether made by a large or a small company, a very recurrent problem I had is that I am a person who prefers to explain things with images rather than with blocks of text, I had the idea to show the video games that will be released in the form of calendar events to know which games will be released each day and be able to quickly visualize if they interest me or simply ignore them.

It should be noted that this project is focused on PC games as it is the platform on which I play mainly, besides that every day hundreds of games are released for different platforms even for mobile phones, so for reasons of ensuring the proper functioning of the IGDB API and keep reasonable the scope of the project in this list are only games that come out on both PC and Nintendo Switch.

### Complexity

Starting now to explain the complexity section of my project, I want to start by saying that my project handles and processes over 3000 games so that the information can be displayed in a way that does not overwhelm the user by seeing all the games that come out this year. All this data is obtained through the IGDB API, obtaining up to a limit of 300 games each month to ensure that each month has an equal amount of games that you might be interested in. 

The IGDB API besides informing you about the release date of each game in timestamp format, allows you to get other information such as the url cover of the game, its genres, a summary text that gives more information about it, a text that gives information about its history if it has one and the platform on which the game will be released. In order to only have to make a round of requests to the API to give you information of all the games that will be released the specific year in which the request is made, because as expected, processing those 3300 games takes a lot of time, this is where the models come in where all that information is stored, more specifically in a model called “Games_Data” located in “models.py” that stores all the information mentioned above for each game.

But before being able to store the information it is logical that we have in account the formats of the information in which the information of each game comes, being the most relevant the release date because we are trying to show the events in a calendar, in which for this project the library of FullCalendar of Javascript was chosen since it grants so much the functionalities as the sufficient customization to create a good calendar in which the games that come out every day of comfortable form can be visualized. 

To be able to show an event on a specific day using this library, it is necessary that its format is in a normal date format, with this I mean the date format that we all know as “YYYYY-MM-DD”, which is very different from the format that comes from the API which is timestamp, so it is necessary to change it beforehand so that it can be easily recognized in FullCalendar, but besides this if we start to carefully review the release date of each game, we will realize that there are games that come out every day, we will realize that there are games that come out every day with the same date, we will realize that there are games that have several release dates which is logical because many games may first be released on a specific console and then when it will be released on PC is when its release is detected with the request I'm making, that's why it is important first of all to obtain the largest release date presented in that list of dates in timestamp format, and then transform them into a recognizable format so that when it is stored in the model, FullCalendar can take care of organizing it in its corresponding box.

In the case that it is the first time running the program in a specific year that is not registered in the record of my model, this will be responsible for making a total of 12 requests to the API that were handled with the concurrent.futures library to make them in parallel in the shortest possible time, but as the documentation of the IGDB API says it is only possible to send 4 requests at the same time, because if you send more you have the risk of throwing an error that reports that it was not possible to successfully complete your requests. For this reason, they were organized in batches of 4 requests so that when they finish getting 4 requests then another 4 requests are launched until a request is made for each day of the month.

In the same way that a game can have more than one release date, a game can be released for different consoles as well as have different genres, that is why before entering it in the model this data was extracted from the “.json” file that was obtained as a response from the API in a more readable and comfortable format to store it inside the model.

Once explained the way in which I get the data from the API, the other features of my project seek to effectively use all the data obtained and present them to users in a simple way that is not overwhelming at first glance, being able to display a list of up to 300 games per month so you can comfortably search for a game you like. Among the features that my program has you can find: 

- A function that has FullCalendar to make a specific function when the mouse enters an event called as “EventMouseEnter”, that I took advantage to show a tooltip that is in charge of showing information about the game, appearing a url image, a summary of the game, and the game genres that you have the mouse over it.
  
- The function that if you are interested in a specific game and want to get more information about it, then by clicking on an event, by using the game ID, it will automatically redirect you to a page where it will show you more information about the game you want to know more about, such as a description about its history, what platforms it is currently on, and even giving you the option to follow it if it caught your attention enough, adding it to a list that you can conveniently view from your profile if you press the “Wishlist” button at the top of the page.
  
- A game finder to check if a specific game is currently in the database. It should be noted that you can only activate it if you double click on any day box in FullCalendar and correctly type the name of the game, if it exists in the database then it will confirm its existence and the exact date you can find it so you can go to that date and you can give it a follow if you are interested in this game.

- The function that when you click on the “Wishlist” button located at the top of the page you can see the games you are currently following, in case you want to remember the games that caught your attention and you are waiting to play them in a specific month when they come out.
  
- The ability to filter games by genre without the need to refresh the page by using the data previously obtained from the API, since each game can have one or more genres, it is possible through a set of buttons to have the ability to filter them to show only the games that include a specific genre, being able to do this function by clicking the button “Filtering by: Default” located at the top of my page, which will show a modal with 24 buttons so you can choose the genre of the game you want to view and almost instantly update the information without having to reload the page, thus improving the user experience of users.
  
- Last but not least to take into account is the initial function to register which was used the django-allauth library to make a complete system of registration and authentication in which we are asked to register a username, our email and a password and then, in order to verify that we are not robots sends us an email to confirm that this is our email, and after pressing it, you can start using all the applications mentioned above. In addition a form located in forms.py was used to modify the aesthetic aspect to fit more with the rest of CSS applied in the project, in which both Tailwind CSS and bootstrap were used to stylize much of this project, adding even animations to improve the user experience.

### What's contained in each created file?

Next I will explain what contains each file created or modified for the realization of this project:

- Util.py: In this file is all the code that is responsible for checking if there is a game database for the current year that the program was executed, which if it does not exist then performs the 12 requests to the IGDB API to obtain the data to be used in the program, and store them in a model so that the next time the user enters the page will use the information stored in the model to improve the user experience and handle more quickly the functions of the web page. This code was kept in another file other than views.py to try to keep as clean as possible the code that handles the views.

- forms.py: In this file were registered the forms for the creation of a user and to authenticate it, which are necessary if you want to modify the base form that gives you django-allauth because aesthetically did not fit with the rest of the project, so I had to register 2 new forms to manipulate them as required.
  
- models.py: Here are the models in which all the information obtained by the IGDB API is stored, in my case I have 5 models, being the main one the model called “Games_Data” in which all the games are stored along with their respective data, the other 3 models above this one are in charge of storing the year of release of the games using a Foreign Key, their release platforms and their genres by using a ManytoMany.Field since a game can have multiple genres and can be released on multiple platforms. The 5th model is in charge of storing the users and storing the logic of if the user is following a game then storing it in the user model so that when the events are loaded it is displayed with a different red color than the rest of the elements.
  
- templatetags: In this folder is stored a simple python code that is necessary to create it to add the ability to customize the forms in forms.py and add classes to make them look flashy. This was done because the Django-allauth library, although it is very complete to handle user registration and authentication, is very rigid in terms of customizing its appearance to fit with the rest of the program.

- templates: In templates as you know this is where the “.html” files are stored in which information is taught, in my case I have 2 folders one being specific to django-allauth which is called as “account”, and the other folder called “vid_man” being used to store the html files that are responsible for teaching information regarding the games. 

  - In game_detail is the html that is shown when you click on an event, in index.html is the base page of the program where you can find the FullCalendar calendar and the modal used for the function of checking if a game is in the database and when you are going to filter the games by genre.

  - In layout.html this the layout of the page that this in all the pages located by the superior part, only that the options that appear in this will depend if the user is logged in or not, only being able to log in or to register if the user is not authenticated, and showing the options of profile, to filter by genres and logout if the user is authenticated, 

  - In wishlist.html that is where the list of games that currently follows the user who is connected is found. 

  - In welcome.html which is where you will find a welcome page whose purpose is only to receive users who are not connected.
  
- main.js: This file is in charge of handling all the Javascript code that affects the project on the Frontend side, in this is the code that handles the FullCalendar library to ensure that the events sent from the Backend are displayed without any problems, integrating also the functions mentioned in the complexity section within the own functions available in the FullCalendar library, in order to make it more interactive and improve the user experience, being one of them for example to detect if the user follows a specific game then it will add a CSS or style different from the rest of events. In addition to handling the events and calendar functions, this file also handles the code to receive an instant response from the functions such as the game search engine in the database, the code to follow a game and a different message appears depending on whether you already follow the game or not, and the code to filter the games also used javascript code to make the change of events instantaneous without having to reload the page, in which also changes the text of the button “Filtering by” to indicate that it is currently filtering.

- styles.css: Here as we well know is all the CSS used in the html pages that I mentioned in the html part, in which I tried to use configurations and colors that will combine with a dark background since I am very fan of these types of backgrounds. Besides having customization of specific parts of FullCalendar, I also added 2 animations to make the user interface more eye-catching.

- tailwind.config.js: This is the default configuration file that was created when installing the Javascript libraries, in this one what I configured was to place a dark background inside it.
  
- output.css: This file is important to include the tailwind options.css in my project, I added it because they add more advanced customization options than bootstrap, and as mentioned above I am a very visual person so I needed to like my project aesthetically, so I opted to install this library to expand my options.

- package.json, package-lock.json and node_modules: They are files created automatically when I install the Javascript libraries that I need to make my project that in this case were 5 libraries of FullCalendar and one of tailwind.css.

- views.py: As well we know in this part I manage the information that I pass to my html as well as I manage the Jsonresponse that I send to my Javascript to manage the information in real time, and to achieve that the changes are carried out without needing to reload the page.

### How to run my application?

With the version I'm passing you it is not necessary to make requests to the API to register the games database because the data of the games you are going to use already exists in db.sqlite3, but my program has the ability that in case it does not detect a game record for that year to extract the information, requests will be made to the IGDB API that can take a maximum time of 5 minutes for it to correctly display the data and have been saved correctly in the models. It is only necessary to go through this process once since the information is stored in the database, the processes will be performed with this information stored in the models to guarantee a good user experience and that the functions are executed as quickly as possible. 

In my case I made the project in VS code that as you may know, if VS code is positioned in the base folder of the project you can run this application using the following code in the terminal: "python manage.py runserver".

### Other Information

Thank you very much for all your work making this course possible! This was a personal project that I took a lot of time to do by myself and I hope you liked it. Have a nice day!
