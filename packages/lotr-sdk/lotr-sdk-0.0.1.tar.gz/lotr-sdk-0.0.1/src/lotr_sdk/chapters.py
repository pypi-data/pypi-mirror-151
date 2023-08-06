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

CHAPTER_API = API + 'chapter/'
HEADERS = {"Authorization": "Bearer " + TOKEN}

"""
 A class used to represent a Chapter
 ...
 Arguments
 ----------
 id : str
     the id of the chapter
 chapterName : str
     the name of the chapter
 book : str
     the id of the book the chapter belongs to

 """
@dataclass
class Chapter():
    id: str = ""
    chapterName: str = ""
    book: str = ""


"""
 A function that returns a list of all available Chapters. Each chapter returned is of class Chapter
 ...
 Arguments
 ----------
 params : dict
    default value of {}. Params is a dict that contains the parameters sent to an API call

 """
def getAllChapters(params={}):
    res = requests.get(CHAPTER_API,params=params, headers=HEADERS)
    if res.status_code == 200:
        logging.info(f"Status {res.status_code}. Successfully accessed {CHAPTER_API}.")    
        res_json = res.json()
        chapters = []
        for x in res_json["docs"]:
            chapters.append(Chapter(
                x.get("_id"),
                x.get("chapterName"),
                x.get('book')
            ))
        #if user limit is smaller than 1000 don't check next pages
        r = res_json["pages"]+1
        #If the pages value is larger than 1, there are more quotes to load 
        for i in range(2,r):
            q_res = requests.get(CHAPTER_API,params= params |{"page": i}, headers=HEADERS)
            if q_res.status_code == 200:
                logging.info(f"Status {q_res.status_code}. Successfully accessed {CHAPTER_API} page {i}.")
                q_json = q_res.json()["docs"]
                for x in q_json:
                    chapters.append(Chapter(
                        x.get("_id"),
                        x.get("chapterName"),
                        x.get('book')
                    ))
            else:
                logging.error(f"Status {q_res.status_code}. Failed to get page {i}.")
        return chapters
    else:
        logging.error(f"Status {res.status_code}. Failed to get chapters.")
        return []

"""
 A function that receives an id and returns a Chapter object of said id
 ...
 Arguments
 ----------
 id : str
    The wanted chapter's id
 """
def getChapterById(id):
    res = requests.get(CHAPTER_API + id, headers=HEADERS)
    if res.status_code == 200:
        logging.info(f"Status {res.status_code}. Successfully accessed {CHAPTER_API + id}.")
        res_json = res.json()["docs"][0]
        return Chapter(
                        res_json.get("_id"),
                        res_json.get("chapterName"),
                        res_json.get('book')
                        )
    else:
        logging.error(f"Status {res.status_code}. Failed to get quotes {id}.")
        return None

"""
 A function that receives a name and returns a Chapter object of said name
 ...
 Arguments
 ----------
 name : str
        The wanted chapter's name
 """
def getChapterByName(name):
    params={"chapterName" : name}
    res = requests.get(CHAPTER_API,params=params, headers=HEADERS)
    if res.status_code == 200:
        logging.info(f"Status {res.status_code}. Successfully accessed {CHAPTER_API}.")
        res_json = res.json()["docs"][0]
        return Chapter(
                        res_json.get("_id"),
                        res_json.get("chapterName"),
                        res_json.get('book')
                        )
    else:
        logging.error(f"Status {res.status_code}. Failed to get quotes {id}.")
        return None
"""
 A function that receives an argument to sort by and the sorting method("asc" for ascending and "desc" for descending)
 returns a list of sorted chapters
 ...
 Arguments
 ----------
 sortBy : str
        the argument to sort by. Can be any of the arguments of a Chapter object. Ex. "chapterName"
 sortType : str
        the sorting method("asc" for ascending and "desc" for descending)
 """
def getSortedChapters(sortBy, sortType):
    #check if valid options for sorting
    if sortBy != "_id" and sortBy != "chapterName" and sortBy != "book":
        logging.error(f"{sortBy} is not a valid sort argument.")
        return []

    if sortType != "asc" and sortType != "desc":
        logging.error(f"{sortType} is not a valid sort option.")
        return []
    params = {"sort" : sortBy + ':' + sortType}
    return getAllChapters(params)

"""
 A function that receives an option to match by a regex expression
 ...
 Arguments
 ----------
 option : str
        the argument to match by. Can be any of a chapter's class arguments.
 regex : str
        the regex expression
 """
def getChapterByRegex(option, regex):
    params = {option : regex}
    res= getAllChapters(params)
    return res
