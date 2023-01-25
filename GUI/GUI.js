const { rmSync } = require("original-fs");

function handleClickEventJS() {
    document.getElementById("welcomeText").innerText = "Javascript data verkregen";
} //verandert "Innertext" na klik gebeurtenis middles Python

function handleClickEventPY() {
    eel.get_data()().then((response) => {
        document.getElementById("welcomeText").innerText = response;
    })
    document.getElementById("welcomeText").innerText = "wacht voor response python";
} //verandert "Innertext" na klik gebeurtenis middels Python, omdat deze langer kan duren hebben we een tussen tijd erbij gezet.

document.getElementById("OurjsBtn").addEventListener("click", handleClickEventJS)
document.getElementById("OurpyBtn").addEventListener("click", handleClickEventPY)

function log_in() {
    var email = document.getElementById("log_in_email").value;
    var passw = document.getElementById("log_in_pass1").value;

    if (email != "" && passw != "") {
        eel.login(email, passw)().then((response) => {
            if (response == true) {
                document.getElementById("Log_in").style.display = "none";
                document.getElementById("Home").style.display = "block";
                document.getElementById("menu_bar").style.display = "block";
                change_screen("Home");
            } else {
                window.alert("Something went wrong.");
            }
        })
    } else {
        window.alert("Make sure you awnserd all questions");
    }
}

function sing_up() {
    var email = document.getElementById("log_in_email").value;
    var passw = document.getElementById("log_in_pass1").value;
    var pass2 = document.getElementById("log_in_pass2").value;
    var id = document.getElementById("log_in_steam_id").value;

    if (email != "" && passw != "" && pass2 != "" && id != "") {
        if (passw == pass2) {
            eel.Singup(email, passw, id)().then((response) => {
                if (response == true) {
                    console.log("oke")
                    log_in()
                } else {
                    window.alert("Something went wrong.");
                }
            })
        } else {
            window.alert("Your passwords are not the same.");
        }
    } else {
        window.alert("Make sure you awnserd all questions");
    }
}

function show_sing_up() {
    document.getElementById("log_in_pass2").style.display = "block";
    document.getElementById("log_in_steam_id").style.display = "block";
    document.getElementById("log_in_button1").innerHTML = "Sing up";
    document.getElementById("log_in_button2").innerHTML = "Go back";
    document.getElementById("log_in_button1").setAttribute('onclick', 'sing_up()');
    document.getElementById("log_in_button2").setAttribute('onclick', 'sing_up_go_back()');
}

function sing_up_go_back() {
    document.getElementById("log_in_pass2").style.display = "none";
    document.getElementById("log_in_steam_id").style.display = "none";
    document.getElementById("log_in_button1").innerHTML = "Login";
    document.getElementById("log_in_button2").innerHTML = "Sing up";
    document.getElementById("log_in_button1").setAttribute('onclick', 'log_in()');
    document.getElementById("log_in_button2").setAttribute('onclick', 'show_sing_up()');
}

var game_game_page_num_now = 0
var home_game_page_num_now = 0


function home_get_games(start_num) {
    home_game_page_num_now = start_num;
    eel.Get_games(start_num)().then((response) => {
        console.log(response);
        eel.get_pages_len()().then((responses) => {

            var page_nu = start_num / 5 + 1

            var inhoud = "<div class='pages'><button class='left' onclick='page_change(" + '"home"' + "," + '"back"' + ")'><i class='fa-solid fa-caret-left'></i></button><button class='mid' id='pagefrom'>" + page_nu + " van " + responses + "</button><button class='right' onclick='page_change(" + '"home"' + "," + '"next"' + ")'><i class='fa-solid fa-caret-right'></i></button></div>";
            var max = start_num + 5;

            for (let i = start_num; i < max; i++) {
                var now_info = response[i];

                if (now_info != "error") {
                    inhoud = inhoud + "<div class='game_box' onclick='change_screen(" + '"Games"' + "," + now_info["steam_appid"] + ")'><img src='https://cdn.cloudflare.steamstatic.com/steam/apps/" + now_info["steam_appid"] + "/header.jpg'><button class='text_box'><strong>name: </strong>" + now_info["name"] + "<br><strong>catergory: </strong>" + now_info["categories"] + "<br><strong> id: </strong>" + now_info["steam_appid"] + "</button></div>";
                }
            }

            document.getElementById("game_display_home").innerHTML = inhoud;

        });
    })
}

