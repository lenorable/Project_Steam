import requests # voor de API
resource_uri = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json"
response = requests.get(resource_uri)
response_data_save = response.json()

def get_api_by_nummer(api_item):
    #api_item = 1000 #geeft aan hoeveelste item van de opgehaalde data je wilt gebruiken
    return response_data_save['applist']["apps"][api_item]["name"]

lst = [730, 570, 578080, 1172470, 1568590, 271590, 431960, 440, 1203220, 304930, 1938090, 252490, 1085660, 236390, 1245620, 346110, 1904540, 289070, 230410, 1811260]

lst.sort()
print(response_data_save)

for item in lst:
    print(item)
    print(response_data_save['applist']["apps"][item])
    print(get_api_by_nummer(item))