import csv
import os
import requests

api_key = ""

try:
    os.remove("geocode_output.txt")
except OSError:
    pass
with open("Parking_Violations_Issued_-_Fiscal_Year_2018.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    with open("geocode_output.csv", "w") as result:
        count = 0
        for entry in csv_reader:
            if count == 0:
                result.write("house_number,street_name,intersecting_street,latitude,longitude\n")
            if count != 0:
                house_number = entry[23]
                street_name = entry[24]
                intersecting_street = entry[25]
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
            count = count + 1
            if count > 300:
                break
