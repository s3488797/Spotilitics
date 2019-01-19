import urllib, httplib, requests, base64, json

CLIENT_ID = "4f2c1f999a4c480f9d9eea2f82b53723"
CLIENT_SECRET = "ba1c5975884d4ba080e84b8540b1bc6a"
encoded = base64.b64encode(CLIENT_ID + ":" + CLIENT_SECRET)
header_string = "Basic " + encoded
target_url = "https://accounts.spotify.com/api/token"
data = {
    'grant_type': "client_credentials"
}
headers = {
    'Authorization': header_string
}
r = requests.post(target_url, data=data, headers=headers)
print(r.status_code, r.reason)
if (r.status_code == 200):
    print("Got auth token")
    r_data = json.loads(r.text)
    access_token = r_data["access_token"]
    headers = {
        'Authorization': "Bearer "+access_token
    }
    endpoint = "https://api.spotify.com/v1/search"
    payload = {
        'q': "Less i know the better",
        'type': "track",
        'limit': "3"
    }
    get_string = endpoint + "?" + urllib.urlencode(payload)
    print(get_string)
    s = requests.get(get_string, headers=headers)
    print(s.status_code, s.reason)
    search_results = json.loads(s.text)
    for item in search_results['tracks']['items']:
        print(item['name'] + ", ID: " + item['id'])
