import requests
from django.http import JsonResponse

def get_region(option):
    # The API endpoint
    api_url = "https://api.rajaongkir.com/starter/"

    endpoints = {
        1 : "province",
        2 : "city",
        3 : "subdistrict"
    }

    if option in endpoints:
        api_url = f"{api_url}{endpoints[option]}"
    else:
        raise ValueError("Invalid Option")
    
    # API key for the header
    headers = {
        'key': "25b882cd0e6b6ad1dbc78b6a2cd589b6"
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    
    except requests.exceptions.RequestException as e:
        return {"status" : False}
    

import requests

def get_ongkir(origin, destination, weight, courier):
    url = "https://api.rajaongkir.com/starter/cost" 
    headers = {
        'key': '25b882cd0e6b6ad1dbc78b6a2cd589b6',  
        'content-type': 'application/x-www-form-urlencoded'
    }
    
    payload = {
        'origin': int(origin),
        'destination': int(destination),
        'weight': int(weight),
        'courier': courier
    }

    print("payload : ", payload)

    try:
        response = requests.post(url, headers=headers, data=payload)
        print("data : ", response.json())
        response.raise_for_status() 
        

        data = response.json()
        return data
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    
def get_city(prov_id):
    api_url = 'https://api.rajaongkir.com/starter/city'
    api_url = f"{api_url}?province={prov_id}"

    headers = {
        'key': "25b882cd0e6b6ad1dbc78b6a2cd589b6"
    }


    try:
        resp = requests.get(api_url, headers=headers)
        resp.raise_for_status()

        data = resp.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"Status" : e} 
    
if __name__ == "__main__":
    print(get_region(3))