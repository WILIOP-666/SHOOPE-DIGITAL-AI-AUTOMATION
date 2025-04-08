import logging
from sqlalchemy.orm import Session

from app.db.session import Base, engine
from app.core.security import get_password_hash
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.ai_config import AIConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Check if we already have users
    user = db.query(User).first()
    if not user:
        logger.info("Creating initial admin user")
        admin_user = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin"),
            full_name="Administrator",
            is_admin=True,
        )
        db.add(admin_user)
        db.commit()
        
        # Create default AI configuration
        ai_config = AIConfig(
            user_id=admin_user.id,
            is_active=True,
            store_level="user_id",
            faq_threshold=0.75,
        )
        db.add(ai_config)
        db.commit()
        
        logger.info("Initial data created")
    else:
        logger.info("Database already initialized")
