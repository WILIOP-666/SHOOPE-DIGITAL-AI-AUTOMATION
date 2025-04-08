import json
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.order import Order, OrderStatus
from app.models.product import Product, ProductType

async def deliver_digital_product(order_id: int, db: Session) -> Dict[str, Any]:
    """
    Deliver a digital product based on the order.
    """
    # Get the order
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return {"success": False, "message": "Order not found"}
    
    # Check if order is paid
    if order.status != OrderStatus.PAID:
        return {"success": False, "message": "Order is not paid"}
    
    # Check if order is already delivered
    if order.is_delivered:
        return {"success": False, "message": "Order is already delivered"}
    
    # Get the product
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        return {"success": False, "message": "Product not found"}
    
    # Deliver based on product type
    delivery_data = {}
    
    if product.product_type == ProductType.TEMPLATE:
        # Deliver template content
        delivery_data = {
            "type": "template",
            "content": product.content,
            "instructions": "Here is your template. You can use it right away."
        }
    
    elif product.product_type == ProductType.ACCOUNT:
        # Deliver account details
        delivery_data = {
            "type": "account",
            "details": product.content,
            "instructions": "Here are your account details. Keep them secure."
        }
    
    elif product.product_type == ProductType.LINK:
        # Deliver link
        delivery_data = {
            "type": "link",
            "url": product.content,
            "instructions": "Click the link to access your digital product."
        }
    
    elif product.product_type == ProductType.VOUCHER:
        # Deliver voucher code
        delivery_data = {
            "type": "voucher",
            "code": product.content,
            "instructions": "Use this voucher code to redeem your product."
        }
    
    # Update order
    order.status = OrderStatus.DELIVERED
    order.is_delivered = True
    order.delivery_data = json.dumps(delivery_data)
    db.commit()
    
    return {
        "success": True,
        "message": "Product delivered successfully",
        "delivery_data": delivery_data
    }
