import tidalapi
import spotipy
from tidalapi import Session
from spotipy.oauth2 import SpotifyOAuth
def auth_tidal():
    print("starting")
    print("getting auth token")
    session = tidalapi.Session()
    session.login_oauth_simple()
    print(session.check_login())
    if session.check_login():
        print("Tidal OK!")
        return session
    else:
        print("Tidal ERROR!")
        exit(1)

def auth_spotify(clientID: str, clientSecret: str):
    print(clientID)
    print(clientSecret)
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(open_browser=False, scope="user-library-read, user-library-modify, playlist-modify-public, playlist-modify-private", client_id=clientID, client_secret=clientSecret, redirect_uri="http://localhost"))
    if sp.current_user()['display_name'] != "":
        print("Spotify Seems To Be OK!")
        return sp
    else:
        print("Spotify ERROR!")
        exit(1)

# Tidal saved songs ---> Spotify saved songs OR playlist
def parse_fav(tidal_session: Session, userID: int, spotifyAuth):
    tracklist = tidalapi.Favorites(session=tidal_session, user_id=userID).tracks()
    print(len(tracklist))
    # idlist = [] # uncomment to do batch (will crash if theres too many items)
    for track in tracklist:
        full = str(track.name) + " - " + str(track.artist.name) + " - " + str(track.id)
        print(full)
        q = "track:" + str(track.name) + " artist:" + str(track.artist.name)
        print(q)
        u = spotifyAuth.search(type="track", market="AU", q=q, limit=1)
        print(u)
        if u["tracks"]["total"] == 0:
            print("unable to find")
            with open("error.txt", "a") as file:
                file.write("\n" + str(full))
        else:
            for item in u['tracks']['items']:
                print(item["id"])
                # idlist.append(item['id']) # uncomment for batch
                # spotifyAuth.playlist_add_items(playlist_id="PLAYLISTID HERE CHANGHE ME IF NOT COMMENTED OUT!!", items=[item["id"]]) # UNCOMMENT IF YOU WANT THE SONGS TO GO TO A SPOTIFY PLAYLIST, PUT PLAYLIST ID HERE ALSO (THE ID IN URL BAR WHEN YOU CLICK ON THE PLAYLIST ON SPOTIFY WEBUI) - this one adds songs one by one
                spotifyAuth.current_user_saved_tracks_add(tracks=[item["id"]]) # COMMENT IF YOU DONT WANT IT TO "LIKE" THE SONGS ON SPOTIFY

    # print(idlist) # debugging :P
    # spotifyAuth.playlist_add_items(playlist_id="PLAYLISTID HERE CHANGHE ME IF NOT COMMENTED OUT!!", items=idlist) # uncomment for batch, same as above change the playlist_id


# Tidal playlist > Spotify saved songs OR playlist
def parse(tidal_session: Session, playlistID: str, spotifyAuth):
    a = tidalapi.playlist.UserPlaylist(session=tidal_session, playlist_id=playlistID)
    print(a.num_tracks)
    tracks = a.tracks()
    # tracklist = [] # uncomment to do batch (will crash if theres too many items)
    for track in tracks:
        print(track.name + " - " + str(track.artist.name))
        q = "track:" + str(track.name) + " artist:" + str(track.artist.name)
        print(q)
        u = spotifyAuth.search(type="track", market="AU", q=q, limit=1)
        print(u)
        if u["tracks"]["total"] == 0:
            print("unable to find")
        else:
            for item in u['tracks']['items']:
                print(item["id"])
                # idlist.append(item['id']) # uncomment for batch
                # spotifyAuth.playlist_add_items(playlist_id="PLAYLISTID HERE CHANGHE ME IF NOT COMMENTED OUT!!", items=[item["id"]]) # UNCOMMENT IF YOU WANT THE SONGS TO GO TO A SPOTIFY PLAYLIST, PUT PLAYLIST ID HERE ALSO (THE ID IN URL BAR WHEN YOU CLICK ON THE PLAYLIST ON SPOTIFY WEBUI) - this one adds songs one by one
                spotifyAuth.current_user_saved_tracks_add(tracks=[item["id"]])  # COMMENT IF YOU DONT WANT IT TO "LIKE" THE SONGS ON SPOTIFY
    # print(idlist) # debugging :P
    # spotifyAuth.playlist_add_items(playlist_id="PLAYLISTID HERE CHANGHE ME IF NOT COMMENTED OUT!!", items=idlist) # uncomment for batch, same as above change the playlist_id


if __name__ == '__main__':
    spotifyauth = auth_spotify(clientID="PUT SPOTIFY CLIENT ID HERE, GET ON SPOTIFY DEV WEBSITE", clientSecret="SPOTIFY CLIENT SECRET HERE, GET ON SAME DEV WEBSITE")
    tidalauth = auth_tidal()
    # parse(tidal_session=tidalauth, playlistID="SOURCE TIDAL PLAYLIST ID", spotifyAuth=spotifyauth) # uncomment for playlist > spotify
    parse_fav(tidal_session=tidalauth, userID=your tidal user id here as an int open webui tidal and click your profile top left id is in url, spotifyAuth=spotifyauth) # liked > spotify
