from config import MY_API_KEY
import requests
import csv
import json

def main():
    params = get_params()
    data = get_data(params)
    print(data.text)

    
def get_params():
    params = {}
    params["term"] = "restaurant"
    params["location"] = "Allegheny County"
    params["limit"] = 50
    params["offset"] = 500
    return params

def get_data(params):
    headers = {'Authorization': 'Bearer %s' % MY_API_KEY}
    url = 'https://api.yelp.com/v3/businesses/search'
    return requests.get(url, params=params, headers=headers)
    


if __name__ == "__main__":
    main()