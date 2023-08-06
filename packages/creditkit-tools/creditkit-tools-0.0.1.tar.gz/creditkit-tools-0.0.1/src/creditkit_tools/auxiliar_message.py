import logging 
import requests 

def logging_requests():
    x = requests.get('https://w3schools.com')
    print(x.status_code)
    logging.warning(f"This is an example of {x}")