import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie, Scene, db
from auth import requires_auth, AuthError


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # handling access after request
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # get all actors from db
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(aut_jwt):
        try:
            actors = Actor.query.order_by(Actor.id).all()
            formatted_actors = [actor.format() for actor in actors]
            return jsonify({
                'success': True,
                'actors': formatted_actors
            }), 200
        except:
            abort(404)

    # get all movies from db
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(aut_jwt):
        try:
            movies = Movie.query.order_by(Movie.id).all()
            formatted_movies = [movie.format() for movie in movies]
            return jsonify({
                'success': True,
                'movies': formatted_movies
            }), 200
        except:
            abort(404)

    # post a new actor to db
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_new_actor(aut_jwt):
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        salary = body.get('salary', None)

        try:
            actor = Actor(name=name, age=age, salary=salary)
            actor.insert()
            formatted_actor = actor.format()
            return jsonify({
                'success': True,
                'new_actor': formatted_actor
            }), 200
        except:
            abort(422)

    # post a new movie to db
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_new_movie(aut_jwt):
        body = request.get_json()
        title = body.get('title', None)
        description = body.get('description', None)
        category = body.get('category', None)

        try:
            movie = Movie(title=title, description=description,
                          category=category)
            movie.insert()
            formatted_movie = movie.format()
            return jsonify({
                'success': True,
                'new_movie': formatted_movie
            }), 200
        except:
            abort(422)

    # update actor information in db
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor_info(aut_jwt, actor_id):
        body = request.get_json()
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            if 'name' in body:
                actor.name = body.get('name')
            if 'age' in body:
                actor.age = body.get('age')
            if 'salary' in body:
                actor.salary = body.get('salary')

            actor.update()
            formatted_actor = actor.format()
            return jsonify({
                'success': True,
                'modified_actor': formatted_actor
            }), 200
        except:
            abort(400)

    # update movie information in db
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie_info(aut_jwt, movie_id):
        body = request.get_json()
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            if 'title' in body:
                movie.title = body.get('title')

            if 'description' in body:
                movie.description = body.get('description')

            if 'category' in body:
                movie.category = body.get('category')

            movie.update()
            formatted_movie = movie.format()
            return jsonify({
                'success': True,
                'modified_movie': formatted_movie
            }), 200
        except:
            abort(400)

    # delete actor from db
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(aut_jwt, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'deleted_actor_id': actor_id,
            }), 200
        except:
            abort(422)

    # delete movie from db
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(aut_jwt, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'deleted_movie_id': movie_id,
            }), 200
        except:
            abort(422)

    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome TO Casting Agency API :)',
            'endpoints': {
                '/actors with GET Request': 'will get you all the actors',
                '/movies with GET Request': 'will get you all the movies',
                '/actors with POST Request': 'will add new actor',
                '/movies with POST Request': 'will add new movie',
                '/actors/1 with PATCH Request': 'will modify actor<1> info',
                '/movies/1 with PATCH Request': 'will modify movie<1> info',
                '/actors/1 with DELETE Request': 'will delete actor<1>',
                '/movies/1 with DELETE Request': 'will delete movie<1>'
            }
        })

    # error handeling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def Unauthorized_error(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized Error"
        }), 401

    @app.errorhandler(500)
    def Internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(e):
        response = jsonify(e.error)
        response.status_code = e.status_code
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
