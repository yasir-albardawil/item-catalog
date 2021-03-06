
# Item Catalog
*A Udacity Full Stack Nanodegree Degree project*

Website link: http://ec2-54-93-109-154.eu-central-1.compute.amazonaws.com/
## Prerequisites
* [Python 3.7](https://www.python.org/)
* [Vagrant](https://www.vagrantup.com/)
* [VirtualBox](https://www.virtualbox.org/)

## Setup Project:
1.  Install Vagrant & VirtualBox
2.  Clone the Udacity Vagrantfile
3.  Go to Vagrant directory and either clone this repo or download and place zip here
4.  Launch the Vagrant VM (`vagrant up`)
5.  Log into Vagrant VM (`vagrant ssh`)
6.  Navigate to  `cd/vagrant`  as instructed in terminal
7.  The app imports requests which is not on this vm. `Run sudo pip install requests`
8.  Setup application database  `python /item-catalog/database_setup.py`
9.  *Insert fake data  `python /item-catalog/add_movies.py`
10.  Run application using  `python /item-catalog/application.py`
11.  Access the application locally using  [http://localhost:8000](http://localhost:8000/)

## JSON endpoints
#### The following are open to the public:

`http://localhost:8000/movies.json`  - Displays the whole movies and the gnres

        {
      "moives": [
        {
          "genre": "drama", 
          "id": 1, 
          "movieCoverUrl": "https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg", 
          "movieName": "The Shawshank Redemption", 
          "movieTrailerUrl": "https://www.imdb.com/videoembed/vi3877612057", 
          "rating": 9.3, 
          "storyline": "Chronicles the experiences of a formerly successful banker as a prisoner in the gloomy jailhouse of Shawshank after being found guilty of a crime he did not commit. The film portrays the man's unique way of dealing with his new, torturous life; along the way he befriends a number of fellow prisoners, most notably a wise long-term inmate named Red. Written by J-S-Golden", 
          "year": 1994
        }
        }
      ]

`http://localhost:8000/movies/genre/animation.json`  - Displays movies for a specific genre

    {
      "movies": [
        {
          "genre": "animation", 
          "id": 2, 
          "movieCoverUrl": "https://m.media-amazon.com/images/M/MV5BMDliOTIzNmUtOTllOC00NDU3LWFiNjYtMGM0NDc1YTMxNjYxXkEyXkFqcGdeQXVyNTM3NzExMDQ@._V1_SY1000_CR0,0,699,1000_AL_.jpg", 
          "movieName": "Big Hero 6", 
          "movieTrailerUrl": "https://www.youtube.com/embed/z3biFxZIJOQ", 
          "rating": 7.8, 
          "storyline": "When a devastating event befalls the city of San Fransokyo and catapults Hiro into the midst of danger, he turns to Baymax and his close friends adrenaline junkie Go Go Tomago, neatnik Wasabi, chemistry whiz Honey Lemon and fanboy Fred. Determined to uncover the mystery, Hiro transforms his friends into a band of high-tech heroes called \"Big Hero 6.\" Written by Walt Disney Animation Studios", 
          "year": 2014
        }
      ]
    }

`http://localhost:8000/movies/genre/horror/3.json`  - Displays movies for a specific genre and movie id

    {
      "movie": {
        "genre": "horror", 
        "id": 3, 
        "movieCoverUrl": "https://m.media-amazon.com/images/M/MV5BZDVkZmI0YzAtNzdjYi00ZjhhLWE1ODEtMWMzMWMzNDA0NmQ4XkEyXkFqcGdeQXVyNzYzODM3Mzg@._V1_SY1000_CR0,0,666,1000_AL_.jpg", 
        "movieName": "IT", 
        "movieTrailerUrl": "https://www.imdb.com/videoembed/vi1396095257", 
        "rating": 7.4, 
        "storyline": "In the Town of Derry, the local kids are disappearing one by one. In a place known as 'The Barrens', a group of seven kids are united by their horrifying and strange encounters with an evil clown and their determination to kill It. Written by Emma Chapman", 
        "year": 2017
      }
    }

## Author
* **Yasir Albardawil** - *Initial work* - [yasir-albardawil](https://github.com/yasir-albardawil)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

