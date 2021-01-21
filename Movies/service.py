
from imdbapiproj.Movies.models import *
from abc import ABC,abstractmethod
import json


class MovieoService(ABC):
    '''Abstract Class for add movie, retrive movie,Delete movie,Update movie, retrive all movies'''
    @abstractmethod
    def add_movie(self,movie):
        pass

    @abstractmethod
    def get_movie(self,id):
        pass

    @abstractmethod
    def get_all_movies(self):
        pass

    @abstractmethod
    def update_movies(self,id,instance):
        pass

    @abstractmethod
    def delete_movies(self,id):
        pass

    @abstractmethod
    def remove_sa_instance(mov):
        pass


class MovieImpl(MovieoService):
    def add_movie(self,movie):
        db.session.add(movie)
        db.session.commit()


    def get_movie(self,id):
        movieinst = Movie.query.filter_by(id=id).first()
        if movieinst:
            mov = self.remove_sa_instance(movieinst)
            return mov

    def get_all_movies(self):
        allmovies = Movie.query.filter(Movie.active == 'Y').all()
        return allmovies

    def update_movies(self,id,instance):
        extmovie = Movie.query.filter_by(id=id).first()
        if extmovie:
            extmovie.movie_name = instance['movie_name']
            extmovie.director_name = instance['director_name']
            extmovie.imdb_score = instance['imdb_score']
            extmovie.popularity = instance['popularity']
            db.session.commit()
            return True
        return False

    def delete_movies(self,id):
        extmovie = Movie.query.filter_by(id=id).first()
        if extmovie:
            db.session.delete(extmovie)
            db.session.commit()
            return True
        return False

    @staticmethod
    def remove_sa_instance(mov):
        print("Inside SA instance")
        mov_json = mov.__dict__
        if mov_json.__contains__('_sa_instance_state'):
            print("Inside movJson")
            mov_json.pop('_sa_instance_state')
            mov_json.pop('created')
            mov_json.pop('modified')
        else:
            pass
        return mov_json

# if __name__ == '__main__':
    # m1 = MovieImpl()
    # m = Movie(movie_name='III', director_name='www',
    #       imdb_score=1.5, popularity=1.0)
    # a = m1.add_movie(m)
    # print(a)




