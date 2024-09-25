import requests
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

# Ensure BASE_URL has the correct schema
if not BASE_URL.startswith('http://') and not BASE_URL.startswith('https://'):
    BASE_URL = 'http://' + BASE_URL

def check_response(response, expected_status_code, endpoint):
    if response.status_code == expected_status_code:
        print(f"Success for {endpoint}")
    else:
        print(f"Failed for {endpoint}. Expected: {expected_status_code}, Got: {response.status_code}")
        print(f"Response: {response.json()}")

#Testing GET
response = requests.get(f"{BASE_URL}/calendar/")

def test_get():
    print("Testing GET")

    #Valid filters
    response = requests.get(f"{BASE_URL}/calendar/", params={
        "page": 1,
        "limit": 10,
        "min_price":50,
        "max_price":200,
        "available":"t"
    })
    check_response(response, 200, "GET /calendar/ (valid filters)")

    #Invalid filters
    response = requests.get(f"{BASE_URL}/calendar/", params={
        "page": -1,
        "limit": 200,
        "min_price":-50,
        "available":"t"
    })
    check_response(response, 422, "GET /calendar/ (invalid filters)") #422 Unprocessable Entity, fastapi's default response for invalid data

    #Invalid date range
    response = requests.get(f"{BASE_URL}/calendar/", params={
        "start_date": "2021-01-01",
        "end_date": "2020-01-01"
    })
    check_response(response, 400, "GET /calendar/ (invalid date range)")
    
    #Invalid availability
    response = requests.get(f"{BASE_URL}/calendar/", params={
        "available": "invalid"
    })
    check_response(response, 400, "GET /calendar/ (invalid availability)")
    
    #Invalid price range
    response = requests.get(f"{BASE_URL}/calendar/", params={
        "min_price": 200,
        "max_price": 50
    })
    check_response(response, 400, "GET /calendar/ (invalid price range)")

#Testing POST
def test_post():
    print("Testing POST")

    #Valid data
    response = requests.post(f"{BASE_URL}/calendar/", json={
        "listing_id": 1,
        "date": "2021-01-01",
        "available": "t",
        "price": 100,
        "minimum_nights": 1,
        "maximum_nights": 30
    })
    check_response(response, 200, "POST /calendar/ (valid data)")

    #Invalid data
    response = requests.post(f"{BASE_URL}/calendar/", json={
        "listing_id": 1,
        "date": "2021-01-01",
        "available": "t",
        "price": -100,
        "minimum_nights": 1,
        "maximum_nights": 30
    })
    check_response(response, 400, "POST /calendar/ (invalid data)")


test_get()
test_post()