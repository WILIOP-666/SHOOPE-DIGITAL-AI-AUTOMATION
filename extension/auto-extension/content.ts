import { Storage } from "@plasmohq/storage"

// Initialize storage
const storage = new Storage()

// Function to extract order information from Shopee order page
function extractOrderInfo() {
  // This is a simplified example - in a real implementation, 
  // we would need to adapt this to the actual Shopee page structure
  
  // Check if we're on an order page
  if (!window.location.href.includes("shopee") || !window.location.href.includes("order")) {
    return null
  }
  
  try {
    // Example selectors - these would need to be updated based on actual Shopee DOM structure
    const orderIdElement = document.querySelector(".order-id")
    const orderStatusElement = document.querySelector(".order-status")
    const productNameElement = document.querySelector(".product-name")
    
    if (!orderIdElement || !orderStatusElement || !productNameElement) {
      return null
    }
    
    // Extract the order information
    const orderId = orderIdElement.textContent.trim()
    const orderStatus = orderStatusElement.textContent.trim()
    const productName = productNameElement.textContent.trim()
    
    return {
      shopee_order_id: orderId,
      status: orderStatus === "Paid" ? "PAID" : orderStatus,
      product_name: productName
    }
  } catch (error) {
    console.error("Error extracting order info:", error)
    return null
  }
}

// Function to add AUTO button to the page
function addAutoButton() {
  // Check if we're on an order page
  if (!window.location.href.includes("shopee") || !window.location.href.includes("order")) {
    return
  }
  
  // Check if button already exists
  if (document.querySelector("#auto-deliver-button")) {
    return
  }
  
  // Create button
  const button = document.createElement("button")
  button.id = "auto-deliver-button"
  button.textContent = "Deliver with AUTO"
  button.style.backgroundColor = "#4f46e5"
  button.style.color = "white"
  button.style.padding = "8px 16px"
  button.style.borderRadius = "4px"
  button.style.border = "none"
  button.style.cursor = "pointer"
  button.style.margin = "10px 0"
  
  // Add click event
  button.addEventListener("click", async () => {
    const orderInfo = extractOrderInfo()
    if (!orderInfo) {
      alert("Could not extract order information")
      return
    }
    
    // Send message to background script
    chrome.runtime.sendMessage(
      { 
        type: "PROCESS_SHOPEE_ORDER", 
        orderInfo 
      },
      (response) => {
        if (response && response.success) {
          alert("Order processed successfully!")
          // Update button
          button.textContent = "Delivered ✓"
          button.style.backgroundColor = "#22c55e"
          button.disabled = true
        } else {
          alert("Failed to process order. Please try again.")
        }
      }
    )
  })
  
  // Find a good place to insert the button
  // This would need to be adapted to the actual Shopee page structure
  const targetElement = document.querySelector(".order-actions")
  if (targetElement) {
    targetElement.appendChild(button)
  }
}

// Run when page loads
window.addEventListener("load", () => {
  // Check if extension is logged in
  storage.get("isLoggedIn").then(isLoggedIn => {
    if (isLoggedIn === "true") {
      // Add button with slight delay to ensure page is fully loaded
      setTimeout(addAutoButton, 1000)
    }
  })
})

// Run when URL changes (for single-page applications)
let lastUrl = location.href
new MutationObserver(() => {
  if (location.href !== lastUrl) {
    lastUrl = location.href
    storage.get("isLoggedIn").then(isLoggedIn => {
      if (isLoggedIn === "true") {
        setTimeout(addAutoButton, 1000)
      }
    })
  }
}).observe(document, { subtree: true, childList: true })
