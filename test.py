import requests

def create_customer():
    name = input("Enter customer name: ")
    email = input("Enter customer email: ")
    response = requests.post('http://localhost:5000/create_customer', json={'name': name, 'email': email})
    print(response.json())
    create_subscription(response.json().get('id'))  # Passes the customer ID to create_subscription()

def create_subscription(customer_id):
    if customer_id:
        price_id = input("Enter price ID: ")
        response = requests.post('http://localhost:5000/create_subscription', json={'customer_id': customer_id, 'price_id': price_id})
        print(response.json())
        choice = input("Do you want to cancel this subscription? (yes/no): ")
        if choice.lower() == 'yes':
            cancel_subscription(response.json().get('id'))  # Passes the subscription ID to cancel_subscription()
    else:
        print("Customer ID is missing. Unable to create subscription.")

def cancel_subscription(subscription_id):
    if subscription_id:
        response = requests.post('http://localhost:5000/cancel_subscription', json={'subscription_id': subscription_id})
        print(response.json())
    else:
        print("Subscription ID is missing. Unable to cancel subscription.")

if __name__ == '__main__':
    create_customer()
