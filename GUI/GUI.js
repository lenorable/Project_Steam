function handleClickEventJS(){
    document.getElementById("welcomeText").innerText = "Javascript data verkregen";
} //verandert "Innertext" na klik gebeurtenis middles Python

function handleClickEventPY(){
    eel.get_data()().then((response) => {
    document.getElementById("welcomeText").innerText = response;
    })
    document.getElementById("welcomeText").innerText = "wacht voor response python";
} //verandert "Innertext" na klik gebeurtenis middels Python, omdat deze langer kan duren hebben we een tussen tijd erbij gezet.

document.getElementById("OurjsBtn").addEventListener("click", handleClickEventJS)
document.getElementById("OurpyBtn").addEventListener("click", handleClickEventPY)

function log_in(){
    var email = document.getElementById("log_in_email").value;
    var passw = document.getElementById("log_in_pass1").value;

    if (email != "" && passw != ""){
            eel.login(email, passw)().then((response) => {
                if (response == true){
                    document.getElementById("Log_in").style.display = "none";
                    document.getElementById("Home").style.display = "block";
                    document.getElementById("menu_bar").style.display = "block";
                    home()
                } else {
                    window.alert("Something went wrong.");
                }
            })
    } else{
        window.alert("Make sure you awnserd all questions"); 
    }
}

function sing_up(){
    var email = document.getElementById("log_in_email").value;
    var passw = document.getElementById("log_in_pass1").value;
    var pass2 = document.getElementById("log_in_pass2").value;
    var id = document.getElementById("log_in_steam_id").value;

    if (email != "" && passw != "" && pass2 != "" && id != ""){
        if (passw == pass2){
            eel.Singup(email, passw, id)().then((response) => {
                if (response == true){
                    console.log("oke")
                    log_in()
                } else {
                    window.alert("Something went wrong.");
                }
            })
        } else {
            window.alert("Your passwords are not the same.");
        }
    } else{
        window.alert("Make sure you awnserd all questions"); 
    }
}

function show_sing_up(){
    document.getElementById("log_in_pass2").style.display = "block";
    document.getElementById("log_in_steam_id").style.display = "block";
    document.getElementById("log_in_button1").innerHTML = "Sing up";
    document.getElementById("log_in_button2").innerHTML = "Go back";
    document.getElementById("log_in_button1").setAttribute('onclick','sing_up()');
    document.getElementById("log_in_button2").setAttribute('onclick','sing_up_go_back()');
}

function sing_up_go_back(){
    document.getElementById("log_in_pass2").style.display = "none";
    document.getElementById("log_in_steam_id").style.display = "none";
    document.getElementById("log_in_button1").innerHTML = "Login";
    document.getElementById("log_in_button2").innerHTML = "Sing up";
    document.getElementById("log_in_button1").setAttribute('onclick','log_in()');
    document.getElementById("log_in_button2").setAttribute('onclick','show_sing_up()');
}

function home_get_games(start_num){
    eel.Get_games(start_num)().then((response) => {
        console.log(response);
            var inhoud = "";
            var max = start_num + 5;

            for (let i = start_num; i < max; i++){
                var now_info = response[i];

                inhoud = inhoud + "<div class='game_box'><img src='https://cdn.cloudflare.steamstatic.com/steam/apps/" + now_info["steam_appid"] + "/header.jpg'><button class='text_box'><strong>name: </strong>" + now_info["name"] + "<br><strong>categorie: </strong>" + now_info["categories"] + "<br><strong> id: </strong>" + now_info["steam_appid"] + "</button></div>";
            }

            document.getElementById("game_display_home").innerHTML = inhoud;
    })
}

//to start all functions for _____ screen
function home(){
    home_get_games(1000)
}

function games(){

}

function players(){

}

function compare(){

}

function account(){

}
// einde automatisch startende functies