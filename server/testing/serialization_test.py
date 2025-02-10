from app import app, db
from server.models import Customer, Item, Review


class TestSerialization:
    '''models in models.py'''

    def test_customer_is_serializable(self):
        '''customer is serializable'''
        with app.app_context():
            # Create a customer and related review
            c = Customer(name='Phil')
            i = Item(name='Test Item for Serialization', price=19.99)
            db.session.add_all([c, i])
            db.session.commit()

            # Create a review and associate it with the customer and item
            r = Review(comment='great!', customer_id=c.id, item_id=i.id)
            db.session.add(r)
            db.session.commit()

            # Serialize the customer and verify its structure
            customer_dict = c.to_dict()

            assert customer_dict['id']
            assert customer_dict['name'] == 'Phil'
            assert customer_dict['reviews']
            assert 'customer' not in customer_dict['reviews']

    def test_item_is_serializable(self):
        '''item is serializable'''
        with app.app_context():
            # Create an item and related review
            i = Item(name='Insulated Mug', price=9.99)
            c = Customer(name='Test Serialization Customer')
            db.session.add_all([c, i])
            db.session.commit()

            # Create a review and associate it with the item and customer
            r = Review(comment='great!', customer_id=c.id, item_id=i.id)
            db.session.add(r)
            db.session.commit()

            # Serialize the item and verify its structure
            item_dict = i.to_dict()

            assert item_dict['id']
            assert item_dict['name'] == 'Insulated Mug'
            assert item_dict['price'] == 9.99
            assert item_dict['reviews']
            assert 'item' not in item_dict['reviews']

    def test_review_is_serializable(self):
        '''review is serializable'''
        with app.app_context():
            # Create customer and item records
            c = Customer(name='Serialization Test Customer')
            i = Item(name='Serialization Test Item', price=25.50)
            db.session.add_all([c, i])
            db.session.commit()

            # Create a review and associate it with the customer and item
            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            # Serialize the review and verify its structure
            review_dict = r.to_dict()

            assert review_dict['id']
            assert review_dict['customer']
            assert review_dict['item']
            assert review_dict['comment'] == 'great!'
            assert 'reviews' not in review_dict['customer']
            assert 'reviews' not in review_dict['item']
