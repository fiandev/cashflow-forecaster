from app import app
from models import db, User, Business
import sys

def fix_user_business(email):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f"User with email {email} not found.")
            return

        print(f"Checking business for user: {user.name} (ID: {user.id})")
        
        business = Business.query.filter_by(owner_id=user.id).first()
        if business:
            print(f"✅ User already has business: {business.name} (ID: {business.id})")
        else:
            print("❌ User has NO business. Creating one now...")
            new_business = Business(
                owner_id=user.id,
                name=f"{user.name}'s Business",
                currency="USD",
                country="USA"
            )
            db.session.add(new_business)
            db.session.commit()
            print(f"✅ Created new business: {new_business.name} (ID: {new_business.id})")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        email = sys.argv[1]
        fix_user_business(email)
    else:
        print("Usage: python fix_business.py <email>")
