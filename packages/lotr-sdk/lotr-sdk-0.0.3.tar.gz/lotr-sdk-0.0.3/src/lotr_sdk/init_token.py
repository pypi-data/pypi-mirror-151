import requests
try:
    from settings import API
except ImportError:
    from .settings import API
import logging
logging.basicConfig(filename='sdk.log', level=logging.INFO)
import os
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

"""
 A function to initialize a token. Must be run before attempting to use sdk!!
 ...
 Arguments
 ----------
 token : str
    a bearer token provided by the api.

 """
def initToken(token):
    header = {"Authorization": "Bearer " + token}
    response = requests.get(API + 'movie',headers=header)
    if response.status_code == 200:
        with open(os.path.join(__location__, 'access_token.py'), "w") as myfile:
            myfile.write(f"TOKEN = '{token}'")
            logging.info("TOKEN was created in access_token.py")
            return token
    else:
        logging.error("Failed to create TOKEN in access_token.py")
        return ""

initToken('f')