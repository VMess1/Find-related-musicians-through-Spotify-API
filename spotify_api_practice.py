from dotenv import load_dotenv
import os
import requests

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
AUTH_URL = 'https://accounts.spotify.com/api/token'

#The Spotify API has different call methods depending on the data you want to receive. 
#The client credientials API does not access user info on spotify, but only what is searchable
#on the main app
#This is the API that this programme uses as to access user information we need to have authorisation
#from the user, this is slightly more complex to set up.

#Spotify documentation specifies that we need to request an access token first of all, before we 
#can access the API data. 
#https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow

def get_token():
    auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    })
    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
    return access_token


def make_authorization(token):
    headers = {
        f"Authorization": "Bearer {token}".format(token=token)
    }
    return headers


def find_artist_by_id(artist_id, headers):
    endpoint = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = headers
    response = requests.get(endpoint, headers=headers)
    return response.json()


def find_related_artists(artist_id, headers):
    endpoint = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
    headers = headers
    response = requests.get(endpoint, headers=headers)
    return response.json()


def print_related_artists(data):
    for artist in data['artists']:
        print("\n" + artist['name'])
        print("Genres: ", end="")
        for genre in artist['genres']:
            print(genre.title(), end=", ")
        print("\n" + f"{artist['followers']['total']}", "followers")


def find_artist_by_search(headers):
    artist_name= input("Name an artist that you like and we'll try to find other bands you may enjoy: ")
    artists = artist_name.split()
    search_term = "%20".join(artists)
    headers=headers
    query = f"q={search_term}"
    type = "&type=artist"
    url = f"https://api.spotify.com/v1/search?{query}{type}"
    response = requests.get(url, headers=headers)
    return response.json()


def get_id_by_search():
    token = get_token()
    global headers
    headers = make_authorization(token)
    data = find_artist_by_search(headers)
    print(f"\nYou searched for: {data['artists']['items'][0]['name']}")
    print("You may like the following artists:")
    return data['artists']['items'][0]['id']


def find_related_artists_by_search():
    id = get_id_by_search()
    data = find_related_artists(id, headers)
    print_related_artists(data)

find_related_artists_by_search()