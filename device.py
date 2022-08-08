import requests
import json
from refresh import Refresh

ACCESS_TOKEN = str(Refresh().refresh())

class Device:

	def __init__(self):
		self.access_token = ACCESS_TOKEN
		self.available_devices_url = 'https://api.spotify.com/v1/me/player/devices' 

	def device(self):

		response = requests.get(
			self.available_devices_url,
			headers={
				"Authorization": f"Bearer {ACCESS_TOKEN}"
			}
		)
		json_resp = response.json()
		for device in json_resp['devices']:
			if device['is_active'] == True:
				return device['id']
		
a = Device()
a.device()