from imdbapiproj.app import *
import json
from flask import request
from imdbapiproj.Movies.models import *
from imdbapiproj.User.models import *
from imdbapiproj.Movies.service import *

m = MovieImpl()

'''API to Add and Retrive Genre'''
@app.route('/genre/', methods=['GET', 'POST'])
def genre():
    if request.method == 'POST':
        '''Method to add Genre'''
        gendata = request.get_json()
        # print(gendata)
        user = gendata.get('username')
        pwd = gendata.get('password')
        logob = Login.query.filter_by(username=user).first()

        try:
            if logob and pwd:
                if logob.regref.role == 'user':
                    return json.dumps({'error': 'NOT_AUTHORISED_CONTACT_ADMIN','status': 0})

                elif int(logob.password) == pwd:
                    genre_name = gendata.get('genre_name')
                    if not genre_name:
                        return json.dumps({'error': 'PLS_PROVIDE_GENRE_NAME','status': 0})

                    g1 = Genre(genre_name= gendata['genre_name'])
                    db.session.add(g1)
                    db.session.commit()
                    return json.dumps({'status': 1, 'message': '{} Gener Inserted Successfully!'.format(genre_name)})
                else:
                    return json.dumps({"status": "Invalid Password"})

            return json.dumps({"status": "Please provide Valid Username,Password"})
        except Exception as e:
            print("==Something went wrong==", str(e))
            return json.dumps({'error': 'Sysytem is down please try after some time', 'status': 0})




    elif request.method == 'GET':
        '''Method to Retrive Genre'''
        try:
            genres = Genre.query.all()
            all_genre = []
            for gen in genres:
                all_genre.append(m.remove_sa_instance(gen))
            return json.dumps({'status': 1, 'data': all_genre})

        except Exception as e:
            print("==Something went wrong in getting all detials for Genre==", str(e))
            return json.dumps({'status': 0, 'error': 'CANNOT_FETCH_DATA_FOR_GENRE'})
