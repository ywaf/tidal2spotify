# tidal2spotify
Script to move liked songs OR playlists from Tidal TO Spotify liked songs OR playlists

Tidal doesnt have an official API, this script uses a lib which is made from reverse engineered API's. This will probably stop working in the future 🤷‍♂️

# Usage
1. Read the code (main.py)
2. Install the dependencies in requirements.txt - ```pip3 install -r requirements.txt```
3. Get spotify oauth creds, [Here](https://developer.spotify.com/) - clientID and clientSecret
4. Put these in the code
5. Comment / Uncomment lines based on what you would like the script to do
6. Create a file ```error.txt``` in the same folder as the script - songs failed to be matched by Spotify API will be written here
7. Run the script
8. Check the desired output on Spotify
9. Profit?

# Libs used
https://github.com/tamland/python-tidal

https://github.com/spotipy-dev/spotipy

