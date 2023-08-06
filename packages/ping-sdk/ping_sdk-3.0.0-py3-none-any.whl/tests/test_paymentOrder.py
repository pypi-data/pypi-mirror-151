import unittest
import uuid
import os
from dotenv import load_dotenv
from ping.payments_api import PaymentsApi
from test_helper import testHelper


@unittest.skipUnless(testHelper.api_is_connected(), "A connection to the API is needed")
class TestPaymentOrder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.payments_api = PaymentsApi(os.getenv("TENANT_ID"))
        cls.split_tree_id = os.getenv("SPLIT_TREE_ID")
        cls.test_helper = testHelper

    def setUp(self):
        self.payment_order_id = os.getenv("PAYMENT_ORDER_ID")

# Get Payment Orders Tests
    # get payment orders correctly (status code 200)
    def test_get_payment_orders_200(self): 
    
        response_date = self.payments_api.paymentOrder.get_payment_orders("2020-03-27T09:42:30Z", "2022-03-27T09:42:30Z")
        response = self.payments_api.paymentOrder.get_payment_orders()

        # tests with start-end date
        self.test_helper.run_tests(self, response_date)

        # tests without date
        self.test_helper.run_tests(self, response)

    # get payment orders with impossible dates (status code 422)
    def test_get_payment_orders_422(self):
        response_date = self.payments_api.paymentOrder.get_payment_orders("12/90/2019", "40/10/2020")
        self.test_helper.run_tests(self, response_date, 422)

# Create Payment Order Tests
    # creates a payment order correctly (status code 200)
    def test_create_payment_order_200(self):
        response = self.payments_api.paymentOrder.create_payment_order(self.split_tree_id, "SEK")
        self.test_helper.run_tests(self, response)

    # creates a payment orders with incorrect id format (status code 422)
    def test_create_payment_order_422(self):
        response = self.payments_api.paymentOrder.create_payment_order(self.split_tree_id, "")
        self.test_helper.run_tests(self, response, 422)

# Get Payment Order Tests
    # gets a payment order correctly (status code 200)
    def test_get_payment_order_200(self):
        response = self.payments_api.paymentOrder.get_payment_order(self.payment_order_id)
        self.test_helper.run_tests(self, response)
    
    # get a payment order with incorrect id format (status code 422)
    def test_get_payment_order_422(self):
        response = self.payments_api.paymentOrder.get_payment_order(0)
        self.test_helper.run_tests(self, response, 422)
    
    # get a payment order with a non-existing id (status code 404)
    def test_get_payment_order_404(self):
        response = self.payments_api.paymentOrder.get_payment_order(uuid.uuid4())
        self.test_helper.run_tests(self, response, 404)

# Update Payment Order Tests
    # updates a payment order correctly (status code 204)
    def test_update_payment_order_204(self):
        
        response = self.payments_api.paymentOrder.update_payment_order(
            self.payment_order_id,
            self.split_tree_id
        )
        self.test_helper.run_tests(self, response, 204)
        

    # updates a payment order with incorrect id format (status code 422)
    def test_update_payment_order_422(self):
        
        response = self.payments_api.paymentOrder.update_payment_order(
            0,
            self.split_tree_id
        )
        self.test_helper.run_tests(self, response, 422)
        

    # updates a payment order with a non-existing id (status code 404)
    def test_update_payment_order_404(self):
        
        response = self.payments_api.paymentOrder.update_payment_order(
            "",
            self.split_tree_id
        )
        self.test_helper.run_tests(self, response, 404)
        

# Close Payment Order Tests
    # closes a payment order correctly (status code 204)
    def test_close_payment_order_204(self):
        response = self.payments_api.paymentOrder.close_payment_order(self.payment_order_id)
        self.test_helper.run_tests(self, response, 204)

    # closes a payment order with an incorrect id format (status code 422)
    def test_close_payment_order_422(self):
        response = self.payments_api.paymentOrder.close_payment_order(0)
        self.test_helper.run_tests(self, response, 422)

    # closes a payment order with a non-existing id (status code 404)
    def test_close_payment_order_404(self):
        response = self.payments_api.paymentOrder.close_payment_order(uuid.uuid4())
        self.test_helper.run_tests(self, response, 404)

# Split Payment Order Tests
    # splits a payment order correctly (status code 204)
    def test_split_payment_order_204(self):
        response = self.payments_api.paymentOrder.split_payment_order(self.payment_order_id)
        self.test_helper.run_tests(self, response, 204)

    # fast forwards and splits a payment order correctly (status code 204)
    def test_split_payment_order_fast_forward_204(self):
        payment_order_id = self.test_helper.prepare_payment_order_handling()
        response = self.payments_api.paymentOrder.split_payment_order(payment_order_id, fast_forward=True)
        self.test_helper.run_tests(self, response, 204)

    # splits a payment order with an incorrect id format (status code 422)
    def test_split_payment_order_422(self):
        response = self.payments_api.paymentOrder.split_payment_order(0)
        self.test_helper.run_tests(self, response, 422)

    # splits a payment order with a non-existing id (status code 404)
    def test_split_payment_order_404(self):
        response = self.payments_api.paymentOrder.split_payment_order(uuid.uuid4())
        self.test_helper.run_tests(self, response, 404)

# Settle Payment Order Tests
    # settles a payment correctly (status code 204)
    def test_settle_payment_order_204(self):
        response = self.payments_api.paymentOrder.settle_payment_order(self.payment_order_id)
        self.test_helper.run_tests(self, response, 204)
    
    # fast forwards and settles a payment correctly (status code 204)
    def test_settle_payment_order_fast_forward_204(self):
        payment_order_id = self.test_helper.prepare_payment_order_handling()
        response = self.payments_api.paymentOrder.settle_payment_order(payment_order_id, fast_forward=True)
        self.test_helper.run_tests(self, response, 204)

    # settles a payment with an incorrect id format (status code 422)
    def test_settle_payment_order_422(self):
        response = self.payments_api.paymentOrder.settle_payment_order(0)
        self.test_helper.run_tests(self, response, 422)

    # settles a payment with a non-existing id (status code 404)
    def test_settle_payment_order_404(self):
        response = self.payments_api.paymentOrder.settle_payment_order(uuid.uuid4())
        self.test_helper.run_tests(self, response, 404)


if __name__ == '__main__':
    unittest.main()
