import csv
import json
import re
import folium
import time
from geopy.geocoders import Nominatim

from main_app.app_variables.variables import RAW_COUNTRIES_COORDINATES, COUNTRIES_COORDINATES, MAIN_CSV_DS_PATH
from main_app.generic.generic_funcs import get_coords_by_country_name


def get_countries_coord():
    with open(COUNTRIES_COORDINATES) as file:
        return json.load(file)


def json_country_coords():
    country_coords = {}
    with open(MAIN_CSV_DS_PATH) as file:
        details = csv.DictReader(file)
        countries = {c['country_txt'] for c in details}
        for country in countries:
            res = re.sub(r"\((.*?)\)", "", country)
            loc = get_coords_by_country_name(res)
            if loc:
                loc = loc.raw
                time.sleep(1)
                country_coords[country] = {'lat': loc['lat'], 'lon': loc['lon']}
                print(f'Added {country} to countries dict')
        with open(COUNTRIES_COORDINATES, 'w') as clean_json:
            json.dump(country_coords, clean_json)
    print('Finished adding all coords to countries file')


def view_top_orgs_by_country(df):
    map_zoo = folium.Map(location=[45, 20], zoom_start=4)
    terror_data = False
    counter = 0
    for i in range(len(df.index)):
        country = df.iloc[counter]['country']
        country_coord = get_countries_coord().get(country)
        if country_coord is None:
            counter += 1
            continue
        terror_data = f'Country: {country}.\nTerror organizations:\n'
        while df.iloc[counter]['country'] == country and counter < len(df) - 1:
            terror_data += f'{df.iloc[counter]["org"]},\n'
            counter += 1
        folium.Marker(location=(country_coord['lat'], country_coord['lon']),
                      popup=terror_data,
                      tooltip='Click for more information!').add_to(map_zoo)
        if counter == len(df) - 1:
            break
    if not terror_data:
        return None
    return map_zoo




# The following functions are a backup, in case 'geopy' does not work
def clean_json_coord():
    with open(RAW_COUNTRIES_COORDINATES) as raw_json:
        all_data = json.load(raw_json)
        all_coord = all_data['features']
        coord_dict = {}
        for country in all_coord:
            coord = country['geometry']['coordinates']
            coord_dict[country['properties']['name']] = coord[0][0] if isinstance(coord[0][0][0], float) else coord[0][0][0]
        with open(COUNTRIES_COORDINATES, 'w') as clean_json:
            json.dump(coord_dict, clean_json)

def view_top_orgs_by_country_backup(df):
    print('Started view_top_orgs_by_country func')
    map_zoo = folium.Map(location=[45, 20], zoom_start=4)
    terror_data = False
    all_countries_coord = get_countries_coord()
    counter = 0
    print(len(df))
    print(df.tail())
    for i in range(len(df.index)):
        country = df.iloc[counter]['country']
        print(f'First country: {country}')
        country_coord = all_countries_coord.get(country)
        if country_coord is None:
            counter += 1
            continue
        terror_data = f'Country: {country}\nTerror organizations:\n'
        print(f'country before while: {df.iloc[counter]["country"]}')
        while df.iloc[counter]['country'] == country and counter < len(df) - 1:
            terror_data += f'{df.iloc[counter]["org"]}|\n'
            counter += 1
            print(counter)
        folium.Marker(location=(country_coord[0], country_coord[1]),
                      popup=terror_data,
                      tooltip='Click for more information!').add_to(map_zoo)
        if counter == len(df) - 1:
            break
    if not terror_data:
        return None
    print('Before map_zoo')
    return map_zoo


if __name__ == '__main__':
    # json_country_coords()
    geolocator = Nominatim(user_agent="my_geopy_app")
    print(geolocator.geocode('Germany', exactly_one=True).raw)