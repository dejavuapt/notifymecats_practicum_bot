import requests
from core.settings import URL_CATS, URL_DOGS, logging

def get_url_cat_image() -> str:
    try:
        response: requests.Response =  requests.get(URL_CATS)
    except Exception as error:
        logging.error(error)
        response: requests.Response =  requests.get(URL_DOGS)
    finally:
        random_picture_url: str = response.json()[0].get('url')
        
    return random_picture_url