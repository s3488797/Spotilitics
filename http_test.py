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
encoded_data = urllib.urlencode(data)
r = requests.post(target_url, data=data, headers=headers)
print(r.status_code, r.reason)
r_data = json.loads(r.text)
print(r_data["access_token"])
