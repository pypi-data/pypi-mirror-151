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
from quotes import getAllLotrQuoates

MOVIE_API = API + 'movie/'
HEADERS = {"Authorization": "Bearer " + TOKEN}

"""
 A class used to represent a Movie
 ...
 Arguments
 ----------
    id: str 
        the movie's id
    name: str 
        the movie's name
    run_time_minutes: int
        the movie's run time in minutes
    budget_millions: int 
        the movie's budget in millions
    box_office_revenue_millions: int 
        the movie's box office revenue in million
    academy_award_nominations: int 
        the number of academy award nominations the movie received
    academy_award_wins: int 
        the number of academy awards won by the movie
    rotten_tomatoes_score: 
        the movie's score on rotten tomatos
 """
@dataclass
class Movie():
    id: str = ""
    name: str = ""
    run_time_minutes: int = 0
    budget_millions: int = 0
    box_office_revenue_millions: int = 0
    academy_award_nominations: int = 0
    academy_award_wins: int = 0
    rotten_tomatoes_score: float = 0

    def getAllMovieQuates(self):
        return getAllLotrQuoates({"movie": self.id})


"""
 A function that returns a list of all available movies. Each character returned is of class Movie
 ...
 Arguments
 ----------
 params : dict
    default value of {}. Params is a dict that contains the parameters sent to an API call

 """
def getAllMovies(params = {}):
    response = requests.get(MOVIE_API,params=params, headers=HEADERS)
    if response.status_code == 200:
        logging.info(f"Successfully accessed {MOVIE_API}")
        movie_dict = response.json()
        num_of_movies = movie_dict["total"] if movie_dict["total"] < movie_dict["limit"] else movie_dict["limit"]
        movies = []
        for i in range(num_of_movies):
            movies.append(Movie(
                movie_dict["docs"][i]["_id"],
                movie_dict["docs"][i]["name"],
                movie_dict["docs"][i]["runtimeInMinutes"],
                movie_dict["docs"][i]["budgetInMillions"],
                movie_dict["docs"][i]["boxOfficeRevenueInMillions"],
                movie_dict["docs"][i]["academyAwardNominations"],
                movie_dict["docs"][i]["academyAwardWins"],
                movie_dict["docs"][i]["rottenTomatoesScore"],
            ))

        logging.info(
            f"Successfully converted {len(movies)} movies out of {num_of_movies}")
        return movies
    else:
        logging.error(
            f"Status: {response.status_code}. Failed to access {MOVIE_API}")
        return []

"""
 A function that receives an argument to sort by and the sorting method("asc" for ascending and "desc" for descending)
 returns a list of sorted characters
 ...
 Arguments
 ----------
 sortBy : str
        the argument to sort by. Can be any of the arguments of a Movie object. Ex. "academy_award_wins"
 sortType : str
        the sorting method("asc" for ascending and "desc" for descending)
 """
def getAllMoviesSorted(sortBy,sortType):
    if sortBy != "_id" and sortBy != "name" and sortBy != "runtimeInMinutes" and sortBy != "budgetInMillions" and sortBy != "boxOfficeRevenueInMillions" and sortBy != "academyAwardNominations" and sortBy != "academyAwardWins" and sortBy != "rottenTomatoesScore":
        logging.error(f"{sortBy} is not a valid sort argument.")
        return []
    if sortType != "asc" and sortType != "desc":
        logging.error(f"{sortType} is not a valid sort option.")
        return []
    
    return getAllMovies({"sort" : sortBy + ':' + sortType})


"""
 A function that receives an id and returns a Movie object of said id
 ...
 Arguments
 ----------
 id : str
    The wanted movies's id
 """
def getMovieById(id):
    res = requests.get(MOVIE_API + id, headers=HEADERS)
    if res.status_code == 200:
        movie_dict = res.json()["docs"][0]
        new_movie = Movie(
            movie_dict["_id"],
            movie_dict["name"],
            movie_dict["runtimeInMinutes"],
            movie_dict["budgetInMillions"],
            movie_dict["boxOfficeRevenueInMillions"],
            movie_dict["academyAwardNominations"],
            movie_dict["academyAwardWins"],
            movie_dict["rottenTomatoesScore"]
        )
        return new_movie
    else:
        print('error')
        return None

"""
 A function that receives a name and returns a Movie object of said name
 ...
 Arguments
 ----------
 name : str
        The wanted movie's name
 """
def getMovieByName(name):
    params = {'name': name + ' ' if name == "The Two Towers" else name,
        'limit':'1'}
    res = requests.get(MOVIE_API, params=params, headers=HEADERS)
    if res.status_code == 200:
        res_json = res.json()
        return(Movie(
                    res_json["docs"][0]["_id"],
                    res_json["docs"][0]["name"],
                    res_json["docs"][0]["runtimeInMinutes"],
                    res_json["docs"][0]["budgetInMillions"],
                    res_json["docs"][0]["boxOfficeRevenueInMillions"],
                    res_json["docs"][0]["academyAwardNominations"],
                    res_json["docs"][0]["academyAwardWins"],
                    res_json["docs"][0]["rottenTomatoesScore"]
                ))
    else:
        return None


"""
 A function that receives a comparison function to return movies by. Ex budgetInMillions<100
 ...
 Arguments
 ----------
 option : str
        A movie argument to check against
 symbol : str
        the symbol for the compare function. Ex < , > , = , <=, etc.
 val : str
        the value to compare the argument againt. Ex 100
 """
def getMoviesByComparison(option, symbol, val):
    params = {option+symbol+val : ""}
    return getAllMovies(params)

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
def getMoviesByRegex(option, regex):
    params = {option : regex}
    return getAllMovies(params)
