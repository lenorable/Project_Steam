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