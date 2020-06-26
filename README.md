# Casting Agency API 
Welcome to my Casting Agency API, Through this API you can create, read, update and delete movies and actors in your agency using different permissions.
- You can find this API hosted on heroku through this [link](https://capfsnd.herokuapp.com/)

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

****

#### Virtual Environment

We recommend working within a virtual environment. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

****

#### PIP Dependencies

install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages from the `requirements.txt` file.

****

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database.  

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

****

### Database Setup

Make sure that you have [PostgreSQL](http://postgresguide.com/utilities/psql.html) installed and running on your local machine
Create the Database by running the following command in your terminal:
```
createdb castingagency
```

****

### Running The Server

make sure you are working using your created virtual environment.

To run the server, execute:

```bash
python app.py
```

****

### Endpoints
- Each endpoint except GET '/' require Authorization header with each request you make which contains an access token that you can get by login to Auth0 as mentioned at the end of this documentation

#### GET : '/'
- Returns:
    - It will return the home page with welcoming message and short description for each endpoint.
#### GET : '/actors'
- Returns:
    - List of all actors with each actor information like name, age and salary. 
 ```
{
    "actors": [
        {
            'id': 1,
            'name': 'Ramy',
            'age': 35,
            'salary': 100000,
        },
        {
            'id': 2,
            'name': 'sameh',
            'age': 50,
            'salary': 150000,
        },
        {
            'id': 3,
            'name': 'bassem',
            'age': 42,
            'salary': 200000,
        }
    ],
    "success": true
}
```  
#### POST : '/actors'
- Request Body: 
```
{
    'name': 'adam',
    'age': 30,
    'salary': 150000
}
```
- Returns:
    - the newly created actor.
 ```
{
    "new_actor": {
                    'id':4,
                    'name': 'adam',
                    'age': 30,
                    'salary': 150000
                },
    "success": true
}
``` 
#### PATCH : '/actors/<int:actor_id>'
- Request Arguments:
    - the required actor id must be passed in the URL 

- Request Body: at actor_id=1
```
{
    'name': 'Tamer',
    'age': 35,
    'salary': 100000,
}
```
- Returns:
    - the patched actor information.
 ```
{
    "modified_actor": {
                    'id': 1,
                    'name': 'Tamer',
                    'age': 35,
                    'salary': 100000,
                    },
    "success": true
}
``` 
#### DELETE : '/actors/<int:actor_id>'
- Request Arguments:
    - the required actor id must be passed in the URL.
- Returns:
        - the deleted actor id.
 ```
{
    "deleted_actor_id": <actor_id>,
    "success": true
}
``` 
#### GET : '/movies'
- Returns:
    - List of all movies with each movie information like title, description and category. 
 ```
{
    "movies": [
        {
            'id': 1,
            'title': 'taken',
            'description': 'movie description',
            'category': 'action'
        },
        {
            'id': 2,
            'title': 'taken2',
            'description': 'movie description',
            'category': 'action'
        }
    ],
    "success": true
}
```  
#### POST : '/movies'
- Request Body: 
```
{
    'title': 'new movie',
    'description': 'movie description',
    'category': 'comedy'
}
```
- Returns:
    - the newly created movie.
 ```
{
    "new_movie": {
                'id': 3,
                'title': 'new movie',
                'description': 'movie description',
                'category': 'comedy'
                },
    "success": true
}
``` 
#### PATCH : '/movies/<int:movie_id>'
- Request Arguments:
    - the required movie id must be passed in the URL 

- Request Body: at movie_id=1
```
{
    'title': 'doctor strange',
    'description': 'movie description',
    'category': 'action'
}
```
- Returns:
    - the patched movie information.
 ```
{
    "modified_actor":{
                    'id': 1,
                    'title': 'doctor strange',
                    'description': 'movie description',
                    'category': 'action'
                    },
    "success": true
}
``` 
#### DELETE : '/movies/<int:movie_id>'
- Request Arguments:
    - the required movie id must be passed in the URL.
- Returns:
        - the deleted movie id.
 ```
{
    "deleted_movie_id": <movie_id>,
    "success": true
}
``` 

****

## Testing The Application
To run tests run the commands: 

```
$ dropdb castingagency
$ python test_app.py
```
### Authorization and Authentication
my API allows different permissions and different roles:
#### Casting Assistant: 
- Permissions: the ability to get actors and movies.

#### Director
- Permissions: the ability to get, patch and delete actors and movies.

#### Producer: 
- Permissions: the ability to get, patch,delete, post actors and movies.

****


## Online Testing
You can test The API using Postman or curl all what you need is:
- get the access_token you need you can login by this [link](https://ahmedkhitaby.auth0.com/authorize?audience=FSNDCastingAgency&response_type=token&client_id=2jO6Y46GpIizYCLjqWcjZsYB0dMRm035&redirect_uri=https://castingagencyapi.herokuapp.com/)

- use our API URL https://castingagencyapi.herokuapp.com/ and the access_tokrn by either postman or curl to test the endpoints

## Accessing The Application
- You can use the following credentials for different permissions and different roles
    - Casting Assistant: ```email``` = assistant@ahm.com | ```password``` = CastingPass123456
    - Director: ```email``` = director@ahm.com | ```password``` = CastingPass123456
    - Producer: ```email``` = producer@ahm.com | ```password``` = CastingPass123456