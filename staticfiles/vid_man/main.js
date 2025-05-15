let calendar;
let all_events = [];

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    const buttons = document.querySelectorAll('button[data-genre]');
    buttons.forEach(button => button.disabled = true);
    if (calendarEl) {
        fetch('/get_games_data/')
            .then(response => response.json())
            .then(data => {
                    all_events = data.game_events.map(event => {
                        if (data.followed_games.some(game => game.id === event.id)) {
                            event.className = ['important-event'];
                        } else {
                            event.color = ['fc-event'];
                        }
                        return event;
                    });

                    const current_year = new Date().getFullYear();

                    calendar = new FullCalendar.Calendar(calendarEl, {
                        initialView: 'dayGridMonth',
                        themeSystem: 'bootstrap',
                        editable: true,
                        selectable: true,
                        events: all_events,
                        showNonCurrentDates: false,
                        dayMaxEvents: 5,
                        validRange: {
                            start: `${current_year}-01-01`,
                            end: `${current_year}-12-31`
                        },

                    eventClick: function(info) {
                    info.jsEvent.preventDefault();
                    let game_id = info.event._def.publicId;
                    window.location.href = `/game/${game_id}`;
                    },
                    eventMouseEnter: function(event, jsEvent, view) {
                    const genres = event.event._def.extendedProps.genre ? event.event._def.extendedProps.genre.join(", ") : "No genres available";
                    const content = `
                    <div class="p-4 rounded-lg shadow-lg hover:bg-gray-700 transition duration-300" style="background-color: #2d3748; color: #fff; border: 2px solid #ffcc00; box-shadow: 0 4px #ff9900, 0 6px 20px rgba(0, 0, 0, 0.19);">
                    <div class="flex justify-center items-center">
                            <img src="https://images.igdb.com/igdb/image/upload/t_cover_small/${event.event.url}.jpg" alt="${event.event.title}" class="rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
                        </div>
                        <div class="text-center mt-4">
                            <p class="text-sm text-blue font-bold">${event.event._def.extendedProps.summary}</p>
                        </div>
                        <div class="mt-2 p-2">
                            <p class="text-xs italic text-blue-400" style="text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);">Genres: ${genres}</p>
                        </div>
                    </div>
                    `;
                    if (!event.el._tippy) {
                        tippy(event.el, {
                            content: content,
                            allowHTML: true,
                            placement: 'right-end',
                            appendTo: document.body,
                            followCursor: true,
                            theme: 'game',
                        }).show();
                    }
                },
                eventContent: function(data) {
                    return {
                    html: `
                    <div class="tooltip-wrapper responsive-event">
                            <div class="flex items-center">
                                <img src="https://images.igdb.com/igdb/image/upload/t_cover_small/${data.event.url}.jpg" alt="${data.event.title}" class="rounded" style="width: 60px; height: 80px;">
                                <strong class="fc-title ml-2">${data.event.title}</strong>
                            </div>
                    </div> 
                        `
                    };
                },

                });
                calendar.render();
                calendarEl.classList.add('bounce');
                buttons.forEach(button => button.disabled = false);
            });
            }
})

document.addEventListener('DOMContentLoaded', function() {
    var follow_button = document.querySelector("#follow_button");
    if (follow_button) {
        follow_button.addEventListener('click', function(event) {
        event.preventDefault();
        
        var game_id = follow_button.getAttribute("data-game-id");
        var csrf_Token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        fetch(`/follow_game/${game_id}`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrf_Token,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            const messageElement = document.getElementById("message");
            messageElement.textContent = "";
            messageElement.className = "";

            if (data.status === "followed") {
                follow_button.textContent = "Unfollow";
                follow_button.className = "retro-button-unfollow";
                messageElement.textContent = "You are following this game!";
                messageElement.className = "text-lg font-semibold text-green-500";
            
            } else if (data.status === "unfollowed") {
                follow_button.textContent = "Follow";
                follow_button.className = "retro-button-follow";
                messageElement.textContent = "Game removed from Watchlist!";
                messageElement.className = "text-lg font-semibold text-red-500";

            } else {
                alert('Failed to follow the game');
            }
            setTimeout(() => {
                messageElement.textContent = "";
                messageElement.className = "";
            }, 4000);
        })}
    )} 
})

document.querySelectorAll('button[data-genre]').forEach(button => {
    button.addEventListener('click', function() {
        const genre = this.getAttribute('data-genre');
        filter_events(genre);
    });
});

function filter_events(genre) {
    const genre_type = document.getElementById('genre-type')
    if (calendar) {
        calendar.removeAllEvents();

        if (genre === 'all') {
            calendar.addEventSource(all_events);
            genre_type.textContent = "Default"
            close_Filter_Modal()
        } else {
            const filtered_events = all_events.filter(event => event.genre.includes(genre));
            calendar.addEventSource(filtered_events);
            genre_type.textContent = `${genre}`
            close_Filter_Modal()
        }
    }
}

document.getElementById('nav-bar-search').addEventListener('input', function() {
    const query = this.value;
    fetch(`/search_games/?q=${query}`)
    .then(response => response.json())
    .then(data => {
        const results_container = document.getElementById('results-container');
        results_container.innerHTML = '';

        data.games.forEach(game => {
            const result_item = document.createElement('div');
            result_item.className = 'result-item border-b border-gray-700 cursor-pointer';

            const link = document.createElement('a');
            link.href = `/game/${game.id}`;
            link.textContent = game.name;
            link.className = 'text-white';

            result_item.appendChild(link);
            result_item.addEventListener('click', function() {
                window.location.href = link.href;
            });

            results_container.appendChild(result_item)
        });
    });
});

const search_input = document.getElementById('nav-bar-search');
const results_container = document.getElementById('results-container');

search_input.addEventListener('focus', function() {
    if (this.value) {
        results_container.style.display = 'block';
    }
});

search_input.addEventListener('input', function() {
    if (this.value) {
        results_container.style.display = 'block';
    } else {
        results_container.style.display = 'none';
    }
})

document.addEventListener('click', function(event) {
    if (!search_input.contains(event.target) && !results_container.contains(event.target)) {
        results_container.style.display = 'none';
    }
})

document.getElementById('nav-bar-search').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        const query = this.value;
        fetch(`/search_games/?q=${query}`)
        .then(response => response.json())
        .then(data => {
            if (data.games) {
                const game = data.games.find(game => game.name.toLowerCase() === query.toLowerCase());
                if (game) {
                    window.location.href = `/game/${game.id}`;
                } else {
                    alert('Game not Found in the Database!');
                }};
        });
    }
});
