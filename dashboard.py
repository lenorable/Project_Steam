import eel # voor GUI
import json
import complex_functions
import string
import random
import psycopg2
import API

eel.init('GUI') #vanaf hieronder "init" (inhoud) eel, tot aan benede\

@eel.expose #laat zien aan javascript dat de functie bestaat en aangeroepen kan worden.
def get_data():
    return API.get_api_info(1816550)["price"]

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

    return True

@eel.expose
def Get_games(start_num):
    print(start_num)
    back = {}
    for item in range(start_num, (start_num+5)):
        back[item] = API.get_api_by_nummer(item)

    return back

eel.start('GUI.html') # alles wat binnen "eel.init" & eel.start valt is inhoud GUI1