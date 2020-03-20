import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    acct = input('Enter Twitter Account:')
    if len(acct) < 1:
        break
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '1000'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)
    if len(js) > 1:
        break


def get_information(json_file):
    first_el = input('Which key you want to get? \n users   next_cursor  next_cursor_str  previous_cursor\
    previous_cursor_str   total_count \n')
    lst_with_main_keys = ['next_cursor', 'next_cursor_str', 'previous_cursor', 'previous_cursor_str',\
                          'total_count']
    if first_el in lst_with_main_keys:
        return json_file[first_el]
    elif first_el == 'users':
        lst_with_friends = []
        for i in json_file[first_el]:
            lst_with_friends.append(i["screen_name"])
        str_with_friends = ''
        for i in lst_with_friends:
            str_with_friends += i + '  | '
        print(str_with_friends[:-1])
        friend = input("Which friend do you want to chose? \n ")
        if friend not in lst_with_friends:
            return 'YOU CHOSE INCORRECT PERSON!'
        else:
            indexes = lst_with_friends.index(friend)
            dictionary = json_file[first_el][indexes]
            keeys = list(dictionary.keys())
            str_with_keys = ''
            for i in keeys:
                str_with_keys += i + ' |  '
            print(str_with_keys)
            Key = input('Which key do you want to choose? \n' )
            if (Key != 'entities') and (Key != 'status'):
                res = str(json_file[first_el][indexes][Key])
                return "Information, that you wanted:  \n" + res
            elif Key == 'entities':
                entities = input('url  |  description \n Choose, please \n ')
                if entities == 'url':
                    urls = input("url  |  expanded_url  |  display_url  |  indices \n Whan do you choose? \n")
                    res = str(json_file[first_el][indexes][Key][entities]['urls'][0][urls])
                    return "Information, that you wanted:  \n" + res
                elif entities == 'description':
                    description = input("url  |  expanded_url  |  display_url  |  indices \n Whan do you choose?\n ")
                    res = str(json_file[first_el][indexes][Key][entities]['urls'][0][description])
                    return "Information, that you wanted:  \n" + res
            elif Key == 'status':
                k = list(json_file[first_el][indexes][Key].keys())
                l_with_s_keys = ''
                for i in k:
                    l_with_s_keys += i + " | "
                print(l_with_s_keys)
                status = input('What do you choose? \n')
                if status != 'entities':
                    res = str(json_file[first_el][indexes][Key][status])
                    return "Information, that you wanted:  \n" + res
                elif status == 'entities':
                    ent_keys = list(json_file[first_el][indexes][Key][status].keys())
                    s_w_k = ''
                    for i in ent_keys:
                        s_w_k += i + ' | '
                    print(s_w_k)
                    keeeey = input("What will you choose? \n ")
                    res = str(json_file[first_el][indexes][Key][status][keeeey])
                    return "Information, that you wanted:  \n" + res



print(get_information(js))