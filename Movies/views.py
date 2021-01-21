from imdbapiproj.app import *
from flask import request
from flask import jsonify, make_response
import json
from imdbapiproj.Movies.models import *
from imdbapiproj.Movies.service import *
from imdbapiproj.User.user_views import *
from imdbapiproj.Movies.gener_views import *
from flask import render_template

m = MovieImpl()

'''API for Add and Retrive Movies'''
@app.route('/movies/', methods=['GET', 'POST'])
def movie():
    if request.method == 'POST':
        '''Method to add movie'''
        jsondata = request.get_json()
        user = jsondata.get('username')
        pwd = jsondata.get('password')
        logob = Login.query.filter_by(username=user).first()
        gendata = jsondata.get('genre')
        # print(gendata,type(gendata))

        try:
            if logob and pwd:
                if logob.regref.role == 'user':
                    return json.dumps({'error': 'NOT_AUTHORISED_CONTACT_ADMIN',
                                       'status': 0})


                elif int(logob.password) == pwd:
                    movie_name = jsondata.get('movie_name')
                    if not movie_name:
                        return json.dumps({'error': 'PLS_PROVIDE_MOVIE_NAME',
                                           'status': 0})
                    director_name = jsondata.get('director_name')
                    if not director_name:
                        return json.dumps({'error': 'PLS_PROVIDE_DIRECTOR_NAME',
                                           'status': 0})
                    imdb_score = jsondata.get('imdb_score')
                    if not imdb_score:
                        return json.dumps({'error': 'PLS_PROVIDE_imdb_score',
                                           'status': 0})
                    popularity = jsondata.get('popularity')
                    if not popularity:
                        return json.dumps({'error': 'PLS_PROVIDE_POPULARITY_FOR_MOVIE',
                                           'status': 0})

                    movobj = Movie(movie_name=movie_name, director_name=director_name, imdb_score=imdb_score,
                                   popularity=popularity)

                    m.add_movie(movobj)
                    db.session.commit()

                    gendata = jsondata.get('genre')
                    list1 = []
                    for gen in gendata:
                        list1.append(Genre.query.filter(Genre.genre_name == gen).first())
                    movobj.genrs.extend(list1)
                    db.session.commit()
                    print("movieObj", movobj)
                    print(list1)
                    return json.dumps({'status': 1, 'message': 'Movie Inserted Successfully!'})
                else:
                    return json.dumps({"status": "Invalid Password"})
            return json.dumps({"status": "Please provide Valid Username,Password"})
        except Exception as e:
            print("==Something went wrong==", str(e))
            return json.dumps({'error': 'Sysytem is down please try after some time', 'status': 0})



    elif request.method == 'GET':
        '''Method to retrive all movies'''
        try:
            movies = m.get_all_movies()
            all_movies = []

            for mov in movies:
                mov = m.remove_sa_instance(mov)
                list1 = []
                for mo in mov.get("genrs"):
                    list1.append(str(mo))
                # print(list1)
                a = {"movie_name": mov.get("movie_name"), "director_name": mov.get("director_name"),
                     "imdb_score": mov.get("imdb_score"),
                     "popularity": mov.get("popularity"), "genrs": list1}
                # print(a)
                all_movies.append(a)

            return json.dumps({'status': 1, 'data': all_movies})

        except Exception as e:
            print("==Something went wrong in getting all detials for Movies=", str(e))
            return json.dumps({'status': 0, 'error': 'CANNOT_FETCH_DATA_FOR_MOVIE'})


@app.route('/movies/<int:mid>/', methods=['GET', 'PUT', 'DELETE'])
def movie_details(mid):
    if request.method == 'GET':
        '''Method to retrive single movie'''
        try:
            movinstance = m.get_movie(mid)
            if movinstance:
                list1 = []
                for mo in movinstance.get("genrs"):
                    list1.append(str(mo))
                # print(list1)
                a = {"movie_name": movinstance.get("movie_name"), "director_name": movinstance.get("director_name"),
                     "imdb_score": movinstance.get("imdb_score"),
                     "popularity": movinstance.get("popularity"), "genrs": list1}
                # print(a)

                return json.dumps({'status': 1, 'data': a})
            else:
                return json.dumps({"status": "Movie with Given ID not present"})
        except Exception as e:
            print("==Something went wrong in getting detials for Movie=", str(e))
            return json.dumps({'status': 0, 'error': 'CANNOT_FETCH_DATA_FOR_MOVIE'})

    elif request.method == 'DELETE':
        '''Method to delete movie'''
        user = request.headers.get('username')
        pwd = request.headers.get('password')

        logob = Login.query.filter_by(username=user).first()

        if logob and pwd:
            if logob.regref.role == 'user':
                return json.dumps({'error': 'NOT_AUTHORISED_CONTACT_ADMIN',
                                   'status': 0})

            elif logob.password == pwd:
                movinst = m.delete_movies(mid)

                if movinst:
                    return json.dumps({"status": "Movie Deleted Successfully"})
                return json.dumps({"status": "Movie with Given ID not present"})
            else:
                return json.dumps({"status": "Invalid Password"})
        return json.dumps({"status": "Please provide Valid Username,Password"})

    elif request.method == 'PUT':
        '''Method to update movie'''
        jsondata = request.get_json()
        # print(jsondata)
        user = jsondata.get('username')
        pwd = jsondata.get('password')
        logob = Login.query.filter_by(username=user).first()

        try:
            if logob and pwd:
                if logob.regref.role == 'user':
                    return json.dumps({'error': 'NOT_AUTHORISED_CONTACT_ADMIN',
                                       'status': 0})


                elif int(logob.password) == pwd:

                    updinst = m.update_movies(mid, jsondata)
                    if updinst:
                        return json.dumps({"status": "Movie Updated Successfully", "data": jsondata})
                    return json.dumps({"status": "Movie with Given id not Present"})
                else:
                    return json.dumps({"status": "Invalid Password"})
            return json.dumps({"status": "Please provide Valid Username,Password"})

        except Exception as e:
            print("==Something went wrong==", str(e))
            return json.dumps({'error': 'Sysytem is down please try after some time', 'status': 0})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
