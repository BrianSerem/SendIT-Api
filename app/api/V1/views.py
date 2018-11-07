from flask import Flask, request
from flask_restful import Resource
from .models import Order,orders, accepted_orders, destinations
from utils import valid_destination_name, valid_origin_name


class GetOrders(Resource): #GetOrders
    def get(self):
        return {"All Parcels": [order.serialize() for order in orders]}


class GetSpecificOrder(Resource): #SpecificOrder
    '''fetch a specific parcel order by id'''

    def get(self, id):
        '''get a specific order by id'''

        order = Order().get_by_id(id)

        if order:
            return {"order": order.serialize()}, 200

        return {"message": "Order not in our records"}, 404

    def delete(self, id):
        '''delete a specific order'''

        order = Order().get_by_id(id)

        if order:
            orders.remove(order)
            return {"message": "order deleted successfully"}, 200
        return {"message": "Order not found"}, 404

    def put(self, id):
        '''approve an  a parcel order'''
        order = Order().get_by_id(id)

        if order:
            if order.status != "Pending":
                return {"message": "order {}".format(order.status)} "wait for approval", 200
            order.status = "approved"
            return {"message": "parcel order  approved"}, 200
        return {"message": "order not in our records, place it"}, 404


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

class CompletedOrders(Resource):
    '''return a list of parcel orders completed by admin'''

    def get(self):
        return {"completed orders": [order.serialize() for order in orders if order.status == "completed"]}, 200