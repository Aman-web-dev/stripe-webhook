import stripe

stripe.api_key = "sk_test_51PNrL501Pe4bfmvIaMxBrExCl2J41NECyaBlNHpATxxu881MCVxqt5pup0353Z63KyMvyUfu6FBKNLDkVpJfc3hc00wt1CYNr2"

def create_customer(name, email):
    customer = stripe.Customer.create(
        name=name,
        email=email,
    )
    return customer


def create_subscription(customer_id, price_id):
    subscription = stripe.Subscription.create(
        customer=customer_id,
        items=[{"price": price_id}],
    )
    return subscription



def cancel_subscription(subscription_id):
    subscription = stripe.Subscription.delete(subscription_id)
    return subscription



