from werkzeug.security import check_password_hash, generate_password_hash
import jwt
from datetime import datetime, timedelta
from flask_login import UserMixin
from flask import current_app
from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(30))
    permissions = db.Column(db.Integer)
    default_role = db.Column(db.Boolean, default=False)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def has_permission(self, perm):
        return (self.permissions & perm)  == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm 

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm 
    
    def reset_permission(self):
        self.permissions = 0

    def insert_role():
        roles = {
            'User' : [Permission.FOLLOW, Permission.WRITE, Permission.COMMENT],
            'Admin' :  [Permission.FOLLOW, Permission.WRITE, Permission.COMMENT , Permission.ADMIN]
        }

        for ro in roles:
            role = Role.query.filter_by(role_name = ro).first()
            if role is None:
                role = Role(role_name = ro)
            default_role = 'User'
            role.reset_permission()
            for perm in roles[ro]:
                role.add_permission(perm)
            role.default_role = (role.role_name == default_role)
            db.session.add(role)
        db.session.commit()     
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.role_name}>'

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    email = db.Column(db.String(60))
    password_hash = db.Column(db.String(150))
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('you cant read password')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.role is None:
            if current_app.config.get('ADMIN_EMAIL') == self.email :
                self.role = Role.query.filter_by(role_name='Admin').first()
            if self.role is None:
                 self.role = Role.query.filter_by(default_role=True).first()

    def able(self, perm):
        return  self.role is not  None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.role is not None and self.role.has_permission(Permission.ADMIN)
    
    def gen_token(self):
        now = datetime.now()
        calc = timedelta(seconds=1800)
        get_time = (now + calc).timestamp()
        return jwt.encode({'exp': get_time, 'id': self.id}, current_app.secret_key, algorithm='HS256')
        
    def confirm_token(self, token):
        try:
            data = jwt.decode(token, current_app.secret_key,algorithms='HS256')
        except Exception as t :
            return False

        if data.get('id') != self.id:
             return False
        self.confirmed = True
        db.session.add(self)
        return True

    
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.username}>'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Permission:
    FOLLOW = 1 
    WRITE = 2
    COMMENT = 4 
    ADMIN = 8