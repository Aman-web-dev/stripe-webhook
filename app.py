from flask import Flask, request, jsonify
from utils import create_customer , create_subscription ,cancel_subscription
import stripe

app = Flask(__name__)

# Set your secret key: remember to change this to your live secret key in production
stripe.api_key = "sk_test_51PNrL501Pe4bfmvIaMxBrExCl2J41NECyaBlNHpATxxu881MCVxqt5pup0353Z63KyMvyUfu6FBKNLDkVpJfc3hc00wt1CYNr2"
endpoint_secret = 'your_endpoint_secret'  # Replace with your actual endpoint secret

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
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
        return jsonify({'error': str(e)}), 400

    # Handle the event
    if event['type'] == 'customer.created':
        handle_customer_created(event['data']['object'])
    elif event['type'] == 'customer.subscription.created':
        handle_subscription_created(event['data']['object'])
    elif event['type'] == 'customer.subscription.deleted':
        handle_subscription_deleted(event['data']['object'])
    else:
        print('Unhandled event type {}'.format(event['type']))

    return jsonify({'status': 'success'}), 200

def handle_customer_created(customer):
    print('Customer created:', customer)

def handle_subscription_created(subscription):
    print('Subscription created:', subscription)

def handle_subscription_deleted(subscription):
    print('Subscription deleted:', subscription)

@app.route('/create_customer', methods=['POST'])
def create_customer_endpoint():
    data = request.json
    customer = create_customer(data['name'], data['email'])
    return jsonify(customer), 201

@app.route('/create_subscription', methods=['POST'])
def create_subscription_endpoint():
    data = request.json
    subscription = create_subscription(data['customer_id'], data['price_id'])
    return jsonify(subscription), 201

@app.route('/cancel_subscription', methods=['POST'])
def cancel_subscription_endpoint():
    data = request.json
    subscription = cancel_subscription(data['subscription_id'])
    return jsonify(subscription), 200

if __name__ == '__main__':
    app.run(port=5000)
