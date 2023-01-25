import requests # voor de API
import json
import re

resource_uri = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json"
response = requests.get(resource_uri)
response_data_save = response.json()

f = open('testsave.json', 'w')
f.write('{"applist": {"apps":[')
f.close()

count = 0
percent = 0

f = open('testsave.json', 'a')
for item in response_data_save['applist']['apps']:

    if round(100/len(response_data_save['applist']['apps'])*(count + 1)) != percent:
        percent = round(100/len(response_data_save['applist']['apps'])*(count + 1))
        print(str(percent) + "%")

    if count != len(response_data_save['applist']['apps'])-1:
        try:
            sos = re.sub(r"[^a-zA-Z0-9 ]+", '', str(item["name"]))
            if str(item["name"]) != "":
                f.write('{"appid":' + str(item["appid"]) +  ',"name":"' + sos + '"},')
        except:
            pass
    else:
        sos = re.sub(r"[^a-zA-Z0-9 ]+", '', str(item["name"]))
        f.write('{"appid":' + str(item["appid"]) +  ',"name":"' + sos + '"}')

    count += 1

f.write("]}}")
f.close()

f = open("testsave.json", "r")
response_data_save = f.read()
response_data_save = json.loads(response_data_save)

def get_api_by_nummer(api_item):
    #api_item = 1000 #geeft aan hoeveelste item van de opgehaalde data je wilt gebruiken
    app_id = response_data_save['applist']["apps"][api_item]["appid"]
    return(get_api_info(app_id))

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