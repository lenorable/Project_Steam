const { copyFileSync } = require("original-fs");
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
        eel.get_pages_len()().then((responses) => {

            var page_nu = start_num / 5 + 1

            var inhoud = "<div class='pages'><button class='left' onclick='page_change(" + '"home"' + "," + '"back"' + ")'><i class='fa-solid fa-caret-left'></i></button><button class='mid' id='pagefrom'>" + page_nu + " van " + responses + "</button><button class='right' onclick='page_change(" + '"home"' + "," + '"next"' + ")'><i class='fa-solid fa-caret-right'></i></button></div>";
            var max = start_num + 5;

            for (let i = start_num; i < max; i++) {
                var now_info = response[i];

                if (now_info != "error") {
                    inhoud = inhoud + "<div class='game_box'  onclick='change_screen(" + '"Games"' + "," + now_info["steam_appid"] + ")'><img src='https://cdn.cloudflare.steamstatic.com/steam/apps/" + now_info["steam_appid"] + "/header.jpg'><button class='text_box'><strong>name: </strong>" + now_info["name"] + "<br><strong> id: </strong>" + now_info["steam_appid"] + "</button></div>";
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
                    inhoud = inhoud + "<div class='game_box'  onclick='change_screen(" + '"Games"' + "," + now_info["steam_appid"] + ")'><img src='https://cdn.cloudflare.steamstatic.com/steam/apps/" + now_info["steam_appid"] + "/header.jpg'><button class='text_box'><strong>name: </strong>" + now_info["name"] + "<br><strong> id: </strong>" + now_info["steam_appid"] + "</button></div>";
                }
            }

            document.getElementById("game_display_games").innerHTML = inhoud;
        });
    })
}

//to start all functions for _____ screen
function Home() {
    home_get_games(-5);
}

function Games(game) {
    if (game == null) {
        games_get_games(-5);
        document.getElementById('piechart_ratings').innerHTML = "";
        document.getElementById('personal_game_info').innerHTML = "";
    } else {
        game_info(game);
        get_own_game_info(game)
    }
}

function Players() {
    document.getElementById("friend_info").innerHTML = "";
    get_friends();
}

function Compare() {

}

function Account() {
    get_own_games();
    eel.askid()().then((response) => {
        document.getElementById("account_id_copy").innerHTML = "<strong>id: </strong>" + response;
    })
}
// einde automatisch startende functies

function change_screen(screen, id) {
    var lst = ["Home", "Games", "Players", "Compare", "Account"];

    for (let i = 0; i < lst.length; i++) {
        if (lst[i] != screen) {
            document.getElementById(lst[i]).style.display = "none";
            //document.getElementById("button_" + lst[i]).style.backgroundColor = "#2A475E";
        } else {
            document.getElementById(lst[i]).style.display = "block";
            //document.getElementById("button_" + lst[i]).style.backgroundColor = "#375d7b";
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
                backgroundColor: { stroke: '#1B2838', fill: "none" },
                legend: { textStyle: { color: '#c7d5e0' } },
                titleTextStyle: { color: '#c7d5e0' }
            };


            var chart = new google.visualization.PieChart(document.getElementById('piechart_ratings'));
            chart.draw(data, options);
        }
    })
}

function get_own_game_info(id) {
    eel.check_game_owned(id)().then((response) => {
        var inhoud = ""
        if (response == true) {
            eel.user_game_data(id)().then((response2) => {
                console.log(response2)
                inhoud = "<h1>your achievements:</h1>"

                for (let i = 0; i < response2["achieve"].length; i++) {
                    if (response2["achieve"][i]['achieved'] == 1) {
                        var naam = response2["achieve"][i]["name"];
                        var description = response2["achieve"][i]["description"];
                        var api_naam = response2["achieve"][i]["apiname"];


                        for (let x = 0; x < response2["glob_achieve"].length; x++) {
                            if (response2["glob_achieve"][x]["name"] == api_naam) {
                                var percent = response2["glob_achieve"][x]["percent"];
                                break;
                            }
                        }

                        inhoud = inhoud + "<button class='information_true'><strong>Name: </strong>" + naam + "<br> <strong>Description: </strong>" + description + "<br> <strong>Global achievment count: </strong>" + Math.round(percent) + "%<br></button>";
                    }
                }

                document.getElementById("personal_game_info").innerHTML = inhoud;
            })
        } else {
            inhoud = "<button class='information_false'>You do not own this game</button>";
        }

        document.getElementById("personal_game_info").innerHTML = inhoud;
    })
}

