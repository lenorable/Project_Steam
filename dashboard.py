import eel # voor GUI
import json
import complex_functions
import string
import random
import psycopg2
import API
from API import *
import math
import re

eel.init('GUI') #vanaf hieronder "init" (inhoud) eel, tot aan benede\

@eel.expose #laat zien aan javascript dat de functie bestaat en aangeroepen kan worden.
def get_data():
    return API.get_api_info(1816550)["price"]

charlist = " " + string.punctuation + string.digits + string.ascii_letters
chars = list(charlist)
key = ['h', 'A', 'U', 'T', 'v', 'K', '&', '}', 'O', ',', 'x', 'b', 'a', 'l', 'I', '{', '7', '!', 'y', 'L', '1', '"', '*', 'W', '/', 'R', 'd', 'G', 'Q', 'S', '5', 'f', 'C', 't', 'N', ';', 'q', "'", '|', '@', 'M', '%', 'H', '`', '4', '0', 'n', 'Y', ':', 'c', '6', 'D', '=', '$', '#', 'e', '(', '3', 'B', 'w', '~', '-', '\\', 'u', 'V', 'o', 'P', ']', 'J', 'j', 'F', 's', 'p', 'E', 'm', '8', ')', '_', '.', '<', '^', ' ', '+', '>', 'k', '9', '[', 'Z', 'r', '?', 'z', 'g', '2', 'i', 'X']

# gooi dit ALSJEBLIEFT UITEINDELIJK IN DE LOG IN FUNCTIE

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
        id = API.get_api_by_nummer(item)
        awns = API.get_api_info(id)
        return_item[id]["name"] = awns["name"]
    
    return return_item

@eel.expose
def login(email, passw):

    connection_string = "host='localhost' dbname='Login' user='postgres' password='k6LfYEIszD1cOP29qTvx'"
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    query = "SELECT password FROM login WHERE email = '{}';".format(email)

    cursor.execute(query)
    saves = cursor.fetchall()
    conn.close()

    try:
        if saves[0][0] == encrypt(passw):
            connection_string = "host='localhost' dbname='Login' user='postgres' password='k6LfYEIszD1cOP29qTvx'"
            conn = psycopg2.connect(connection_string)
            cursor = conn.cursor()

            query = "SELECT id FROM login WHERE email = '{}';".format(email)

            cursor.execute(query)
            saves = cursor.fetchall()
            conn.close()

            global glob_id
            glob_id = saves[0][0]
            load_user_data(glob_id)
           
            return True
        else:
            return False
    except:
        return False

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

    global glob_id
    glob_id = id
    load_user_data(glob_id)

    return True

@eel.expose
def Get_games(start_num):
    back = {}
    for item in range(start_num, (start_num+5)):
        back[item] = API.get_api_info_basic(item)

    return back

@eel.expose
def get_pages_len():
    return math.ceil(len(response_data_save['applist']["apps"]) / 5)

@eel.expose
def get_all_game_info(id):
    return API.get_api_info(id)

@eel.expose
def check_game_owned(id):
    for item in API.user_games:
        if item["appid"] == id:
            return True
    return False

@eel.expose
def user_game_data(game_id):
    return API.load_user_data_game(glob_id, game_id)

@eel.expose
def askid():
    global glob_id
    return glob_id

@eel.expose
def change_color():
    f = open("settings.json", "r")
    color_now = json.loads(f.read())
    f.close()

    r = open("GUI/GUI.css", "r")
    data_now = r.read()
    r.close()

    if color_now["settings"]["colors"] == 0:
        for item in color_now["color_scheme"][color_now["settings"]["colors"]]:
            data_now = data_now.replace(color_now["color_scheme"][color_now["settings"]["colors"]][item], color_now["color_scheme"][1][item])
        color_now["settings"]["colors"] = 1
        f = open("settings.json", "w")
        f.write(str(color_now).replace("'", '"'))
        f.close()
    else:
        for item in color_now["color_scheme"][color_now["settings"]["colors"]]:
            data_now = data_now.replace(color_now["color_scheme"][color_now["settings"]["colors"]][item], color_now["color_scheme"][0][item])
        color_now["settings"]["colors"] = 0
        f = open("settings.json", "w")
        f.write(str(color_now).replace("'", '"'))
        f.close()

    f = open("GUI/GUI.css", "w")
    f.write(data_now)
    f.close()

@eel.expose
def get_friends_info():
    return API.friend_info

@eel.expose
def get_friends_game(steam_id):
    resource_uri = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=32D90521B5D10D656EF5AEBD9CCE5A16&steamid={}&format=json".format(steam_id)
    response = requests.get(resource_uri)
    try:
        return response.json()["response"]["games"]
    except:
        return ""

@eel.expose
def get_simple_game_info(steam_id):
    for appitem in API.response_data_save['applist']["apps"]:
        if appitem[0] == steam_id:
            return appitem[1]

@eel.expose
def search_name(name):
    for appitem in API.response_data_save['applist']["apps"]:
        if appitem[1] == name:
            return appitem[0]

@eel.expose
def overwrite_status():
    global glob_id
    connection_string = "host='localhost' dbname='Login' user='postgres' password='k6LfYEIszD1cOP29qTvx'"
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    query = "SELECT status from login WHERE id = {};".format(glob_id)

    cursor.execute(query)
    saves = cursor.fetchall()
    conn.close()

    if saves[0][0] == "desk":
        return True
    else:
        return False

@eel.expose
def feedback(feedback):
    global glob_id
    connection_string = "host='localhost' dbname='Login' user='postgres' password='k6LfYEIszD1cOP29qTvx'"
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    query = "SELECT email from login WHERE id = {};".format(glob_id)

    cursor.execute(query)
    saves = cursor.fetchall()
    conn.close()

    connection_string = "host='localhost' dbname='Login' user='postgres' password='k6LfYEIszD1cOP29qTvx'"
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    query = "INSERT INTO feedback VALUES ('{}', {}, '{}')".format(feedback, glob_id, saves[0][0])
    print(query)
    cursor.execute(query)
    conn.commit()
    conn.close

    return 'verstuurd, u krijgt binnenkort antwoord in uw mail.'

@eel.expose
def get_own_games():
    global glob_id
    resource_uri = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=32D90521B5D10D656EF5AEBD9CCE5A16&steamid={}&format=json".format(glob_id)
    response = requests.get(resource_uri)
    try:
        return response.json()["response"]["games"]
    except:
        return ""

@eel.expose
def searchgames(name):
    gamelist = API.response_data_save["applist"]["apps"]

    found = []
    for game in gamelist:
        if name in str(game[1]).lower():
            found.append([game[1], game[0]])
            if len(found) == 20:
                break

    return found

eel.start('GUI.html') # alles wat binnen "eel.init" & eel.start valt is inhoud GUI1