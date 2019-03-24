from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import click

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.cli.command()
def forge():
    db.create_all()

    name = "Chang WanMing"
    movies = [
        {'title': 'My Neighbor Totoro',     'year': '1988'},
        {'title': 'Dead Poets Society',     'year': '1989'},
        {'title': 'A Perfect World',        'year': '1993'},
        {'title': 'Leon',                   'year': '1994'},
        {'title': 'Mahjong',                'year': '1996'},
        {'title': 'Swallowtail Butterfly',  'year': '1996'},
        {'title': 'King of Comedy',         'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WAL-E',                  'year': '2008'},
        {'title': 'The Pork of Music',      'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


@app.route('/')
@app.route('/index')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)


if __name__ == '__main__':
    app.run()
