from dataclasses import dataclass
import requests
import logging
logging.basicConfig(filename='sdk.log', level=logging.INFO)
try:
    from settings import API
    from access_token import TOKEN
except ImportError:
    from .settings import API
    from .access_token import TOKEN

QUOTE_API = API + 'quote/'
HEADERS = {"Authorization": "Bearer " + TOKEN}

"""
 A class used to represent a Quote
 ...
 Arguments
 ----------
 id : str
     the id of the quote
 dialog : str
     the dialog said by a character
 movie : str
     the movie in which the dialog was spoken
 character : str:
    the character that spoke the dialog

 """
@dataclass
class Quote():
    id: str = ""
    dialog: str = ""
    movie: str = ""
    character: str = ""

"""
 A function that returns a list of all available quotes. Each quote returned is of class Quote
 ...
 Arguments
 ----------
 params : dict
    default value of {}. Params is a dict that contains the parameters sent to an API call

 """
def getAllLotrQuoates(params={}):
    res = requests.get(QUOTE_API,params=params, headers=HEADERS)
    if res.status_code == 200:
        logging.info(f"Status {res.status_code}. Successfully accessed {QUOTE_API}.")
        res_json = res.json()
        quotes = []
        for x in res_json["docs"]:
            quotes.append(Quote(
                x["id"],
                x["dialog"],
                x["movie"],
                x["character"]
            ))
        #if user limit is smaller than 1000 don't check next pages
        r = 0 if  params.get("limit") else res_json["pages"]+1 
        #If the pages value is larger than 1, there are more quotes to load 
        for i in range(2,r):
            q_res = requests.get(QUOTE_API,params= params |{"page": i}, headers=HEADERS)
            if q_res.status_code == 200:
                logging.info(f"Status {q_res.status_code}. Successfully accessed {QUOTE_API} page {i}.")
                q_json = q_res.json()
                for x in q_json["docs"]:
                    quotes.append(Quote(
                        x["id"],
                        x["dialog"],
                        x["movie"],
                        x["character"]
                    ))
            else:
                logging.error(f"Status {q_res.status_code}. Failed to get page {i}.")
        return quotes
    else:
        logging.error(f"Status {res.status_code}. Failed to get quotes.")
        return []

"""
 A function that receives an id and returns a Quote's object of said id
 ...
 Arguments
 ----------
 id : str
    The wanted quote's id
 """
def getQuoteById(id):
    res = requests.get(QUOTE_API + id, headers=HEADERS)
    if res.status_code == 200:
        logging.info(f"Status {res.status_code}. Successfully accessed {QUOTE_API + id}.")
        res_json = res.json()["docs"][0]
        return Quote(
                        res_json["id"],
                        res_json["dialog"],
                        res_json["movie"],
                        res_json["character"]
                    )
    else:
        logging.error(f"Status {res.status_code}. Failed to get quotes {id}.")
        return None

"""
 A function that receives an argument to sort by and the sorting method("asc" for ascending and "desc" for descending)
 returns a list of sorted characters
 ...
 Arguments
 ----------
 sortBy : str
        the argument to sort by. Can be any of the arguments of a Quote object. Ex. "dialog"
 sortType : str
        the sorting method("asc" for ascending and "desc" for descending)
 """
def getQuotesSorted(sortBy, sortType):
    #check if valid options for sorting
    if sortBy != "id" and sortBy != "dialog" and sortBy != "movie" and sortBy != "character":
        logging.error(f"{sortBy} is not a valid sort argument.")
        return []

    if sortType != "asc" and sortType != "desc":
        logging.error(f"{sortType} is not a valid sort option.")
        return []
    params = {"sort" : sortBy + ':' + sortType}
    return getAllLotrQuoates(params)

"""
 A function that receives an option to match by a regex expression
 ...
 Arguments
 ----------
 option : str
        the argument to match by. Can be any of a movie's class arguments.
 regex : str
        the regex expression
 """
def getQuotesByRegex(option, regex):
    params = {option : regex}
    return getAllLotrQuoates(params)

"""
 A function that returns a limited amount of quotes, as long as limit < 1000
 ...
 Arguments
 ----------
 limit : int
        the amount of quotes to return
 """
def getLimitedQuotes(limit):
    params = {"limit" : limit}
    return getAllLotrQuoates(params)


