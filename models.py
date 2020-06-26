from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


DATABASE_URL = os.environ.get('DATABASE_URL')

# database_name = 'castingagency'
# database_path = 'postgresql://{}:{}@{}/{}'.format(
#     'postgres', '6253', 'localhost:5432', database_name)
db = SQLAlchemy()


def setup_db(app, DATABASE_URL=DATABASE_URL):
    # def setup_db(app, DATABASE_URL=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)


class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.Integer(), nullable=False)
    scenes = db.relationship('Scene', backref='actors')

    def __init__(self, name, age, salary):
        self.name = name
        self.age = age
        self.salary = salary

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'salary': self.salary,
        }


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)
    scenes = db.relationship('Scene', backref='movies')

    def __init__(self, title, description, category):
        self.title = title
        self.description = description
        self.category = category

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category
        }


class Scene(db.Model):
    __tablename__ = 'scenes'
    movie_id = db.Column(db.Integer, db.ForeignKey(
        'movies.id'), primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey(
        'actors.id'), primary_key=True)
    scene_description = db.Column(db.String(), nullable=False)
