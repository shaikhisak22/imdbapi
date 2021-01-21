from imdbapiproj.User.models import *
from flask import request
import json
SUCCESS = "success"
ERROR = "error"


'''API to Register User and Admin'''
@app.route("/movie/register/",methods=['POST'])
def user_registration():
    reqdata= request.get_json()
    if not reqdata:
        return json.dumps({ERROR:"Fields are mandatory [Fullname,email,username,password,role]"})
    else:
        fname = reqdata.get('fullname')
        user = reqdata.get('username')
        pwd = reqdata.get('password')
        email = reqdata.get('email')
        contact = reqdata.get('contact')
        role = reqdata.get('role')
        if not fname or not user or not pwd or not email or not contact:
            return json.dumps({ERROR: "Fields are mandatory [Fullname,email,username,password,role]"})

        if Login.query.filter_by(username=user).first():
            return json.dumps({ERROR: "Duplicate Username..!"})

        reg = Register(fullname=fname,email=email,contact= contact,role=role)
        db.session.add(reg)
        db.session.commit()

        login = Login(username=user,password=pwd,regid=reg.id)
        db.session.add(login)
        db.session.commit()
        return json.dumps({SUCCESS: f"{user} ADDED SUCCESSFULLY...!"})






# if __name__ == '__main__':
#     app.run(debug=True)