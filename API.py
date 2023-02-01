import requests # voor de API
import json
import re

user_games = {}
user_friends = {}
friend_info = []

#get data and write to file--------------------------------------------------------------------------------------------------
resource_uri = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=32D90521B5D10D656EF5AEBD9CCE5A16&format=json"
response = requests.get(resource_uri)
response_data_save = response.json()

f = open('testsave.json', 'w')
f.write('{"applist": {"apps":[')
f.close()

count = 0
percent = 0

f = open('testsave.json', 'a')
for item in response_data_save['applist']['apps']:

    #if round(100/len(response_data_save['applist']['apps'])*(count + 1)) != percent:
    #    percent = round(100/len(response_data_save['applist']['apps'])*(count + 1))
    #    print(str(percent) + "%")

    if count != len(response_data_save['applist']['apps'])-1:
        try:
            sos = re.sub(r"[^a-zA-Z0-9 ]+", '', str(item["name"]))
            if str(item["name"]) != "":
                f.write('[' + str(item["appid"]) +  ', "' + sos + '"],')
        except:
            print(str(item["appid"]))
            pass
    else:
        sos = re.sub(r"[^a-zA-Z0-9 ]+", '', str(item["name"]))
        f.write('[' + str(item["appid"]) +  ', "' + sos + '"]')

    count += 1

f.write("]}}")
f.close()

f = open("testsave.json", "r")
response_data_save = f.read()
response_data_save = json.loads(response_data_save)

#-----------------------------------------------------------------------------------------------------------------------------








#sort ids--------------------------------------------------------------------------------------------------
def sort_ids():
    f = open("testsave.json", "r")
    response_data_save = f.read()
    response_data_save = json.loads(response_data_save)

    lst = []
    for item in response_data_save["applist"]["apps"]:
        lst.append(item[0])

    def mergeSort(lst):
        if len(lst) > 1:
            mid = len(lst)//2
            L = lst[:mid]
            R = lst[mid:]
            mergeSort(L)
            mergeSort(R)

            i = j = k = 0

            while i < len(L) and j < len(R):
                if L[i] <= R[j]:
                    lst[k] = L[i]
                    i += 1
                else:
                    lst[k] = R[j]
                    j += 1
                k += 1

            while i < len(L):
                lst[k] = L[i]
                i += 1
                k += 1

            while j < len(R):
                lst[k] = R[j]
                j += 1
                k += 1

    mergeSort(lst)

    f = open('sorted_ids.json', 'w')
    f.write('{"applist": {"apps":[')
    f.close()

    count = 0

    f = open('sorted_ids.json', 'a')
    for item in lst:
        if count != len(lst)-1:
            f.write('"' + str(item) + '",')
        else:
            f.write('"' + str(item) + '"')

        count += 1

    f.write("]}}")
    f.close()

sort_ids()
#-----------------------------------------------------------------------------------------------------------------------------








#load games and friends of the user--------------------------------------------------------------------------------------------------

def load_user_data(steam_id):
    global user_games
    global user_friends
    global friend_info
    resource_uri = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=32D90521B5D10D656EF5AEBD9CCE5A16&steamid={}".format(steam_id)
    response = requests.get(resource_uri)
    try:
        user_friends = response.json()["friendslist"]["friends"]
    except:
        pass

    resource_uri = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=32D90521B5D10D656EF5AEBD9CCE5A16&steamid={}&format=json".format(steam_id)
    response = requests.get(resource_uri)
    user_games = response.json()["response"]["games"]

    friends = []
    friend_info = []
    for item in user_friends:
        friends.append(item["steamid"])

    for item in friends:
        resource_uri = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=32D90521B5D10D656EF5AEBD9CCE5A16&format=json&steamids={}".format(int(item))
        response = requests.get(resource_uri)
        try:
            friend_info.append([item, response.json()["response"]["players"]])
        except:
            pass

#-----------------------------------------------------------------------------------------------------------------------------





    
def load_user_data_game(steam_id, game_id):
    resource_uri = "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={}&key=32D90521B5D10D656EF5AEBD9CCE5A16&steamid={}&l=en".format(game_id, steam_id)
    response = requests.get(resource_uri)
    achievements = response.json()["playerstats"]["achievements"]

    resource_uri = "https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={}&format=json".format(game_id)
    response = requests.get(resource_uri)
    glob_achievements = response.json()["achievementpercentages"]["achievements"]

    back_product = {
        "achieve" : achievements,
        "glob_achieve" : glob_achievements,
    }

    return back_product



def get_api_by_nummer(api_item):
    #api_item = 1000 #geeft aan hoeveelste item van de opgehaalde data je wilt gebruiken
    app_id = response_data_save['applist']["apps"][api_item][0]
    return(get_api_info(app_id))

#def get_api_info_basic(api_item):
#    return_lst = {
#    "steam_appid" : response_data_save['applist']["apps"][api_item][0],
#    "name" : response_data_save['applist']["apps"][api_item][1],
#    }
#    return return_lst

def get_api_info_basic(api_item):
    f = open("sorted_ids.json", "r")
    response_data_ = f.read()
    response_data_ = json.loads(response_data_)

    use_id = response_data_['applist']["apps"][api_item]

    for item in response_data_save['applist']["apps"]:
        if item[0] == int(use_id):
            return_lst = {
            "steam_appid" : item[0],
            "name" : item[1],
            }
    
    return return_lst


print(get_api_info_basic(10))

#get game details--------------------------------------------------------------------------------------------------

#geef de app id op en krijg alle data terug in een json format. gebruik: hoe duur is app 1816550 --> print(get_api_info(1816550)["price"])
#de meeste items die meer dan 1 value terug geven zijn door een ";" gescheiden. alleen de genre is gescheiden door ", ".
def get_api_info(app_id):
    resource_uri = "http://store.steampowered.com/api/appdetails?appids={}".format(app_id)
    response = requests.get(resource_uri)
    response_data = response.json()

    if response_data[str(app_id)]["success"] == False:
        return "error"

    base_api_data = response_data[str(app_id)]["data"]
    api_info = ["steam_appid", "name", "release_date", "english", "developer", "publisher", "platforms", "required_age", "categories", "genres", "steamspy_tags", "achievements", "positive_ratings", "negative_ratings", "average_playtime", "median_playtime",  "owners",  "price"]


    def English_support():
        try:
            if "English" in base_api_data["supported_languages"]:
                return True

        except:
            return "unknown"
        
    def developers():
        developers = ""
        try:
            for item in base_api_data["developers"]:
                    developers = developers + item + ';'

            return developers
        except:
            return "unknown"

    def publishers():
        publishers = ""
        try:
            for item in base_api_data["publishers"]:
                    publishers = publishers + item + ';'

            return publishers
        except:
            return "unknown"

    def platforms():
        try:
            platforms = ""
            for item in base_api_data["platforms"]:
                if base_api_data["platforms"][item] == True:
                        platforms = platforms + item + ';'

            return platforms

        except:
            return "unknown"

    def categories():
        try:
            categories = ""
            for item in base_api_data["categories"]:
                categories = categories + item["description"] + ';'

            return categories
        
        except:
            return "unknown"

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
    
    def price():
        if base_api_data["is_free"] == True:
            return 0
        else:
            try:
                return base_api_data["price"]["final_formatted"]
            except:
                return "unknown"

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
        "price" : price()
    }

    return return_lst
#-----------------------------------------------------------------------------------------------------------------------------