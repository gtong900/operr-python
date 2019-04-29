import os
import requests

api_key = ""
url = 'https://data.cityofnewyork.us/resource/9wgk-ev5c.json?$limit=5000&$offset=0'

try:
    os.remove("geocode_output.txt")
except OSError:
    pass

with open("geocode_output.csv", "w") as result:
    result.write("house_number,street_name,intersecting_street,latitude,longitude\n")
    csv_file = requests.get(url)
    for entry in csv_file.json():
        #fetch data from json entry
        house_number = ''
        street_name = ''
        intersecting_street = ''
        if 'house_number' in entry:
            house_number = entry['house_number']
        if 'street_name' in entry:
            street_name = entry['street_name']
        if 'intersecting_street' in entry:
            intersecting_street = entry['intersecting_street']

        # call geocode api
        address = house_number + " " + street_name + " " + intersecting_street
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}, New York, NY&key={}'.format(address,api_key)
        response = requests.get(url)
        json_data = response.json()
        lat = 'Unavailable'
        lng = 'Unavailbale'
        if len(json_data['results']) > 0:
            geometry_location = json_data['results'][0]['geometry']['location']
            lat = geometry_location['lat']
            lng = geometry_location['lng']
        result.write(house_number + "," + street_name + "," + intersecting_street + "," + str(lat) + "," + str(lng) + "\n")
