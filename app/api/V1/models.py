orders = []
accepted_orders = []
destinations = ['nairobi', 'nakuru', 'kisumu',
                'naivasha', 'mombasa', 'kiambu']


class Order:

    order_id = 1

    def __init__(self, origin=None, price=None, destination=None, weight=None, status="Pending"):
        self.origin = origin
        self.price = price
        self.destination = destination
        self.weight = weight
        self.id = Order.order_id
        self.status = status

        Order.order_id += 1

    def serialize(self):
        '''return tuple as dictionary'''

        return dict(
            id=self.id,
            origin=self.origin,
            price=self.price,
            destination=self.destination,
            weight=self.weight,
            status=self.status
        )

    def get_by_id(self, order_id):
        '''get a single item by unique id'''

        for order in orders:
            if order.id == order_id:
                return order
