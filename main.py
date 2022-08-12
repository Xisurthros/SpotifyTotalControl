import requests
from pprint import pprint
from device import Device # Checks which Device is currently being used by spotify
from refresh import Refresh # Auto Refreshes Spotify OAUTH token
from json.decoder import JSONDecodeError

# URLS can be found throughout https://developer.spotify.com/console/

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
NEXT_URL = 'https://api.spotify.com/v1/me/player/next'
PREVIOUS_URL = 'https://api.spotify.com/v1/me/player/previous'
PAUSE_URL = 'https://api.spotify.com/v1/me/player/pause'
PLAY_URL = 'https://api.spotify.com/v1/me/player/play'
RECENT_TRACKS = 'https://api.spotify.com/v1/me/player/recently-played'
SAVED_TRACKS = 'https://api.spotify.com/v1/me/tracks'
VOLUME = 'https://api.spotify.com/v1/me/player/volume'
TOP = '	https://api.spotify.com/v1/me/top/'
USER_PLAYLISTS = '	https://api.spotify.com/v1/me/playlists'

DEVICE_ID = Device().device() # Checks which Device is currently being used by spotify

def help():
	print('[get_current_track] to get live track updates to your currently playing')
	print('[recent] to get information your recently played list\n\t(songs must be played for at least 30 seconds to be considered recently played)')
	print('[top] to get your top listened to artists')
	print('[saved] to get the total number and list of all artists that you have saved song for')
	print('[next] go to the next audio in the queue')
	print('[previous] go to the previous audio')
	print('[pause] pause currently playing audio')
	print('[play] play the currently paused audio')
	print('[volume] to change the volume in the spotify application')
	print('[search_artist] seach for an artist')
	print('[search_song] search for a song')

def get_current_track():
	print('Ctr-C to get out of currently-playing\n')
	current_track_id = None
	while True:
		try:
			response = requests.get(
				SPOTIFY_GET_CURRENT_TRACK_URL,
				headers={
				    "Authorization": f"Bearer {ACCESS_TOKEN}"
				}
			)
			json_resp = response.json()
		
			track_id = json_resp['item']['id']
			track_name = json_resp['item']['name']
			artists = [artist for artist in json_resp['item']['artists']]
		
			link = json_resp['item']['external_urls']['spotify']
		
			artist_names = ', '.join([artist['name'] for artist in artists])
		
			current_track_info = {
				"id": track_id,
				"track_name": track_name,
				"artists": artist_names,
				"link": link
			}
	
			if current_track_info['id'] != current_track_id:
				pprint(
					current_track_info,
					indent=4,
				)
				current_track_id = current_track_info['id']
		except KeyboardInterrupt:
			break

def recent():
	songs = []
	artists = []
	x = 0

	response = requests.get(
			RECENT_TRACKS,
			headers={
			    "Authorization": f"Bearer {ACCESS_TOKEN}"
			}
		)
	json_resp = response.json()
	for item in json_resp['items']:
		print(f"{item['track']['album']['artists'][0]['name']}: {item['track']['name']}")

def top():
	while True:
		try:
			user_input = input('Enter(artists, tracks): ')
			user_input = user_input.lower()
			response = requests.get(
				TOP + f'{user_input.lower()}',
				headers={
				    "Authorization": f"Bearer {ACCESS_TOKEN}"
				}
			)
			json_resp = response.json()
			if user_input == 'artists':
				for item in json_resp['items']:
					artist = item['name']
					followers = item['followers']['total']
					genres = item['genres']
					popularity = item['popularity']
					print(f'NAME: {artist}\n     FOLLOWERS: {followers}\n     GENRES: {genres}\n     POPULARITY {popularity}')
					break
			elif user_input == 'tracks':
				for item in json_resp['items']:
					artist = item['artists'][0]['name']
					song = item['name']
					print(f'SONG: {song} | ARTIST: {artist}')
					break
		except JSONDecodeError:
			print('Invalid Error\nTry again with (artists or tracks)')

def saved():
	artists = []
	cleaned = []
	x = 0
	for i in range(50):
		response = requests.get(
				f'{SAVED_TRACKS}?limit=50&offset={x}',
				headers={
				    "Authorization": f"Bearer {ACCESS_TOKEN}"
				}
			)
		json_resp = response.json()
		for item in json_resp['items']:
			artist = item['track']['album']['artists'][0]['name']
			if artist in artists:
				pass
			else:
				artists.append(artist)
		x += 50

	print(sorted(artists)[1:])
	print(f'Total Artists: {len(artists)}')

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

def search_artist():
	cleaned = ''
	user_input = input('Enter artist name: ')
	for item in user_input.split(' '):
		cleaned += (f'{item}%')
	cleaned
	response = requests.get(
		f"https://api.spotify.com/v1/search?q=artist:{cleaned}&type=artist",
		headers={
			    "Authorization": f"Bearer {ACCESS_TOKEN}"
			}
		)
	json_resp = response.json()
	for item in json_resp['artists']['items']:
		name = item['name']
		popularity = item['popularity']
		genre = item['genres']
		followers = item['followers']['total']
		print(f'NAME: {name} FOLLOWERS: {followers} GENRE: {genre} POPULARITY: {popularity}')

def search_song():
	cleaned = ''
	user_input = input('Enter song name: ')
	for item in user_input.split(' '):
		cleaned += (f'{item}%')
	cleaned
	response = requests.get(
		f"https://api.spotify.com/v1/search?q=track:{cleaned}&type=track",
		headers={
			    "Authorization": f"Bearer {ACCESS_TOKEN}"
			}
		)
	json_resp = response.json()
	for item in json_resp['tracks']['items']:
		song = item['name']
		artist = item['album']['artists'][0]['name']
		uri = item['uri']
		print(f'SONG: {song} ARTIST: {artist} URI: {uri}')

def my_playlists():
	offset = 0
	playlists = []
	for num in range(4):
		response = requests.get(
			f'{USER_PLAYLISTS}?limit=50&offset={offset}',
			headers={
				    "Authorization": f"Bearer {ACCESS_TOKEN}"
				}
			)
		offset+=50
		json_resp = response.json()
		for item in json_resp['items']:
			playlist = {
				'name': item['name'],
				'owner': item['owner']['display_name'],
				'description': item['description'],
				'id': item['id'],
				'track_amount': item['tracks']['total']
			}
			if playlist in playlists:
				pass
			else:
				playlists.append(playlist)
	for playlist in playlists:
		print(f'Name: {playlist["name"]} | ID: {playlist["id"]}')
	print(f'You have: {len(playlists)} playlists')

def main():
	print('Enter HELP for controls')

	while True:
		user_input = input("Enter: ")
		user_input = user_input.lower()

		if user_input == 'help':
			help()
		elif user_input == 'next':
			next()
		elif user_input == 'previous':
			previous()
		elif user_input == 'pause':
			pause()
		elif user_input == 'play':
			play()
		elif user_input == 'volume':
			volume()
		elif user_input == 'current':
			get_current_track()
		elif user_input == 'recent':
			recent()
		elif user_input == 'top':
			top()
		elif user_input == 'saved':
			saved()
		elif user_input == 'search_artist':
			search_artist()
		elif user_input == 'search_song':
			search_song()
		elif user_input == 'my_playlists':
			my_playlists()
		else:
			print('Invalid Entry. Try Again.\n')

if __name__ == '__main__':
	ACCESS_TOKEN = str(Refresh().refresh()) # Auto Refreshes Spotify OAUTH token
	main()