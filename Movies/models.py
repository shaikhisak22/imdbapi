from imdbapiproj.app import *

movie_genr = db.Table('mov_gener',
        db.Column('mov_id', db.ForeignKey('movie.id'),primary_key = True),
        db.Column('gen_id', db.ForeignKey('genre.id'),primary_key = True))


'''Movie model'''
class Movie(db.Model):
    __tablename__ = 'movie'
    # Movie(movie_name="AAA", director_name="UUU", imdb_score='', popularity='')
    id = db.Column('id',db.Integer(), primary_key=True)
    movie_name = db.Column('movie_name',db.String(60))
    director_name = db.Column('director_name',db.String(60))
    imdb_score = db.Column('imdb_score',db.Float())
    popularity = db.Column('99popularity',db.Float())
    created = db.Column("created", db.DateTime, default=db.func.current_timestamp())
    modified = db.Column("modified", db.DateTime, default=db.func.current_timestamp(),
                         onupdate=db.func.current_timestamp())
    active = db.Column('active', db.String(10), default='Y')

'''Genre model'''
class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column('id',db.Integer(), primary_key=True)
    genre_name = db.Column('genre_name',db.String(10))
    created = db.Column("created", db.DateTime, default=db.func.current_timestamp())
    modified = db.Column("modified", db.DateTime, default=db.func.current_timestamp(),
                         onupdate=db.func.current_timestamp())
    active = db.Column('active', db.String(10), default='Y')
    movref = db.relationship(Movie, secondary=movie_genr, backref=db.backref('genrs', lazy=False))

    def __str__(self):
        return f'''{self.genre_name}'''

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    '''Create table Query'''
    db.create_all()