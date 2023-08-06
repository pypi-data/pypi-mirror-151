import requests
from dataclasses import dataclass, field
try:
    from settings import API
except ImportError:
    from .settings import API
import logging
logging.basicConfig(filename='sdk.log', level=logging.INFO)
from chapters import Chapter

BOOK_API = API + 'book/'

"""
 A class used to represent a Book
 ...
 Arguments
 ----------
 id : str
     the id of the book
 name : str
     the name of the book
 chapters : list
     a list of chapters of the book. 
     Each chapter in the list is a dict containing _id : str for the id of the chapter and chapterName : str for the chapter name
 """
@dataclass
class Book():
    id: str = ""
    name: str = ""
    chapters : list = field(default_factory=list)
"""
 A function that returns a list of all available books. Each chapter returned is of class Book
 ...
 Arguments
 ----------
 params : dict
    default value of {}. Params is a dict that contains the parameters sent to an API call

 """
def getAllBooks(params={}):
    res = requests.get(BOOK_API,params=params)
    if res.status_code == 200:
        logging.info(f"Accessed {BOOK_API} with status {res.status_code}")
        books_dict = res.json()
        num_of_books = books_dict["total"]
        books = []
        for i in range(num_of_books):
            book = Book(books_dict["docs"][i]['_id'], books_dict["docs"]
                                  [i]['name'])
            books.append(book)
        return books
    else:
        logging.error(f"Status {res.status_code}. Failed to access {BOOK_API}.")
        return []

"""
 A function that receives a book's id and returns its chapters
 return dict is {"status" : 'the status code', "total": 'number of total chapters', "chapters" : 'all available chapters for the id'}
 ...
 Arguments
 ----------
 id : str
        The wanted books's id
 """
def getBookChaptersById(id):
    chap_res = requests.get(BOOK_API + id + '/chapter')
    if chap_res.status_code == 200:
        chapters= []
        for x in chap_res.json()["docs"]:
            chapters.append(Chapter(x["_id"],x["chapterName"], id))

        logging.info(f"Status {chap_res.status_code}. Accessed {BOOK_API + id + '/chapter'}")
        return {"status": 200, "total": chap_res.json()["total"], "chapters": chapters}
    else:
        logging.error(f"Status {chap_res.status_code}. Failed to get chapters of book {id}")
        return {"status": chap_res.status_code}

"""
 A function that receives a Book object and returns its chapters
 ...
 Arguments
 ----------
 id : str
        The wanted books's id
 """
def getBookChapters(book):
    res = getBookChaptersById(book.id)
    book.chapters = res["chapters"]
    return res

"""
 A function that receives an id and returns a Book object of said id
 ...
 Arguments
 ----------
 id : str
        The wanted books's id
 """
def getBookById(id):
    res = requests.get(BOOK_API + id)
    if res.status_code == 200:
        logging.info(f"Accessed {BOOK_API} with status {res.status_code}")
        new_book = Book(id, res.json()["docs"][0]["name"])
        return new_book
    else:
        logging.error(f"Status {res.status_code}. Failed to get book of id {id}.")
        return None

"""
 A function that receives a name and returns a Book object of said name
 ...
 Arguments
 ----------
 name : str
        The wanted books's name
 """
def getBookByName(name):
    res = requests.get(BOOK_API, params={"name": name})
    if res.status_code == 200:
        logging.info(f"Status {res.status_code}. Accessed {BOOK_API}.")
        res_json = res.json()
        new_book = Book(res.json()["docs"][0]["_id"], name)
        return new_book
    else:
        logging.error(f"Status {res.status_code}. Failed to get book of name {name}.")
        return None
"""
 A function that receives an option match by a regex expression
 ...
 Arguments
 ----------
 option : str
        the argument to match by. Can be any of a Book class arguments.
 regex : str
        the regex expression
 """
def getBooksByRegex(option, regex):
    params = {option : regex}
    res= getAllBooks(params)
    return res
