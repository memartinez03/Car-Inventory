from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

#Create Car Endpoint
@api.route('/car', methods = ['POST'])
@token_required
def create_car(current_user_token):
    car_year = request.json['car_year']
    car_type = request.json['car_type']
    color = request.json['color']
    make = request.json['make']
    model = request.json['model']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car(car_year, car_type, color, make, model, user_token=user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

#Retrieve Car Endpoint
@api.route('/car', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token = a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

#Retrieve One Car Endpoint
@api.route('/car/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
        a_user = current_user_token.token
        if a_user == current_user_token.token:
            car = Car.query.get(id)
            response = car_schema.dump(car)
            return jsonify(response)
        else:
            return jsonify({"message": "Valid Token Required"}),401


# Update endpoint
@api.route('/car/<id>', methods = ['POST', 'PUT'])
@token_required
def update_contact(current_user_token, id):
    car = Car.query.get(id)
    car.car_year = request.json['car_year']
    car.car_type = request.json['car_type']
    car.color = request.json['color']
    car.make = request.json['make']
    car.model = request.json['model']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# Delete endpoint
@api.route('/car/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)
