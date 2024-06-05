import stripe

from supabase import create_client, Client
import uuid
import os

stripe.api_key = "sk_test_51PNrL501Pe4bfmvIaMxBrExCl2J41NECyaBlNHpATxxu881MCVxqt5pup0353Z63KyMvyUfu6FBKNLDkVpJfc3hc00wt1CYNr2"

# Initialize Supabase client
url: str = os.environ["SUPABASE_URL"]
key: str = os.environ["SUPABASE_API_KEY"]
supabase: Client = create_client(url, key)



def create_stripe_customer(name, email):
    customer = stripe.Customer.create(
        name=name,
        email=email,
    )
    return customer


def create_stripe_subscription(customer_id, price_id):
    subscription = stripe.Subscription.create(
        customer=customer_id,
        items=[{"price": price_id}],
    )
    return subscription



def cancel_stripe_subscription(subscription_id):
    subscription = stripe.Subscription.delete(subscription_id)
    return subscription


def upload_customer_details(email: str, name: str,phone:str) -> dict:
    user_id = str(uuid.uuid4())
    data = {
        "id": user_id,
        "email": email,
        "name": name,
        "phone_number":phone
    }
    response = supabase.table("user").insert(data).execute()
    return response
    
def upload_subscription_details(user_id: str, plan: str, status: str = "active") -> dict:
    subscription_id = str(uuid.uuid4())
    data = {
        "id": subscription_id,
        "user_id": user_id,
        "plan": plan,
        "status": status
    }
    response = supabase.table("subscription").insert(data).execute()
    return response


def update_subscription_cancellation(subscription_id: str) -> dict:
    response = supabase.table("subscription").update({"status": "cancelled"}).eq("id", subscription_id).execute()
    return response