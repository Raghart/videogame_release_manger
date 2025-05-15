let calendar;
let all_events = [];
const results_container = document.getElementById('results-container');
const search_input = document.getElementById('nav-bar-search');

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    const buttons = document.querySelectorAll('button[data-genre]');
    buttons.forEach(button => button.disabled = true);
    if (calendarEl) {
        fetch('/get_games_data/')
            .then(response => response.json())
            .then(data => {
                all_events = process_events(data)
                calendar = initialize_calendar(calendarEl, all_events);
                calendar.render();
                calendarEl.classList.add('bounce');
                buttons.forEach(button => button.disabled = false);
            });
}});

document.querySelectorAll('button[data-genre]').forEach(button => {
    button.addEventListener('click', function() {
        const genre = this.getAttribute('data-genre');
        filter_events(genre);
    });
});   

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
            update_follow_btn(data, follow_button, document.getElementById("message"));  
        })}
    )} 
})

document.getElementById('nav-bar-search').addEventListener('keydown', search_specific_game)

document.getElementById('nav-bar-search').addEventListener('input', debounce(handle_search, 300))

document.addEventListener('click', hide_results_container)

let currentPage = window.location.pathname;
let filterButton = document.getElementById("filter-button");

if (!currentPage.endsWith("/")) {
    filterButton.classList.add("hidden");
} else {
    filterButton.classList.remove("hidden");
}

search_input.addEventListener('focus', toggle_results_container);
search_input.addEventListener('input', toggle_results_container);

function initialize_calendar(calendarEl, events) {
    const current_year = new Date().getFullYear();

    return new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        themeSystem: 'bootstrap',
        events: events,
        editable: false,
        showNonCurrentDates: false,
        dayMaxEvents: 5,
        validRange: {
            start: `${current_year}-01-01`,
            end: `${current_year}-12-31`
        },
        eventClick: function(info) {
            info.jsEvent.preventDefault();
            let game_id = info.event._def.publicId;
            console.log(game_id);
            window.location.href = `/game/${game_id}`;
        },
        eventMouseEnter: function(event, jsEvent, view) {
            if (window.innerWidth > 768) {
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
}

function process_events(data) {
    return data.game_events.map(event => {
        if (data.followed_games.some(game => game.id === event.id)) {
            event.className = ['important-event'];
        } else {
            event.color = ['fc-event'];
        }
        return event;
    });
}

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

function update_follow_btn (data, follow_button , messageElement) {
    messageElement.textContent = ""
    messageElement.className = ""

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
}

function handle_search(event) {
    const query = event.target.value;
    fetch(`/search_games/?q=${query}`)
        .then(response => response.json())
        .then(data => {
            results_container.innerHTML = '';

            data.games.forEach(game => {
                const result_item = create_result_item(game);
                results_container.appendChild(result_item);
            });
    })
    .catch(error => {
        console.error("Error fetching games:", error)
    });
}

function create_result_item (game) {
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

    return result_item
}

function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

function toggle_results_container() {
    results_container.style.display = search_input.value ? 'block' : 'none';
}

function hide_results_container(event) {
    if (!search_input.contains(event.target) && !results_container.contains(event.target)) {
        results_container.style.display ='none';
    }
}

function search_specific_game(event) {
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
}