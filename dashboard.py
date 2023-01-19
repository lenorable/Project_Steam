import requests # voor de API
import eel # voor GUI
import json
import complex_functions
import string
import random
import psycopg2

resource_uri = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json"
response = requests.get(resource_uri)
response_data_save = response.json()

def get_api_by_nummer(api_item):
    #api_item = 1000 #geeft aan hoeveelste item van de opgehaalde data je wilt gebruiken
    app_id = response_data_save['applist']["apps"][api_item]["appid"]
    return get_api_info(app_id)

eel.init('GUI') #vanaf hieronder "init" (inhoud) eel, tot aan benede

#geef de app id op en krijg alle data terug in een json format. gebruik: hoe duur is app 1816550 --> print(get_api_info(1816550)["price"])
#de meeste items die meer dan 1 value terug geven zijn door een ";" gescheiden. alleen de genre is gescheiden door ", ".
def get_api_info(app_id):
    resource_uri = "http://store.steampowered.com/api/appdetails?appids={}".format(app_id)
    response = requests.get(resource_uri)
    response_data = response.json()

    base_api_data = response_data[str(app_id)]["data"]
    api_info = ["steam_appid", "name", "release_date", "english", "developer", "publisher", "platforms", "required_age", "categories", "genres", "steamspy_tags", "achievements", "positive_ratings", "negative_ratings", "average_playtime", "median_playtime",  "owners",  "price"]


    def English_support():
        if "English" in base_api_data["supported_languages"]:
            return True
        
    def developers():
        developers = ""
        for item in base_api_data["developers"]:
                developers = developers + item + ';'

        return developers

    def publishers():
        publishers = ""
        for item in base_api_data["publishers"]:
                publishers = publishers + item + ';'

        return publishers

    def platforms():
        platforms = ""
        for item in base_api_data["platforms"]:
            if base_api_data["platforms"][item] == True:
                    platforms = platforms + item + ';'

        return platforms

    def categories():
        categories = ""
        for item in base_api_data["categories"]:
            categories = categories + item["description"] + ';'

        return categories

    resource_uri = "https://steamspy.com/api.php?request=appdetails&appid={}".format(app_id)
    response = requests.get(resource_uri)
    response_data2 = response.json()

    def achievements():
        resource_uri = "https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/?gameid={}".format(app_id)
        response = requests.get(resource_uri)
        response_data3 = response.json()

        if str(response_data3) != "{}":
            return len(response_data3["achievementpercentages"]["achievements"])
        else:
            return 0 

    return_lst = {
        "steam_appid" : base_api_data["steam_appid"],
        "name" : base_api_data["name"],
        "release_date" : base_api_data["release_date"]["date"],
        "english" : English_support(),
        "developers": developers(),
        "publisher" : publishers(),
        "platforms" : platforms(),
        "required_age" : base_api_data["required_age"],
        "categories" : categories(),
        "genre" : response_data2["genre"],
        "achievements" : achievements(),
        "positive_ratings" : response_data2["positive"],
        "negative_ratings" : response_data2["negative"],
        "average_playtime" : response_data2["average_forever"],
        "median_playtime" : response_data2["median_forever"],
        "owners" : response_data2["owners"],
        "price" : base_api_data["price_overview"]["final_formatted"]
    }

    return return_lst

@eel.expose #laat zien aan javascript dat de functie bestaat en aangeroepen kan worden.
def get_data():
    return get_api_info(1816550)["price"]

charlist = " " + string.punctuation + string.digits + string.ascii_letters
chars = list(charlist)
key = ['h', 'A', 'U', 'T', 'v', 'K', '&', '}', 'O', ',', 'x', 'b', 'a', 'l', 'I', '{', '7', '!', 'y', 'L', '1', '"', '*', 'W', '/', 'R', 'd', 'G', 'Q', 'S', '5', 'f', 'C', 't', 'N', ';', 'q', "'", '|', '@', 'M', '%', 'H', '`', '4', '0', 'n', 'Y', ':', 'c', '6', 'D', '=', '$', '#', 'e', '(', '3', 'B', 'w', '~', '-', '\\', 'u', 'V', 'o', 'P', ']', 'J', 'j', 'F', 's', 'p', 'E', 'm', '8', ')', '_', '.', '<', '^', ' ', '+', '>', 'k', '9', '[', 'Z', 'r', '?', 'z', 'g', '2', 'i', 'X']

def encrypt(password):
    crypted = ""
    for item in password:
        index = chars.index(item)
        crypted += key[index]
    return crypted


def decrypt(password):
    decrypted = ""
    for item in password:
        index = key.index(item)
        decrypted += chars[index]
    return decrypted

def get_games():
    return_item = {}
    for item in range(0, 9):
        id = get_api_by_nummer(item)
        awns = get_api_info(id)
        return_item[id]["name"] = awns["name"]
    
    return return_item

@eel.expose
def login():
    return True

@eel.expose
def Singup(email, passw, id):
    connection_string = "host='localhost' dbname='Login' user='postgres' password='k6LfYEIszD1cOP29qTvx'"
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    query = "INSERT INTO login VALUES ('{}', '{}', {})".format(email, encrypt(passw), id)
    print(query)
    cursor.execute(query)
    conn.commit()
    conn.close

    return True

eel.start('GUI.html') # alles wat binnen "eel.init" & eel.start valt is inhoud GUI1