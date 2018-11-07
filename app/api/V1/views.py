from flask import Flask, request
from flask_restful import Resource
from .models import Order,orders, accepted_orders, destinations
from utils import valid_destination_name, valid_origin_name


class GetOrders(Resource): #GetOrders
    def get(self):
        return {"All Parcels": [order.serialize() for order in orders]}


class CreateParcel(Resource): #PostParcel
    '''Create a new parcel order.'''

    def post(self):
        '''get details of the parcel to be sent.'''

        data = request.get_json()
        origin = data['origin']
        price = data['price']
        destination = data['destination']
        weight = data['weight']

        

        if not valid_origin_name(origin):
            return {'message': "invalid place of origin"}, 400

        if type(price) != int:
            return {'message': "invalid price range"}, 400

        if type(weight) != int:
            return {'message': "Weight invalid"}, 400

        if not valid_destination_name(destination):
            return {'message': "invalid destination name"}, 400

        order = Order(origin, price, destination, weight)

        if order.destination in destinations:
            orders.append(order)
            return {"message": "Order placed waiting for approval!"}, 201
        return {"message": "delivery to {}".format(order.destination) "is currently not available"}