#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    display_name = db.Column(db.String(50))
    email = db.Column(db.String(260))
    facebook_id = db.Column(db.String(50))
    role = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    my_business = db.relationship('Business', secondary=user_business, backref=db.backref('partners', lazy='dynamic'))
