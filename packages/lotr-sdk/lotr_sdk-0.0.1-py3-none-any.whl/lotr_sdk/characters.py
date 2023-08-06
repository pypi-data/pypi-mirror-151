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
from quotes import Quote

CHARACTER_API = API + 'character/'
HEADERS = {"Authorization": "Bearer " + TOKEN}

"""
 A class used to represent a Character
 ...
 Arguments
 ----------
 id : str
     the id of the character
 height : str
     the height of the character
 race : str
     the race of the character
 gender: str 
    the gender of the character
 birth: str
    the birth date of the character
 spouse: str 
    the spouse of the character
 death: str 
    the death date of the character
 realm: str 
    the realm of the character
 hair: str
    the hair description of the character
 name: str 
    the name of the character
 wikiUrl: str 
    a link to the characters bio
 """
@dataclass
class Character():
    id: str = ""
    height: str = ""
    race: str = ""
    gender: str = ""
    birth: str = ""
    spouse: str = ""
    death: str = ""
    realm: str = ""
    hair: str = ""
    name: str = ""
    wikiUrl: str = ""

"""
 A function that returns a list of all available Characters. Each character returned is of class Character
 ...
 Arguments
 ----------
 params : dict
    default value of {}. Params is a dict that contains the parameters sent to an API call

 """
def getAllCharacters(params={}):
    res = requests.get(CHARACTER_API,params=params, headers=HEADERS)
    if res.status_code == 200:
        logging.info(f"Status {res.status_code}. Successfully accessed {CHARACTER_API}.")
        res_json = res.json()
        characters = []
        for x in res_json["docs"]:
            characters.append(Character(
                x.get("_id"),
                x.get("height"),
                x.get("race"),
                x.get("gender"),
                x.get("birth"),
                x.get("spouse"),
                x.get("death"),
                x.get("realm"),
                x.get("hair"),
                x.get("name"),
                
            ))
        #if user limit is smaller than 1000 don't check next pages
        r = res_json["pages"]+1
        #If the pages value is larger than 1, there are more quotes to load 
        for i in range(2,r):
            q_res = requests.get(CHARACTER_API,params= params |{"page": i}, headers=HEADERS)
            if q_res.status_code == 200:
                logging.info(f"Status {q_res.status_code}. Successfully accessed {CHARACTER_API} page {i}.")
                q_json = q_res.json()
                for x in q_json["docs"]:
                    characters.append(Character(
                        x.get("_id"),
                        x.get("height"),
                        x.get("race"),
                        x.get("gender"),
                        x.get("birth"),
                        x.get("spouse"),
                        x.get("death"),
                        x.get("realm"),
                        x.get("hair"),
                        x.get("name"),
                            ))
            else:
                logging.error(f"Status {q_res.status_code}. Failed to get page {i}.")
        return characters
    else:
        logging.error(f"Status {res.status_code}. Failed to get characters.")
        return []

"""
 A function that receives a name and returns a Character object of said name
 ...
 Arguments
 ----------
 name : str
        The wanted Character's name
 """
def getCharacterByName(name):
    params= {"name": name}
    res = requests.get(CHARACTER_API,params=params, headers=HEADERS)
    if res.status_code == 200:
        logging.info(f"Status {res.status_code}. Successfully accessed {CHARACTER_API}.")
        res_json = res.json()["docs"][0]
        return Character(
                        res_json.get("_id"),
                        res_json.get("height"),
                        res_json.get("race"),
                        res_json.get("gender"),
                        res_json.get("birth"),
                        res_json.get("spouse"),
                        res_json.get("death"),
                        res_json.get("realm"),
                        res_json.get("hair"),
                        res_json.get("name"),
                            )
    else:
        logging.error(f"Status {res.status_code}. Failed to get character {name}.")
        return None
"""
 A function that receives an id and returns a Character object of said id
 ...
 Arguments
 ----------
 id : str
    The wanted character's id
 """
