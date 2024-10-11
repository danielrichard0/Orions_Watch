import requests
# from django.http import JsonResponse

def external_api_view():
    # The API endpoint
    api_url = "https://api.rajaongkir.com/starter/province"
    
    # API key for the header
    headers = {
        'key': "072af6c5fb32a9b9a947fe390163254e"
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    
    except requests.exceptions.RequestException as e:
        return {"status" : False}
    
if __name__ == "__main__":
    print(external_api_view())