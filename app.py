from flask import Flask, request, jsonify
from utils import create_stripe_customer, create_stripe_subscription, cancel_stripe_subscription
from utils import upload_customer_details, upload_subscription_details, update_subscription_cancellation
import stripe

app = Flask(__name__)

# Set your secret key: remember to change this to your live secret key in production
stripe.api_key = "sk_test_51PNrL501Pe4bfmvIaMxBrExCl2J41NECyaBlNHpATxxu881MCVxqt5pup0353Z63KyMvyUfu6FBKNLDkVpJfc3hc00wt1CYNr2"
endpoint_secret = 'whsec_qXCiL2CoPwmd0JLDGMuXbgL1ERKtz9EL'


@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    print(payload)
    sig_header = request.headers.get('STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return jsonify({'error': str(e)}), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return jsonify({'error': str(e)}), 404

    # Handle the event
    if event['type'] == 'customer.created':
        handle_customer_created(event['data']['object'])
        print(payload)
    elif event['type'] == 'customer.subscription.created':
        handle_subscription_created(event['data']['object'])
    elif event['type'] == 'customer.subscription.deleted':
        handle_subscription_deleted(event['data']['object'])
    else:
        print('Unhandled event type {}'.format(event['type']))

    return jsonify({'status': 'success',"response":event}), 200


def handle_customer_created(customer):
    print('Customer created:', customer)
    customer_id = customer.get('id') 
    email = customer['email']
    name = customer['name']
    phone = customer.get('phone', '')  # Assuming phone is optional
    upload_customer_details(email, name, phone,customer_id)

def handle_subscription_created(subscription):
    print('Subscription created:', subscription)
    subscription_id = subscription.get('id')  
    customer_id = subscription['customer']  # Assuming 'customer' contains the user ID
    plan = subscription['plan']['id']
    status = subscription['status']
    upload_subscription_details(user_id=customer_id, plan=plan, status=status,subscription_id=subscription_id)

def handle_subscription_deleted(subscription):
    print('Subscription deleted:', subscription)
    subscription_id = subscription['id']
    update_subscription_cancellation(subscription_id)






@app.route('/create_stripe_customer', methods=['POST'])
def create_stripe_customer_endpoint():
    data = request.json
    customer = create_stripe_customer(data['name'], data['email'])
    return jsonify(customer), 201

@app.route('/create_stripe_subscription', methods=['POST'])
def create_stripe_subscription_endpoint():
    data = request.json
    subscription = create_stripe_subscription(data['customer_id'], data['price_id'])
    return jsonify(subscription), 201

@app.route('/cancel_stripe_subscription', methods=['POST'])
def cancel_stripe_subscription_endpoint():
    data = request.json
    subscription = cancel_stripe_subscription(data['subscription_id'])
    return jsonify(subscription), 200

if __name__ == '__main__':
    app.run(port=5000)
