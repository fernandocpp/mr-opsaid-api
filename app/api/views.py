#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, request, current_app
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from . import api
from ..models import User
from app import db, create_app
from functools import wraps


config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
with app.app_context():
    cred_file = current_app.config['CREDENTIALS_FIREBASE_FILE']

cred = credentials.Certificate(cred_file)
cclaras_app = firebase_admin.initialize_app(cred)

admin_mails = [
    'fernando.zmorales@gmail.com',
    'ermaracucho3@gmail.com',
    'carlomurga@gmail.com',
    'shilita25@gmail.com'
    ]


### DECORADOR TOKEN

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            output = {
                'success': 'false',
                'msg': 'Token no enviado'
            }
            return jsonify({'data' : output}), 401

        try: 
            data = auth.verify_id_token(token)
            current_user = User.query.filter_by(public_id=data['uid']).first()
        except:
            output = {
                'success': 'false',
                'msg': 'Token invalido'
            }

            return jsonify({'data' : output}), 401

        return f(current_user, *args, **kwargs)

    return decorated

#Tools

def email_available(email):
    try:
        user = auth.get_user_by_email(email)
    except Exception as e:
        if (e.code == 'USER_NOT_FOUND_ERROR'):
            return True
    return False


def find_element(element, list_element):
    try:
        index_element = list_element.index(element)
        return index_element
    except ValueError:
        return -1



#### END POINTS

@api.route('/createbase', methods=['GET'])
def create_base():
    return jsonify({'message' : 'Base created!'})

@api.route('/allusers', methods=['GET'])#@token_required
def get_all_users():
    """
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    """
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.display_name
        user_data['role'] = user.role
        output.append(user_data)

    return jsonify({'users' : output})

@api.route('/test/', methods=['GET'])
def get_test():
    return jsonify({'success' : 'true'})


#@token_required
#def create_user(current_user):
@api.route('/user', methods=['POST'])
def create_user():
    """
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    """
    data = request.get_json()

    user_available = email_available(data['email'])

    display_name =  data['display_name'] if 'display_name' in data else ''
    first_name = data['first_name'] if 'first_name' in data else ''
    last_name = data['last_name'] if 'last_name' in data else ''

    if (display_name == '' and first_name != '' and last_name != ''):
        display_name = first_name + ' ' +  last_name

    if user_available:
        user = False
        try:
            user = auth.create_user(
                email=data['email'],
                password=data['password'],
                display_name=display_name,
                disabled=False)
        except Exception as e:
            print(e)
            output = {
                'success': 'false',
                'msg': 'Problema de conectividad'
            }
        if user:
            #new_role = 2 if data['email'] == "fernandoadmin@gmail.com" else 1
            new_role = 2 if data['email'] in admin_mails else 1
            new_user = User(public_id=user.uid, email=data['email'], 
                first_name=first_name, last_name='last_name',
                display_name=display_name, 
                role=new_role) #, gender=data['gender'])
            #output['user']['role'] = new_role
            db.session.add(new_user)
            db.session.commit()
            db.session.refresh(new_user)
            print('SI psao firbase')
            output = {
                'success': 'true',
                'msg': 'Usuario creado exitosamente',
                'user': {
                    'uid': user.uid,
                    'display_name': user.display_name,
                    'email': user.email,
                    'role': 'admin' if new_role == 1 else 'user',
                    'photo_url': user.photo_url
                }
            }
        else:
            output = {
                'success': 'false',
                'msg': 'Problema con Firebase'
            }

    else:
        output = {
            'success': 'false',
            'msg': 'Usuario ya existe'
        }

    return jsonify(output)




## INITIAL

@api.route('/user', methods=['GET'])
@token_required
def get_user(current_user):
    user = User.query.filter_by(id=current_user.id).first()
    if user:
        output = {
            'success' : 'true',
            'user': {},
            'msg':''
        }
        output['user']['id'] = user.public_id
        output['user']['display_name'] = user.display_name
        output['user']['role'] = user.role
        output['user']['email'] = user.email

    else:
        output = {
            'success' : 'false',
            'user': {},
            'msg':'Usuario no encontrado'
        }

    return jsonify(output)