function compare_get(id1, id2) {
    eel.get_all_game_info(id1)().then((response) => {
        var to_get = ["achievements", "average_playtime", "categories", "developers", "english", "genre", "median_playtime", "negative_ratings", "owners", "platforms", "positive_ratings", "price", "publisher", "release_date", "required_age", "steam_appid"]
        var inhoud = ""

        document.getElementById("compare_title_box_left").innerHTML = "<img src='https://cdn.cloudflare.steamstatic.com/steam/apps/" + id1 + "/header.jpg'><button class='title'><strong>Name: </strong>" + response["name"] + "</button>";

        for (let i = 0; i < to_get.length; i++) {
            inhoud = inhoud + "<strong>" + to_get[i] + ": </strong>" + response[to_get[i]] + "<br>";
        }

        document.getElementById("compare_div_left").innerHTML = inhoud;
        inhoud = ""

        eel.get_all_game_info(id2)().then((response2) => {
            document.getElementById("compare_title_box_right").innerHTML = "<img src='https://cdn.cloudflare.steamstatic.com/steam/apps/" + id2 + "/header.jpg'><button class='title'><strong>Name: </strong>" + response2["name"] + "</button>";
            for (let i = 0; i < to_get.length; i++) {
                inhoud = inhoud + "<strong>" + to_get[i] + ": </strong>" + response2[to_get[i]] + "<br>";
            }
            document.getElementById("compare_div_right").innerHTML = inhoud;
        })
    })
}

function copy_id() {
    eel.askid()().then((response) => {
        window.alert("copied id: " + response);
        navigator.clipboard.writeText(response);
    })
}


function color_change() {
    eel.change_color()().then((response) => {
        var link = document.querySelector("link[rel=stylesheet]");
        link.href = link.href.replace(/\?.*|$/, "?" + Date.now())

    })
}

function get_friends() {
    eel.get_friends_info()().then((response) => {
        var inhoud = "<button class='players_title'>Your friends: </button>";

        console.log(response);
        if (response == "") {
            inhoud = inhoud + "<div class='friends_info'><button class='button'>Your friends settings are private or you dont have any friends</button></div>";
        } else {
            for (let i = 0; i < response.length; i++) {
                var data = response[i][1][0];
                inhoud = inhoud + "<div class='friends_info' onclick='friend_info_load(" + response[i][0] + ")'><img src='" + data["avatarfull"] + "'></img><button class='button'><strong>Name: </strong>" + data["personaname"] + "</button></div>";
            }
        }

        document.getElementById("your_friends").innerHTML = inhoud;
    })
}

