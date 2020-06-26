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

        self.assistant_header = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhCek9DLVNISjd1QWRtdkU1V25TYiJ9.eyJodHRwczovL2V4YW1wbGUuY29tL2VtYWlsIjoiYXNzaXN0YW50QGFobS5jb20iLCJpc3MiOiJodHRwczovL2FobWVka2hpdGFieS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkODEyMWU2MjA2YTgwMDEzNWQwNmIxIiwiYXVkIjoiRlNORENhc3RpbmdBZ2VuY3kiLCJpYXQiOjE1OTMyMTI2OTEsImV4cCI6MTU5MzIxOTg5MSwiYXpwIjoiMmpPNlk0NkdwSWl6WUNManFXY2pac1lCMGRNUm0wMzUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.O3Jv8ihwKLNXZLPqifwmwLx6Cyb9iddl09qzGimbJrR-B6XoqCXk7YCAWq8e42xaaAzby70FR4ArQD7Zdz97oBjeSCx5VWhoN13Q_QewBshrvpcFKGViL4fC88HtUQLG8fSsz-JN-sc4eyF5b0jN2tlYDQ-FGnM8Q0jBrUt330lTDQVmd3zDhjTn3YY-IY__RE9l3GcErHVmZdbpOKwZtjrClh1Ad50GArOWXbaoRzs87nR5opmC491kwAx-29ffb5jWcsLTZbjiI7EARiXJfqIIXrKFdqEf8tf6EqHdKVtlVfuBZgTRhHUu1M6pZfJdBvRjzBqOrhUcLGS08BWikg'

        self.director_header = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhCek9DLVNISjd1QWRtdkU1V25TYiJ9.eyJodHRwczovL2V4YW1wbGUuY29tL2VtYWlsIjoiZGlyZWN0b3JAYWhtLmNvbSIsImlzcyI6Imh0dHBzOi8vYWhtZWRraGl0YWJ5LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWQ4MTI4ZmJiZDM4NjAwMTllMzc1NjciLCJhdWQiOiJGU05EQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTU5MzIxMjg5NSwiZXhwIjoxNTkzMjIwMDk1LCJhenAiOiIyak82WTQ2R3BJaXpZQ0xqcVdjalpzWUIwZE1SbTAzNSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.JCoyJ2UfS15oulf2dta2RH_zpjDwWXhfL35xNvfWMzm_jgl3yzHMfFmF3FS394BOI6nHh0S9Br_KosLY1KTEFIi1s29SFnBMxf2kxHKaTeidWKW2iSguGyQnEmFxrDGomabIS-F-NiJI9_ZZ1dFhuGdVHlfOZF-4Vi4dAhwMYEz9en-56RO4-QnZrhPwQC1tu58acQ9BeI7Fa8ergNob8Z1g85-LMnd47jOhZk5XibyEIgeuV2jrLPE7uoxWDQRpndT-2V1sKhpJ8l8ys4RVGeWTss6710G_F-1zHoCdTLz3M33JheMpMu5tIw6FJdnbqDAwLLSlEAzF92NmMGSPYw'

        self.producer_header = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhCek9DLVNISjd1QWRtdkU1V25TYiJ9.eyJodHRwczovL2V4YW1wbGUuY29tL2VtYWlsIjoicHJvZHVjZXJAYWhtLmNvbSIsImlzcyI6Imh0dHBzOi8vYWhtZWRraGl0YWJ5LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWQ4MTI0ZTYyMDZhODAwMTM1ZDA2ZjAiLCJhdWQiOiJGU05EQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTU5MzIxMzAxNCwiZXhwIjoxNTkzMjIwMjE0LCJhenAiOiIyak82WTQ2R3BJaXpZQ0xqcVdjalpzWUIwZE1SbTAzNSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.h46_SKkJg-Wv3V8TGewsjl0RoXIztC63LMg8_6Kz5thkGqQ6f5GGZiAOtBHfPAO_8UhnRYdBa47T3MhWKjzr02PMPm-2z5tjyH19WzRfwpDaqNCc5pFVdIBksaRxegQ3FS_3CfqnBK_0H6FcZcjwyevN93eXULW_kM-X-rm0g3eyVIlzU0vEApz2PhQWGb4aY4qL9qGU3ObXQfJiX5TCvGDYy1iuD_4hllScJZSKv7DovDLoH39A4lBgnX4fRfvqSYF4UEL68LS2t1RuBTO_AugG7JzkTBKfIn9J3AG8sFXh8S0my0vEjrHfXAD36miFz7qeoPoqePwDISkL7Cc7gA'

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
