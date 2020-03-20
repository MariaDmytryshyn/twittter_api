import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter



# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def acc_n(name):
    while True:
        acct = name
        if (len(acct) < 1): break
        url = twurl.augment(TWITTER_URL,
                            {'screen_name': acct, 'count': '1000'})
        connection = urllib.request.urlopen(url, context=ctx)
        data = connection.read().decode()

        js = json.loads(data)
        if len(js) > 1:
            break


def find_location(js):
    lst_with_friends = js['users']
    dict_with_friends = {}
    for i in lst_with_friends:
        dict_with_friends[i['location']] = i['screen_name']
    return dict_with_friends


dict_with_location = {}
friend_location = find_location(js)
locations = list(find_location(js).keys())
geolocator = Nominatim(user_agent="specify_your_app_name_here")
geolocator = Nominatim(timeout=100)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
dict_with_location = {}
for point in locations:
    try:
        location = geolocator.geocode(point)
        dict_with_location[(location.latitude, location.longitude)] = friend_location[point]
        if len(dict_with_location) == 1000:
            break
    except AttributeError:
        pass


map = folium.Map(location=[48.314775, 25.082925], zoom_start=2)
fg_hc = folium.FeatureGroup(name="Friends")

for loc in dict_with_location:
        fg_hc.add_child(folium.CircleMarker(location=[loc[0], loc[1]],
                                            radius=10,
                                            popup=dict_with_location[loc],
                                            fill_color='red',
                                            color='red',
                                            fill_opacity=2))


map.add_child(fg_hc)
map.add_child(folium.LayerControl())

map.save('My_world_map_with_friends_locations.html')


