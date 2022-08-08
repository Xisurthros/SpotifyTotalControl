import requests, time
from device import Device
from refresh import Refresh

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
NEXT_URL = 'https://api.spotify.com/v1/me/player/next'
PREVIOUS_URL = 'https://api.spotify.com/v1/me/player/previous'
PAUSE_URL = 'https://api.spotify.com/v1/me/player/pause'
PLAY_URL = 'https://api.spotify.com/v1/me/player/play'
RECENT_TRACKS = 'https://api.spotify.com/v1/me/player/recently-played'
SAVED_TRACKS = 'https://api.spotify.com/v1/me/tracks'
VOLUME = 'https://api.spotify.com/v1/me/player/volume'
TOP = '	https://api.spotify.com/v1/me/top/'

DEVICE_ID = Device().device()

def next():
	requests.post(
		NEXT_URL + f'?device_id={DEVICE_ID}',
		headers={
			"Authorization": f"Bearer {ACCESS_TOKEN}"
		}
	)

def previous():
	requests.post(
		PREVIOUS_URL + f'?device_id={DEVICE_ID}',
		headers={
			"Authorization": f"Bearer {ACCESS_TOKEN}"
		}
	)

def pause():
	requests.put(
		PAUSE_URL + f'?device_id={DEVICE_ID}',
		headers={
			"Authorization": f"Bearer {ACCESS_TOKEN}"
		}
	)

def play():
	requests.put(
		PLAY_URL + f'?device_id={DEVICE_ID}',
		headers={
			"Authorization": f"Bearer {ACCESS_TOKEN}"
		}
	)

def volume():
	vol = input('Volume: ')
	requests.put(
		f'{VOLUME}?volume_percent={vol}&' + f'device_id={DEVICE_ID}',
		headers={
			"Authorization": f"Bearer {ACCESS_TOKEN}"
		}
	)

def main():

	while True:
		user_input = input("Enter: ")
		user_input = user_input.lower()

		if user_input == 'next':
			next()
		elif user_input == 'previous':
			previous()
		elif user_input == 'pause':
			pause()
		elif user_input == 'play':
			play()
		elif user_input == 'volume':
			volume()

if __name__ == '__main__':
	ACCESS_TOKEN = str(Refresh().refresh())
	main()




#### git add but still need to commit
#### issues with signing