import requests

def get_location_from_ip(ip_address):
	try:
		response = requests.get(f"http://ip-api.com/json/{ip_address}")
		city = response.get("city")
		country_code = response.get("countryCode")
		return f"{city} - {country_code}"
	except Exception as e:
		return "Failed fetching location"
