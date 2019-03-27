from config import MY_API_KEY
import requests
import csv
import json
import sys


def main():
    name = []
    rating = []
    prices = []
    review_count = []
    address = []
    zipcode = []
    food_type = []
    latitude = []
    longitude = []

    offset = 0
    for x in range(0, 15):
        offset = x
        params = get_params(offset)
        data = get_data(params)
        parsed = json.loads(data.text)
        businesses = parsed["businesses"]
        
        for business in businesses:
            if business["location"]["zip_code"][0:2] != "15":
                continue
            if business["categories"][0]["alias"] == "golf":
                continue
            if business["coordinates"]["latitude"] is None:
                continue
            if "price" not in business:
                continue 
            name.append(business["name"])
            rating.append(business["rating"])
            prices.append(business["price"])
            review_count.append(business["review_count"])
            address.append(business["location"]["address1"])
            zipcode.append(business["location"]["zip_code"])
            food_type.append(business["categories"][0]["alias"])
            latitude.append(business["coordinates"]["latitude"])
            longitude.append(business["coordinates"]["longitude"])

    to_csv(name, rating, prices, review_count, address, zipcode, food_type, latitude, longitude)   
    

    
def get_params(offset):
    params = {}
    params["term"] = "food"
    params["location"] = "Allegheny County"
    params["limit"] = 50
    params["offset"] = 50*offset
    return params

def get_data(params):
    headers = {'Authorization': 'Bearer %s' % MY_API_KEY}
    url = 'https://api.yelp.com/v3/businesses/search'
    return requests.get(url, params=params, headers=headers)
    
def to_csv(name, rating, price, review_count, address, zipcode, food_type, latitude, longitude):
    with open('pittsburgh_yelp_data.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Restaurant Name', 'Average Rating', 'Price', 'Review Count', 'Street Address', 'Zip Code', 'Food Genre', 'Latitude', 'Longitude'])
        for x in range(0, len(name)-1):
            writer.writerow([name[x], rating[x], price[x], review_count[x], address[x], zipcode[x], food_type[x], latitude[x], longitude[x]])
        f.close()


if __name__ == "__main__":
    main()