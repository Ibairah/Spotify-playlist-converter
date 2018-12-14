import json
from selenium import webdriver
import sys
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

# spotify client id: e41c7a0b58f3413bac2df91e18c23976
# spotify client secret: aac1c90fef7f45da9cbfc68a9131df39

# spotify playlist id: 5qHBXW7kDtTAJxasGtgotm
# POST https://api.spotify.com/v1/playlists/{playlist_id}/tracks add tracks to playlist

def create_song_txt(playlist):
    """
    Accept a list of netease playlist IDs
    Create a .txt file containing all the songs from the playlists
    """
    # playlist = ['142142431', '914893430', '639479361', '541205162']

    with open('playlist.txt', 'w', encoding='utf-8') as file:
        for playlistId in playlist:
            url = "http://music.163.com/api/playlist/detail?id=%s" % playlistId

            driver = webdriver.PhantomJS()
            driver.get(url)

            source = driver.find_element_by_tag_name("pre").text
            data = json.loads(source)

            tracks = data["result"]["tracks"]

            for track in tracks:
                # print(track)
                trackName = track["name"]
                artist = track["artists"][0]["name"]
                s = trackName + ' - ' + artist + '\n'
                file.write(s)

        print('Success')

client_credentials_manager = SpotifyClientCredentials(client_id='e41c7a0b58f3413bac2df91e18c23976',
                                                      client_secret='aac1c90fef7f45da9cbfc68a9131df39')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

netease = open('netease.txt', 'r').readlines()
for line in netease[:1]:
    song = line.split('-')[0]
    results = sp.search(q=song, limit=1, type='track')
    try:
        song_uri = results['tracks']['items'][0]['uri']
        print(song_uri)
    except IndexError:
        print(song)
