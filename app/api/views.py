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

@api.route('/testhtml/', methods=['GET'])
def get_testhtml():
    htmlstr = ''
    htmlstr += '&nbsp;'
    htmlstr += 'Hemos visto por mucho tiempo, la forma en que los avances tecnológicos mejoran la calidad de vida de cada una de nuestras generaciones, desde la simple rueda hasta el Internet de las cosas, cada desarrollo ha cambiando la forma de vida de las sociedades que se beneficiaron de estos adelantos, la evolución estaba garantizada cada vez que un nuevo desarrollo aparecía.'
    htmlstr += 'Ahora bien, la búsqueda de la mejorar, muchas veces se cruza con el ocio, lo que significa que las nuevas tecnologías no siempre son garantía de que estamos en la senda del progreso, por cuando se presentan los nuevos modelos de Iphone, la noticia más importante es hacer "nuestros propios emojis". Sin duda algo divertido, pero si privamos la necesidad por el entretenimiento podemos frenar avances reales.'
    htmlstr += 'La inteligencia artificial es una gran oportunidad de dejar más tiempo para el ser humano, pero definitivamente la ciencia parece estar siendo influenciada por los efectos especiales, lo que nos trae a hablar de las grandes inversiones que se hacen hoy en día en personas de metal, "que nos superan en mente y cuerpo". Es sin duda un prodigio de la tecnología lograr los avances que hoy en día vemos, pero la gran pregunta ¿ son los androides la respuesta a las necesidades que tiene la humanidad en estos momentos?'
    htmlstr += '<div id="ember1072" class="ember-view">'
    htmlstr += '<div class="reader-article-content">'
    htmlstr += '<div class="slate-resizable-image-embed slate-image-embed__resize-right" data-imgsrc="https://media.licdn.com/mpr/mpr/AAIAAgDGAAAAAQAAAAAAAAxlAAAAJDJhYmMyZDM1LTQ5NzItNDJhMS05ZGM0LWY5YTE5YzE5ZTZiZg.jpg"><img class="aligncenter" src="https://www.nytimes.com/images/2018/07/02/business/02AHEAD/02AHEAD-square640.jpg" data-li-src="https://media.licdn.com/mpr/mpr/AAIAAgDGAAAAAQAAAAAAAAxlAAAAJDJhYmMyZDM1LTQ5NzItNDJhMS05ZGM0LWY5YTE5YzE5ZTZiZg.jpg" /></div>'
    htmlstr += '&nbsp;'
    htmlstr += 'Es verdad que el alcance de los cerebros electrónicos es superior al nuestro, pero para las tareas que deben cumplir estos inventos, la forma humana no es la ideal para cumplir los objetivos, me explico con un ejemplo simple, el ángulo de visión de un ser humano es de aproximadamente 180º en el plano horizontal, mientras que una simple mosca cubre el 360°, lo que demuestra que invertir recursos en replicar las características con menos ventajas a otras conocidas, es una muestra de que nos consideramos el mejor modelo a seguir.'
    htmlstr += '<div class="slate-resizable-image-embed slate-image-embed__resize-left" data-imgsrc="https://media.licdn.com/mpr/mpr/AAIAAgDGAAAAAQAAAAAAAAufAAAAJGJmMDgyOTE2LTgzNmUtNGM1Mi1iOWYzLTk5Mzg4NDliMTRlOA.jpg"><img class="alignright" src="https://media.licdn.com/mpr/mpr/AAIAAgDGAAAAAQAAAAAAAAufAAAAJGJmMDgyOTE2LTgzNmUtNGM1Mi1iOWYzLTk5Mzg4NDliMTRlOA.jpg" data-li-src="https://media.licdn.com/mpr/mpr/AAIAAgDGAAAAAQAAAAAAAAufAAAAJGJmMDgyOTE2LTgzNmUtNGM1Mi1iOWYzLTk5Mzg4NDliMTRlOA.jpg" /></div>'
    htmlstr += 'Si este patrón continua, podemos decirle al señor <strong>Hawking</strong> y al señor <strong>Musk</strong>, que no hay nada que temerle a las máquinas, porque al igual que con la amplificación de ruido, ampliaremos los defectos de los seres humanos, en estos cybors, así que bastará con atacar esos errores para hacer frente a Terminator.'
    htmlstr += 'Si vemos con objetividad el verdadero curso de lo que se necesita en robots mecánicos, copiar el caminar de un ser humano no hace grandioso el trabajo de estos nuevos equipos, debemos llevar el desarrollo a cubrir necesidades reales, estructuras capaces de rescatar víctimas de terremotos, apagar un incendio forestal de manera efectiva, salvarnos en condiciones extremas, dispositivos que basados en los mejores ejemplos de la naturaleza, lleguen a donde no podemos, algo que de verdad haga que supere en verdad las capacidades conocidas de la naturaleza.'
    htmlstr += 'Sí, es verdad que un cerebro que aprende y almacena más información que un humano es un gran desarrollo, pero no deja de ser una gran biblioteca, puede ser divertido, pero no sólo de diversión vive el hombre.'
    htmlstr += '</div>'
    htmlstr += '</div>'

    return jsonify({'success' : 'true', 'content' : htmlstr})

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
        display_name = first_name.split(' ', 1)[0] + ' ' +  last_name.split(' ', 1)[0]

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
                first_name=first_name, last_name=last_name,
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


