from datetime import timedelta

from flask import Flask, request, jsonify, url_for, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import exc
from werkzeug.security import check_password_hash

from api.models import db, Person, Ad, Ad_category
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)


@api.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not (email and password):
        return {'error': 'Missing info'}, 400

    user = Person.get_by_email(email)

    if user and check_password_hash(user.password, password) and user.is_active:
        token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=100))
        return {'token': token}, 200

    else:
        return {'error': 'Some parameter is wrong'}, 400


@api.route('/users', methods=['POST'])
def create_user():
    email = request.json.get('email', None)
    first_name = request.json.get('first_name', None)
    last_name = request.json.get('last_name', None)
    password = request.json.get('password', None)

    if not (email and first_name and last_name and password):
        return {'error': 'Missing info'}, 400

    user = Person.get_by_email(email)
    if user and not user.is_active:
        user.reactive_account(first_name, last_name, password)
        return jsonify(user.to_dict()), 200
     
    new_user = Person(
                email=email, 
                password=password, 
                first_name=first_name, 
                last_name=last_name
            )
    try:
        new_user.create()
        return jsonify(new_user.to_dict()), 201

    except exc.IntegrityError:
        return {'error': 'Something went wrong'}, 409


@api.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def read_user(id):
    user = Person.get_by_id(id)
    if user and user.is_active:
        return jsonify(user.to_dict()), 200
    
    return {'error': 'User not found'}, 404


@api.route('/users/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(id):
    current_user = get_jwt_identity() #id

    if current_user != id:
        return {'error': 'Invalid action'}, 400

    update_info = {
        'email': request.json.get('email', None),
        'first_name': request.json.get('first_name', None),
        'last_name': request.json.get('last_name', None),
        'password': request.json.get('password', None),
    }

    user = Person.get_by_id(id)

    if user:
        updated_user =  user.update(**{
                            key:value for key, value in update_info.items() 
                            if value is not None
                        })
        return jsonify(updated_user.to_dict()), 200

    return {'error': 'User not found'}, 400


@api.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    current_user = get_jwt_identity()

    if current_user != id:
        return {'error': 'Invalid action'}, 400
    
    user = Person.get_by_id(id)
    if user:
        user.delete()
        return jsonify(user.to_dict()), 200
    
    return {'error': 'User not found'}, 400


@api.route('users/<int:user_id>/ads/<int:ad_id>', methods=['POST'])
def create_ad():
    pass

@api.route('/users/<int:id>/ads', methods=['GET'])
@jwt_required()
def read_user_ads():
    pass


@api.route('/ads', methods=['GET'])
def read_all_ads():
    pass

@api.route('/ads/<int:id>', methods=['GET'])
@jwt_required()
def read_ad(id):
    pass

@api.route('users/<int:user_id>/ads/<int:ad_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_ad(id):
    pass

@api.route('users/<int:user_id>/ads/<int:ad_id>', methods=['DELETE'])
@jwt_required()
def delete_ad(id):
    pass


@api.route('/ad_categories', methods=['GET'])
def read_ad_categories():
    return {'categories': Ad_category.get()}, 200