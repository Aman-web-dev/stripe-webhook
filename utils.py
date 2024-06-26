import stripe

from supabase import create_client, Client
import uuid
import os

stripe.api_key = "sk_test_51PNrL501Pe4bfmvIaMxBrExCl2J41NECyaBlNHpATxxu881MCVxqt5pup0353Z63KyMvyUfu6FBKNLDkVpJfc3hc00wt1CYNr2"

# Initialize Supabase client
# url: str = os.environ["SUPABASE_URL"]
# key: str = os.environ["SUPABASE_API_KEY"]

url: str = "https://tyzqjwnqqrsszanzcxeq.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR5enFqd25xcXJzc3phbnpjeGVxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxNzU1NjA3OSwiZXhwIjoyMDMzMTMyMDc5fQ.B1D4PS8o9yz1HmAgmK6cZlHuM1tbzK-eVNDJqBF8WDA"
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


def upload_customer_details(email: str, name: str,phone:str,customer_id:str) -> dict:
    user_id = str(uuid.uuid4())
    data = {
        "id": user_id,
        "email": email,
        "stripe_id":customer_id,
        "name": name,
        "phone_number":phone
    }
    response = supabase.table("customer").insert(data).execute()
    return response
    
def upload_subscription_details(customer_id: str,subscription_id:str, plan: str, status: str = "active") -> dict:
    id = str(uuid.uuid4())
    data = {
        "id":id,
        "subscription_id": subscription_id,
        "user_stripe_id": customer_id,
        "plan": plan,   
        "status": status
    }
    response = supabase.table("subscription").insert(data).execute()
    return response


def update_subscription_cancellation(subscription_id: str) -> dict:
    response = supabase.table("subscription").update({"status": "deleted"}).eq("subscription_id", subscription_id).execute()
    return response