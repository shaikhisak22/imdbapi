from imdbapiproj.app import *

'''Register Model'''
class Register(db.Model):
    __tablename__ = 'register'

    id = db.Column('reg_id', db.Integer(), primary_key=True)
    fullname = db.Column('name', db.String(60))
    email = db.Column('email', db.String(255))
    contact = db.Column('contact', db.BigInteger())
    role = db.Column('role_name', db.String(255), default="user")
    loginref = db.relationship('Login', uselist=False, lazy=True, backref="regref")


'''Login Model'''
class Login(db.Model):
    __tablename__ = 'login'

    username = db.Column('username', db.String(30), primary_key=True)
    password = db.Column('password', db.String(255))
    token = db.Column('token', db.String(255), nullable=True)
    active = db.Column('active', db.String(10), default='Y')
    regid = db.Column('regi_id', db.ForeignKey("register.reg_id"), unique=True, nullable=False)


if __name__ == '__main__':
    db.create_all()