@api.route('/home', methods=['GET'])#@token_required
def get_home_static():#(current_user):
    #data = request.get_json()
    #user = User.query.filter_by(id=current_user.id).first()

    output = {
        'success' : 'true',
        'news' : [
            {
            'id' : 1,
            'title' : 'Hay topos en la playa', 
            'extract' : 'Se descubre una especie rara de topos que se reproducen con el agua ...',
            'img_large': 'https://www.nytimes.com/images/2018/07/01/briefing/02ambriefing-asia-promo/02ambriefing-asia-promo-mediumThreeByTwo440.jpg'
            },
            {
            'id' : 2,
            'title' : 'Hay topos en la playa', 
            'extract' : 'Se descubre una especie rara de topos que se reproducen con el agua ...',
            'img_large': 'https://www.nytimes.com/images/2018/06/22/us/politics/backlash-ltr/00republicans1-mediumThreeByTwo440-v4.jpg'
            },
            {
            'id' : 3,
            'title' : 'Hay topos en la playa', 
            'extract' : 'Se descubre una especie rara de topos que se reproducen con el agua ...',
            'img_large': 'https://www.nytimes.com/images/2018/07/02/business/02AHEAD/merlin_140591313_c5e6fa0e-a071-44fa-a1da-a22bf96bb12b-mediumThreeByTwo440.jpg'
            },
            {
            'id' : 4,
            'title' : 'Hay topos en la playa', 
            'extract' : 'Se descubre una especie rara de topos que se reproducen con el agua ...',
            'img_large': 'https://www.nytimes.com/images/2018/07/01/us/01dc-protest-1sub/merlin_140546832_6410f6ce-d14d-4270-b329-adfb88b1938b-mediumThreeByTwo440.jpg'
            },
            {
            'id' : 5,
            'title' : 'Hay topos en la playa', 
            'extract' : 'Se descubre una especie rara de topos que se reproducen con el agua ...',
            'img_large': 'https://www.nytimes.com/images/2018/07/02/science/02-jp-abortion-print/00ABORTION1-mediumThreeByTwo440.jpg'
            },
            {
            'id' : 6,
            'title' : 'Hay topos en la playa', 
            'extract' : 'Se descubre una especie rara de topos que se reproducen con el agua ...',
            'img_large': 'https://www.nytimes.com/images/2018/07/02/world/02TRAVEL-BAN-03/02TRAVEL-BAN-03-mediumThreeByTwo440.jpg'
            }
        ]
    }
    return jsonify(output)