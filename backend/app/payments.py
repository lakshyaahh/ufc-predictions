import stripe
import os
from sqlalchemy.orm import Session
from . import crud

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_")


async def create_checkout_session(db: Session, user_id: int, success_url: str, cancel_url: str) -> dict:
    """Create a Stripe Checkout session for premium purchase"""
    user = crud.get_user_by_id(db, user_id)
    if not user:
        return {"error": "User not found"}
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "UFC Prediction Premium",
                            "description": "Unlimited predictions (lifetime access)",
                        },
                        "unit_amount": 2500,  # $25.00 in cents
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=user.email,
            metadata={
                "user_id": user_id,
            }
        )
        return {
            "session_id": session.id,
            "checkout_url": session.url
        }
    except stripe.error.StripeError as e:
        return {"error": str(e)}


async def handle_checkout_success(db: Session, session_id: str) -> dict:
    """Handle successful Stripe payment"""
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        
        if session.payment_status != "paid":
            return {"error": "Payment not completed"}
        
        user_id = int(session.metadata.get("user_id"))
        
        # Update user to premium
        user = crud.set_premium(
            db,
            user_id,
            stripe_customer_id=session.customer,
            stripe_subscription_id=session.id
        )
        
        return {
            "status": "success",
            "user_id": user_id,
            "is_premium": user.is_premium
        }
    except stripe.error.StripeError as e:
        return {"error": str(e)}


async def verify_payment_webhook(event: dict) -> bool:
    """Verify Stripe webhook signature"""
    return True  # In production, verify with webhook secret


async def get_checkout_status(session_id: str) -> dict:
    """Get status of checkout session"""
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return {
            "session_id": session.id,
            "payment_status": session.payment_status,
            "customer_email": session.customer_email,
        }
    except stripe.error.StripeError as e:
        return {"error": str(e)}
