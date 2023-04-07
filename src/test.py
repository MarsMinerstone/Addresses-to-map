import pandas as pd
from geopy import Nominatim, location
import gspread
# from pandas.core.internals.blocks import replace_regex

from pprint import pprint
import folium

import googlemaps
from gmplot import gmplot

replace_list = ('д. ', 'д ', 'ул. ', 'Ул. ', 'ул ', "Ул ")
def add_value(x):
	t = str(x)
	for i in replace_list:
		t = t.replace(i, ' ')

	return 'Красноярск, ' + t


def main():
	# locator = Nominatim(user_agent="myGeocoder")
	# location = locator.geocode("Красноярск, Красномосковская 64")

	# print(location)
	# print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))


	# gc = gspread.service_account(filename='account.json')
	# sh = gc.open("Контактная_информация2").sheet1
	# df = pd.DataFrame(sh.get_all_records())
	# df.head()

	# df['address'] = df['Адрес'].apply(add_value)
	# pprint(df)

	# from geopy.extra.rate_limiter import RateLimiter

	# # 1 - conveneint function to delay between geocoding calls
	# geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
	# # 2- - create location column
	# df['location'] = df['address'].apply(geocode)
	# # 3 - create longitude, laatitude and altitude from location column (returns tuple)
	# df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)
	# # 4 - split point column into latitude, longitude and altitude columns
	# df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)
	# pprint(df)

	# df.to_csv('data.csv', index=False)

	df = pd.read_csv("data.csv")
	df.head()

	df=df.dropna(subset=['point'])

	map1 = folium.Map(center = [56.021339, 92.897769], zoom_start = 12)
	df.apply(lambda row: folium.CircleMarker(location=[row["latitude"], row["longitude"]]).add_to(map1), axis=1)
	# map1.showMap()
	map1.save("map.html")


def main2():

	df = pd.read_csv("data.csv")
	df.head()

	df=df.dropna(subset=['point'])

	# Set up Google Maps API client
	gmaps = googlemaps.Client(key='{{YOUR_API_KEY}}')

	# Geocode addresses
	df['Location'] = df['Адрес'].apply(lambda x: gmaps.geocode(x)[0]['geometry']['location'])

	# Plot locations on map
	gmap = gmplot.GoogleMapPlotter.from_geocode("California")
	for location in df['Location']:
	    gmap.marker(location['lat'], location['lng'])
	gmap.draw("map.html")

if __name__ == '__main__':
	main()
