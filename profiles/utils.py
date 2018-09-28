import requests

def get_location_from_ip(ip_address):
	try:
		response = requests.get(f"http://ip-api.com/json/{ip_address}")
		return response.json()
	except Exception as e:
		print(e)
