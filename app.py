from flask import Flask , request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db = SQLAlchemy(app)
api = Api(app)

# Define Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200))

# Define CartItem model
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

db.create_all()
class ProductListResource(Resource):
    def get(self):
        products = Product.query.all()
        return [{'id': product.id, 'name': product.name, 'description': product.description,
                 'price': product.price, 'image_url': product.image_url} for product in products]

class ProductResource(Resource):
    def get(self, product_id):
        product = Product.query.get_or_404(product_id)
        return {'id': product.id, 'name': product.name, 'description': product.description,
                'price': product.price, 'image_url': product.image_url}

class CartResource(Resource):
    def post(self):
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        product = Product.query.get_or_404(product_id)

        cart_item = CartItem(product_id=product.id, quantity=quantity)
        db.session.add(cart_item)
        db.session.commit()

        return {'message': 'Product added to cart successfully'}

    def get(self):
        cart_items = CartItem.query.all()
        return [{'id': item.id, 'product_id': item.product_id, 'quantity': item.quantity} for item in cart_items]

class CartItemResource(Resource):
    def delete(self, item_id):
        cart_item = CartItem.query.get_or_404(item_id)
        db.session.delete(cart_item)
        db.session.commit()
        return {'message': 'Item removed from cart successfully'}

# Add resources to API
api.add_resource(ProductListResource, '/products')
api.add_resource(ProductResource, '/products/<int:product_id>')
api.add_resource(CartResource, '/cart')
api.add_resource(CartItemResource, '/cart/<int:item_id>')

if __name__ == '__main__':
    app.run(debug=True)
