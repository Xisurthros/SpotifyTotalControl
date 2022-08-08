import requests, time

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
NEXT_URL = 'https://api.spotify.com/v1/me/player/next'
PREVIOUS_URL = 'https://api.spotify.com/v1/me/player/previous'
PAUSE_URL = 'https://api.spotify.com/v1/me/player/pause'
PLAY_URL = 'https://api.spotify.com/v1/me/player/play'
RECENT_TRACKS = 'https://api.spotify.com/v1/me/player/recently-played'
SAVED_TRACKS = 'https://api.spotify.com/v1/me/tracks'
VOLUME = 'https://api.spotify.com/v1/me/player/volume'
TOP = '	https://api.spotify.com/v1/me/top/'

main():
	pass

if __name__ == '__main__':
	ACCESS_TOKEN = str(Refresh().refresh())
	main()