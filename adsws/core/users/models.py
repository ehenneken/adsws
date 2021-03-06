# -*- coding: utf-8 -*-
"""
    adsws.core.users
    ~~~~~~~~~~~~~~~~~~~~~

    Models for the users (users) of AdsWS
"""
from flask_security import UserMixin, RoleMixin
from adsws.ext.sqlalchemy import db
from sqlalchemy.orm import synonym
from flask_security.utils import encrypt_password, verify_password

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))




class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    _password = db.Column(db.String(120), name='password')
    name = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    registered_at = db.Column(db.DateTime())

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def _set_password(self, password):
        #hashed_password = generate_password_hash(password)
        hashed_password = encrypt_password(password)
        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.encode('UTF-8')
        self._password = hashed_password
    def _get_password(self):
        return self._password
    
    password = synonym('_password', descriptor=property(_get_password, 
                                                        _set_password))
    
    def validate_password(self, password):
        #return check_password_hash(self._password, password)
        return verify_password(password, self._password)

class Role(RoleMixin, db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __eq__(self, other):
        return (self.name == other or
                self.name == getattr(other, 'name', None))

    def __ne__(self, other):
        return (self.name != other and
                self.name != getattr(other, 'name', None))