function games_get_games(start_num) {
    game_game_page_num_now = start_num
    eel.Get_games(start_num)().then((response) => {
        console.log(response);
        eel.get_pages_len()().then((responses) => {

            var page_nu = start_num / 5 + 1

            var inhoud = "<div class='pages'><button class='left' onclick='page_change(" + '"game"' + "," + '"back"' + ")'><i class='fa-solid fa-caret-left'></i></button><button class='mid' id='pagefrom'>" + page_nu + " van " + responses + "</button><button class='right' onclick='page_change(" + '"game"' + "," + '"next"' + ")'><i class='fa-solid fa-caret-right'></i></button></div>";
            var max = start_num + 5;

            for (let i = start_num; i < max; i++) {
                var now_info = response[i];

                if (now_info != "error") {
                    inhoud = inhoud + "<div class='game_box'  onclick='change_screen(" + '"Games"' + "," + now_info["steam_appid"] + ")'><img src='https://cdn.cloudflare.steamstatic.com/steam/apps/" + now_info["steam_appid"] + "/header.jpg'><button class='text_box'><strong>name: </strong>" + now_info["name"] + "<br><strong>catergory: </strong>" + now_info["categories"] + "<br><strong> id: </strong>" + now_info["steam_appid"] + "</button></div>";
                }
            }

            document.getElementById("game_display_games").innerHTML = inhoud;
        });
    })
}

//to start all functions for _____ screen
function Home() {
    home_get_games(10);
}

function Games(game) {
    if (game == null) {
        games_get_games(10)
    } else {
        game_info(game);
    }
}

function Players() {

}

function Compare() {

}

function Account() {

}
// einde automatisch startende functies

function change_screen(screen, id) {
    var lst = ["Home", "Games", "Players", "Compare", "Account"];

    for (let i = 0; i < lst.length; i++) {
        if (lst[i] != screen) {
            document.getElementById(lst[i]).style.display = "none";
            document.getElementById("button_" + lst[i]).style.backgroundColor = "#2A475E";
        } else {
            document.getElementById(lst[i]).style.display = "block";
            document.getElementById("button_" + lst[i]).style.backgroundColor = "#375d7b";
            document.getElementById("button_" + lst[i]).st
            window[lst[i]](id);
        }
    }
}

function page_change(which, what) {
    if (which == "home") {
        if (what == "back") {
            home_get_games(home_game_page_num_now - 5);
        } else {
            home_get_games(home_game_page_num_now + 5);
        }
    } else if (which == "game") {
        if (what == "back") {
            games_get_games(game_game_page_num_now - 5);
        } else {
            games_get_games(game_game_page_num_now + 5)
        }
    }

}

function game_info(id) {
    eel.get_all_game_info(id)().then((response) => {
        var to_get = ["achievements", "average_playtime", "categories", "developers", "english", "genre", "median_playtime", "negative_ratings", "owners", "platforms", "positive_ratings", "price", "publisher", "release_date", "required_age", "steam_appid"]
        var info = ""

        for (let i = 0; i < to_get.length; i++) {
            info = info + "<strong>" + to_get[i] + ": </strong>" + response[to_get[i]] + "<br>";
        }

        document.getElementById("game_display_games").innerHTML = "<div class='game_detail_info_top'><img src='https://cdn.cloudflare.steamstatic.com/steam/apps/" + id + "/header.jpg'><button class='title'><strong>Name: </strong>" + response["name"] + "</button></div><div class='game_detail_info_bottom'>" + info + "</div>";


        // Load google charts
        google.charts.load('current', { 'packages': ['corechart'] });
        google.charts.setOnLoadCallback(drawChart);

        function drawChart() {
            var data = google.visualization.arrayToDataTable([
                ['Review', 'aantal'],
                ['Good', response["positive_ratings"]],
                ['Bad', response["negative_ratings"]],
            ]);

            var options = {
                'title': 'Ratings',
                colors: ['#33cc33', '#ff0000'],
                backgroundColor: { stroke: '#1B2838', fill: "#1B2838" },
                legend: { textStyle: { color: '#c7d5e0' } },
                titleTextStyle: { color: '#c7d5e0' }
            };


            var chart = new google.visualization.PieChart(document.getElementById('piechart_ratings'));
            chart.draw(data, options);
        }
    })
}