def getCharacterById(id):
    res = requests.get(CHARACTER_API + id, headers=HEADERS)
    if res.status_code == 200:
        logging.info(f"Status {res.status_code}. Successfully accessed {CHARACTER_API + id}.")
        res_json = res.json()["docs"][0]
        return Character(
                        res_json.get("_id"),
                        res_json.get("height"),
                        res_json.get("race"),
                        res_json.get("gender"),
                        res_json.get("birth"),
                        res_json.get("spouse"),
                        res_json.get("death"),
                        res_json.get("realm"),
                        res_json.get("hair"),
                        res_json.get("name"),
                            )
    else:
        logging.error(f"Status {res.status_code}. Failed to get quotes {id}.")
        return None

"""
 A function that receives a Character and a dict of params and returns all the character's quotes
 ...
 Arguments
 ----------
 character : Character
    a character object
 params : dict
    default value of {}. Params is a dict that contains the parameters sent to an API call

 """
def getCharacterQuotes(character, params={}):
    return getCharacterQuotesById(character.id, params)

"""
 A function that receives an id and a dict of params and returns all the character's quotes
 ...
 Arguments
 ----------
 id : str
    the character's id
 params : dict
    default value of {}. Params is a dict that contains the parameters sent to an API call

 """
def getCharacterQuotesById(id, params={}):
    res = requests.get(CHARACTER_API + id + '/quote',params=params, headers=HEADERS)
    if res.status_code == 200:
        logging.info(f"Status {res.status_code}. Successfully accessed {CHARACTER_API + id + '/quote'}.")
        res_json = res.json()["docs"]
        quotes = []
        for x in res_json:
            quotes.append(Quote(x["_id"],x["dialog"], x["movie"], id))
        return quotes
    else:
        logging.error(f"Status {res.status_code}. Failed to get quotes {id}.")
        return []
"""
 A function that receives a name and a dict of params and returns all the character's quotes
 ...
 Arguments
 ----------
 name : str
    the character's name
 params : dict
    default value of {}. Params is a dict that contains the parameters sent to an API call

 """
def getCharacterQuotesByName(name, params={}):
    res = requests.get(CHARACTER_API, params={"name": name}, headers=HEADERS)
    if res.status_code == 200:
        logging.info(f"Status {res.status_code}. Successfully accessed {CHARACTER_API}.")
        res_json = res.json()["docs"][0]
        return getCharacterQuotesById(res_json["_id"], params)
    else:
        logging.error(f"Status {res.status_code}. Failed to get quotes for {name}.")
        return []

"""
 A function that receives a list of names and returns all the characters who are not on that list
 ...
 Arguments
 ----------
 names : list of strings
    the characters names

 """
def getAllCharacterWithoutSome(names):
    return getAllCharacters({"name!": names})

"""
 A function that receives an option and and option value
 returns a list of all Characters that option(argument) matches the option value
 ...
 Arguments
 ----------
 option : str
        the argument to sort by. Can be any of the arguments of a Character object. Ex. "race"
 option_value : str
        the option value. Ex. "Human"
 """
def getAllCharactersByOption(option, option_value):
    #check if valid options 
    if option != "sort" and option != "height" and option != "race" and option != "_id" and option != "gender" and option != "birth" and option != "spouse" and option != "death" and option != "realm" and option != "hair" and option != "name":
        logging.error(f"{option} is not a valid character option.")
        return []
    params= {option: option_value}
    return getAllCharacters(params)

"""
 A function that receives an argument to sort by and the sorting method("asc" for ascending and "desc" for descending)
 returns a list of sorted characters
 ...
 Arguments
 ----------
 sortBy : str
        the argument to sort by. Can be any of the arguments of a Chapter object. Ex. "race"
 sortType : str
        the sorting method("asc" for ascending and "desc" for descending)
 """
def getSortedCharacters(sortBy, sortVal):
    return getAllCharactersByOption("sort", sortBy + ':' + sortVal)

"""
 A function that receives an option to match by a regex expression
 ...
 Arguments
 ----------
 option : str
        the argument to match by. Can be any of a character's class arguments.
 regex : str
        the regex expression
 """
def getCharacterByRegex(option, regex):
    params = {option : regex}
    return getAllCharacters(params)
