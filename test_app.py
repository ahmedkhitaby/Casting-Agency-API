import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie, Scene


class CastingAgencyTestCase(unittest.TestCase):
    """ This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.database_name = 'castingagency'
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(
            'postgres', '6253', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.producer_header = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhCek9DLVNISjd1QWRtdkU1V25TYiJ9.eyJodHRwczovL2V4YW1wbGUuY29tL2VtYWlsIjoicHJvZHVjZXJAYWhtLmNvbSIsImlzcyI6Imh0dHBzOi8vYWhtZWRraGl0YWJ5LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWQ4MTI0ZTYyMDZhODAwMTM1ZDA2ZjAiLCJhdWQiOiJGU05EQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTU5MzE2NzM2MywiZXhwIjoxNTkzMTc0NTYzLCJhenAiOiIyak82WTQ2R3BJaXpZQ0xqcVdjalpzWUIwZE1SbTAzNSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.Fshxz91MkZZ2Syfy_vWxmGPjasRx8opmE7xZ-HvvxAMSL7UVX96j9cLlHl-akOZxjH8LlXPk_eARjXeYlEAwCXaxYnfrc8pVSl0WsHomKbF4llal_qHQcDa2oFOnYQV0nLTKFNfsDwrL-sdylWTFIVmeCducWLkEYYE3zo6C-QkNEFXEEYfn_9-5xcFszhKRgDg8LaDlBeKawYccUuy7ES3JJhyJVfSfjKvuQhRqbfaUrZ_g2NbDGuX-Ss2X4LlxjDV_9UkZOyTVTsdwHowczDaccVx9wL6kfYebCEa95olA0Vu-hUruAXFs2uNa2ZOiJ7gZkmIZMJMp6tAzLaSVJg'
        self.new_actor = {
            "name": "new actor",
            "age": 50,
            "salary": 5000
        }

        self.new_movie = {
            "title": "new movie",
            "description": "new movie desc",
            "category": "drama"
        }

    def tearDown(self):
        """Executed after reach test """
        pass

    # test get all actors
    def test_get_all_actors(self):
        res = self.client().get('/actors', headers={
            "Authorization": self.producer_header
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
    # test get all actors 404 error

    def test_404_get_all_actors(self):
        res = self.client().get('/actord')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    # test get all movies

    def test_get_all_movies(self):
        res = self.client().get('/movies', headers={
            "Authorization": self.producer_header
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
    # test get all movies 404 error

    def test_404_get_all_movies(self):
        res = self.client().get('/movied')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    # test post new actor

    def test_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers={
            "Authorization": self.producer_header
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_actor'])
    # test post new movie

    def test_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers={
            "Authorization": self.producer_header
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_movie'])

    # test update actor info

    def test_update_actor_info(self):
        res = self.client().patch('/actors/3', json={'name': 'toto'}, headers={
            "Authorization": self.producer_header
        })
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.format()['name'], 'toto')
    # test update actor info 400 error

    def test_400_update_actor_info(self):
        res = self.client().patch('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
    # test update movie info

    def test_update_movie_info(self):
        res = self.client().patch('/movies/3', json={'title': 'toto movie'}, headers={
            "Authorization": self.producer_header
        })
        data = json.loads(res.data)
        actor = Movie.query.filter(Movie.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.format()['title'], 'toto movie')
    # test update movie info 400 error

    def test_400_update_movie_info(self):
        res = self.client().patch('/movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
    # test delete actor

    def test_delete_actor(self):
        res = self.client().delete('/actors/12', headers={
            "Authorization": self.producer_header
        })
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 12).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_actor_id'], 12)
    # test delete actor 422 error

    def test_422_delete_actor(self):
        res = self.client().delete('/actors/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    # test delete movie

    def test_delete_movie(self):
        res = self.client().delete('/movies/12', headers={
            "Authorization": self.producer_header
        })
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 12).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_movie_id'], 12)
    # test delete movie 422 error

    def test_422_delete_movie(self):
        res = self.client().delete('/movies/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
