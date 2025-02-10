from app import app, db
from server.models import Customer, Item, Review


class TestReview:
    '''Review model in models.py'''

    def test_can_be_instantiated(self):
        '''can be invoked to create a Python object.'''
        r = Review()
        assert r
        assert isinstance(r, Review)

    def test_has_comment(self):
        '''can be instantiated with a comment attribute.'''
        r = Review(comment='great product!')
        assert r.comment == 'great product!'

    def test_can_be_saved_to_database(self):
        '''can be added to a transaction and committed to review table with comment column.'''
        with app.app_context():
            # Ensure the Review table has a 'comment' column
            assert 'comment' in Review.__table__.columns

            # Create a customer and item for the foreign key relationships
            customer = Customer(name='Test Customer')
            item = Item(name='Test Item', price=10.99)
            db.session.add_all([customer, item])
            db.session.commit()

            # Create a Review and associate it with the customer and item
            r = Review(comment='great!', customer_id=customer.id, item_id=item.id)
            db.session.add(r)
            db.session.commit()

            # Assert that the review was saved successfully
            assert hasattr(r, 'id')
            assert db.session.query(Review).filter_by(id=r.id).first()

    def test_is_related_to_customer_and_item(self):
        '''has foreign keys and relationships'''
        with app.app_context():
            assert 'customer_id' in Review.__table__.columns
            assert 'item_id' in Review.__table__.columns

            # Create customer and item records
            c = Customer(name='Relationship Test Customer')
            i = Item(name='Relationship Test Item', price=20.00)
            db.session.add_all([c, i])
            db.session.commit()

            # Create and save a Review object related to the customer and item
            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            # Check foreign keys
            assert r.customer_id == c.id
            assert r.item_id == i.id

            # Check relationships
            assert r.customer == c
            assert r.item == i
            assert r in c.reviews
            assert r in i.reviews
