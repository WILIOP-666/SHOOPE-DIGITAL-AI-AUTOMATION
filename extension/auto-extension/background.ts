import { Storage } from "@plasmohq/storage"
import axios from "axios"

// Initialize storage
const storage = new Storage()

// Function to fetch orders from the API
async function fetchOrders() {
  try {
    const apiUrl = await storage.get("apiUrl")
    const apiKey = await storage.get("apiKey")
    
    if (!apiUrl || !apiKey) {
      console.error("API URL or API Key not set")
      return []
    }
    
    const response = await axios.get(`${apiUrl}/api/orders`, {
      headers: {
        Authorization: `Bearer ${apiKey}`
      }
    })
    
    return response.data
  } catch (error) {
    console.error("Error fetching orders:", error)
    return []
  }
}

// Function to deliver a digital product
async function deliverProduct(orderId: number) {
  try {
    const apiUrl = await storage.get("apiUrl")
    const apiKey = await storage.get("apiKey")
    
    if (!apiUrl || !apiKey) {
      console.error("API URL or API Key not set")
      return false
    }
    
    const response = await axios.post(
      `${apiUrl}/api/orders/${orderId}/deliver`,
      {},
      {
        headers: {
          Authorization: `Bearer ${apiKey}`
        }
      }
    )
    
    return response.status === 200
  } catch (error) {
    console.error(`Error delivering product for order ${orderId}:`, error)
    return false
  }
}

// Check for new orders periodically
async function checkForNewOrders() {
  const isLoggedIn = await storage.get("isLoggedIn")
  
  if (isLoggedIn !== "true") {
    return
  }
  
  const orders = await fetchOrders()
  const paidOrders = orders.filter(order => order.status === "PAID" && !order.is_delivered)
  
  if (paidOrders.length > 0) {
    // Show notification for new paid orders
    chrome.notifications.create({
      type: "basic",
      iconUrl: "assets/icon.png",
      title: "AUTO Marketplace",
      message: `You have ${paidOrders.length} new paid order(s) ready for delivery!`,
      priority: 2
    })
  }
}

// Set up periodic check (every 5 minutes)
setInterval(checkForNewOrders, 5 * 60 * 1000)

// Listen for messages from popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "FETCH_ORDERS") {
    fetchOrders().then(orders => {
      sendResponse({ success: true, orders })
    })
    return true // Required for async response
  }
  
  if (message.type === "DELIVER_ORDER") {
    deliverProduct(message.orderId).then(success => {
      sendResponse({ success })
    })
    return true // Required for async response
  }
})

// Initial check on extension load
checkForNewOrders()
