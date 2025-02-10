from app import app, db
from server.models import Customer, Item, Review


class TestAssociationProxy:
    '''Customer in models.py'''

    def test_has_association_proxy(self):
        '''has association proxy to items'''
        with app.app_context():
            # Provide valid attributes for Customer and Item
            c = Customer(name='Test Customer for Proxy')
            i = Item(name='Test Item for Proxy', price=20.00)

            # Add the customer and item to the session and commit
            db.session.add_all([c, i])
            db.session.commit()

            # Create a review linking the customer and item
            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            # Verify that the association proxy exists and functions correctly
            assert hasattr(c, 'items')  # Check if the association proxy exists
            assert i in c.items         # Check if the item is accessible through the proxy
