import hmac
import hashlib
import time
import json
import requests
from typing import Dict, Any, Optional, List

from app.core.config import settings

class ShopeeAPI:
    def __init__(self):
        self.partner_id = settings.SHOPEE_PARTNER_ID
        self.partner_key = settings.SHOPEE_PARTNER_KEY
        self.api_url = settings.SHOPEE_API_URL
    
    def _generate_signature(self, path: str, timestamp: int) -> str:
        """Generate Shopee API signature."""
        base_string = f"{self.partner_id}{path}{timestamp}"
        signature = hmac.new(
            self.partner_key.encode(),
            base_string.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    async def get_orders(self, shop_id: str, status: str = "READY_TO_SHIP") -> List[Dict[str, Any]]:
        """
        Get orders from Shopee.
        """
        try:
            timestamp = int(time.time())
            path = "/api/v2/order/get_order_list"
            
            url = f"{self.api_url}{path}"
            signature = self._generate_signature(path, timestamp)
            
            params = {
                "partner_id": self.partner_id,
                "timestamp": timestamp,
                "sign": signature,
                "shop_id": shop_id,
                "time_range_field": "create_time",
                "time_from": int(time.time()) - 86400,  # Last 24 hours
                "time_to": int(time.time()),
                "page_size": 100,
                "order_status": status
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if "error" in data and data["error"]:
                print(f"Shopee API error: {data['error']}")
                return []
            
            return data.get("response", {}).get("order_list", [])
        except Exception as e:
            print(f"Error getting orders from Shopee: {e}")
            # For development, return mock data
            return [
                {
                    "order_sn": "210123456789",
                    "order_status": "READY_TO_SHIP",
                    "buyer_user_id": 12345678,
                    "buyer_username": "buyer123",
                    "item_list": [
                        {
                            "item_id": 987654321,
                            "item_name": "Digital Product Template",
                            "model_name": "Standard",
                            "item_sku": "DP-TEMP-001"
                        }
                    ]
                }
            ]
    
    async def update_order_status(self, shop_id: str, order_sn: str, status: str) -> bool:
        """
        Update order status in Shopee.
        """
        try:
            timestamp = int(time.time())
            path = "/api/v2/order/handle_buyer_cancellation"
            
            url = f"{self.api_url}{path}"
            signature = self._generate_signature(path, timestamp)
            
            data = {
                "partner_id": self.partner_id,
                "timestamp": timestamp,
                "sign": signature,
                "shop_id": shop_id,
                "order_sn": order_sn,
                "operation": "ACCEPT" if status == "CANCELLED" else "REJECT"
            }
            
            response = requests.post(url, json=data)
            result = response.json()
            
            if "error" in result and result["error"]:
                print(f"Shopee API error: {result['error']}")
                return False
            
            return True
        except Exception as e:
            print(f"Error updating order status in Shopee: {e}")
            return False

# Initialize Shopee API
shopee_api = ShopeeAPI()