function friend_info_load(player_id) {
    eel.get_friends_info()().then((response) => {
        for (let i = 0; i < response.length; i++) {
            if (response[i][0] == player_id) {
                eel.overwrite_status()().then((response2) => {

                    var inhoud = "<button class='player_display_left_text' id='text_player_info'></button>";
                    var data = response[i][1][0];
                    var inhoud2 = ""
                    console.log(data);
                    var status = data["personastate"];
                    var write_status = "";

                    if (response2 == false) {
                        if (status == 0) {
                            write_status = "Offline";
                        } else if (status == 1) {
                            write_status = "Online";
                        } else if (status == 2) {
                            write_status = "Busy";
                        } else if (status == 3) {
                            write_status = "Away";
                        } else if (status == 4) {
                            write_status = "Snooze";
                        } else if (status == 5) {
                            write_status = "Looking to trade";
                        } else if (status == 6) {
                            write_status = "Looking to play";
                        }
                    } else {
                        write_status = "by desk";
                    }

                    inhoud = inhoud + "<div class='friends_info' id='change_top'><img src='" + data["avatarfull"] + "'></img><button class='button'><strong>Name: </strong>" + data["personaname"] + "</button></div>";

                    inhoud2 = inhoud2 + "<strong>ID: </strong>" + data["steamid"] + "<br>"
                    inhoud2 = inhoud2 + "<strong>Status: </strong>" + write_status + "<br>"
                    inhoud2 = inhoud2 + "<strong>Last online: </strong>" + timeConverter(data["lastlogoff"]) + "<br>"
                    inhoud2 = inhoud2 + "<strong>Acc made on: </strong>" + timeConverter(data["timecreated"]) + "<br>"
                    inhoud2 = inhoud2 + "<strong>Country: </strong>" + data["loccountrycode"] + "<br>"
                    inhoud2 = inhoud2 + "<strong>Real Name: </strong>" + data["realname"] + "<br>"
                    inhoud2 = inhoud2 + "<strong>Site: </strong><a href='" + data["profileurl"] + "' target='_blank'>profile page</a><br>"

                    document.getElementById("friend_info").innerHTML = inhoud;
                    document.getElementById("change_top").style.top = "0%";
                    document.getElementById("change_top").style.marginTop = "0%";
                    document.getElementById("text_player_info").innerHTML = inhoud2;

                    get_games_of_friends(data["steamid"]);
                })
            }
        }
    })
}

function timeConverter(UNIX_timestamp) {
    if (UNIX_timestamp != undefined) {
        var a = new Date(UNIX_timestamp * 1000);
        var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        var year = a.getFullYear();
        var month = months[a.getMonth()];
        var date = a.getDate();
        var hour = a.getHours();
        var min = a.getMinutes();
        var sec = a.getSeconds();
        var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec;
        return time;
    }
    return undefined
}

function steam_status_rewrite(status) {
    eel.overwrite_status()().then((response) => {
        if (response == false) {
            if (status == 0) {
                return "Offline";
            } else if (status == 1) {
                return "Online";
            } else if (status == 2) {
                return "Busy";
            } else if (status == 3) {
                return "Away";
            } else if (status == 4) {
                return "Snooze";
            } else if (status == 5) {
                return "Looking to trade";
            } else if (status == 6) {
                return "Looking to play";
            }
        } else {
            return "by desk";
        }
    })
}

function get_games_of_friends(steam_id) {
    eel.get_friends_game(steam_id)().then((response) => {
        var inhoud = document.getElementById("friend_info").innerHTML;

        if (response.length > 0) {
            for (let i = 0; i < response.length; i++) {
                eel.get_simple_game_info(response[i]["appid"])().then((response2) => {
                    console.log("games log: \n" + response[i]["appid"] + "\n response2: " + response2)
                    inhoud = inhoud + "<div class='player_display_left_games' onclick='change_screen(" + '"Games",' + response[i]["appid"] + ");'><img src='https://cdn.cloudflare.steamstatic.com/steam/apps/" + response[i]["appid"] + "/header.jpg'><button class='button'><strong>Name: </strong>" + response2 + "</button></div>";
                    document.getElementById("friend_info").innerHTML = inhoud;
                })
            }
        }

    })
}

function give_feedback(){
    var feedback = document.getElementById("feedback").value

    eel.feedback(feedback)().then((response) => {
        document.getElementById("feedback").value = ""
    })
}

function get_own_games(){
    var inhoud = "<button class='button'>My games: </button>";

    eel.get_own_games()().then((response) => {
        for (let i = 0; i < response.length; i++){
            eel.get_simple_game_info(response[i]["appid"])().then((response2) => {
                inhoud = inhoud + "<div class='games' onclick='change_screen(" + '"Games",' + response[i]["appid"] + ");'><img src='https://cdn.cloudflare.steamstatic.com/steam/apps/" + response[i]["appid"] + "/header.jpg'><button class='button'><strong>Name: </strong>" + response2 + " </button></div>";
                document.getElementById("my_games").innerHTML = inhoud;
            })
        }
    })
}