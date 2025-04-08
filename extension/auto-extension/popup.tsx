import { useState, useEffect } from "react"
import { Storage } from "@plasmohq/storage"

const storage = new Storage()

function IndexPopup() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [apiKey, setApiKey] = useState("")
  const [apiUrl, setApiUrl] = useState("http://localhost:8000")
  const [status, setStatus] = useState("Not connected")
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    // Load saved settings
    const loadSettings = async () => {
      const savedApiKey = await storage.get("apiKey")
      const savedApiUrl = await storage.get("apiUrl")
      const savedLoginStatus = await storage.get("isLoggedIn")

      if (savedApiKey) setApiKey(savedApiKey)
      if (savedApiUrl) setApiUrl(savedApiUrl)
      if (savedLoginStatus) setIsLoggedIn(savedLoginStatus === "true")
    }

    loadSettings()
  }, [])

  const handleLogin = async () => {
    setLoading(true)
    try {
      // In a real implementation, we would validate the API key
      await storage.set("apiKey", apiKey)
      await storage.set("apiUrl", apiUrl)
      await storage.set("isLoggedIn", "true")
      setIsLoggedIn(true)
      setStatus("Connected")
    } catch (error) {
      console.error("Login error:", error)
      setStatus("Connection failed")
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = async () => {
    await storage.set("isLoggedIn", "false")
    setIsLoggedIn(false)
    setStatus("Not connected")
  }

  const fetchOrders = async () => {
    setLoading(true)
    try {
      // In a real implementation, we would fetch orders from the API
      // For now, we'll use mock data
      setOrders([
        { id: 1, shopee_id: "SHP123456", status: "PAID", product: "Digital Template" },
        { id: 2, shopee_id: "SHP789012", status: "PENDING", product: "Account Access" }
      ])
      setStatus("Orders fetched")
    } catch (error) {
      console.error("Error fetching orders:", error)
      setStatus("Failed to fetch orders")
    } finally {
      setLoading(false)
    }
  }

  const deliverOrder = async (orderId) => {
    setLoading(true)
    try {
      // In a real implementation, we would call the API to deliver the order
      setStatus(`Order ${orderId} delivered successfully`)
      // Update the order status in the list
      setOrders(orders.map(order =>
        order.id === orderId ? { ...order, status: "DELIVERED" } : order
      ))
    } catch (error) {
      console.error("Error delivering order:", error)
      setStatus(`Failed to deliver order ${orderId}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ width: 350, padding: 16 }}>
      <h2 style={{ color: "#4f46e5", marginBottom: 16 }}>
        AUTO Marketplace Extension
      </h2>

      {!isLoggedIn ? (
        <div>
          <div style={{ marginBottom: 12 }}>
            <label style={{ display: "block", marginBottom: 4 }}>
              API URL:
            </label>
            <input
              type="text"
              value={apiUrl}
              onChange={(e) => setApiUrl(e.target.value)}
              style={{ width: "100%", padding: 8, borderRadius: 4, border: "1px solid #ccc" }}
            />
          </div>

          <div style={{ marginBottom: 12 }}>
            <label style={{ display: "block", marginBottom: 4 }}>
              API Key:
            </label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              style={{ width: "100%", padding: 8, borderRadius: 4, border: "1px solid #ccc" }}
            />
          </div>

          <button
            onClick={handleLogin}
            disabled={loading || !apiKey || !apiUrl}
            style={{
              backgroundColor: "#4f46e5",
              color: "white",
              padding: "8px 16px",
              borderRadius: 4,
              border: "none",
              cursor: loading ? "not-allowed" : "pointer",
              opacity: loading || !apiKey || !apiUrl ? 0.7 : 1
            }}
          >
            {loading ? "Connecting..." : "Connect"}
          </button>
        </div>
      ) : (
        <div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
            <span style={{ color: "green" }}>{status}</span>
            <button
              onClick={handleLogout}
              style={{
                backgroundColor: "#ef4444",
                color: "white",
                padding: "4px 8px",
                borderRadius: 4,
                border: "none",
                cursor: "pointer"
              }}
            >
              Disconnect
            </button>
          </div>

          <div style={{ marginBottom: 16 }}>
            <button
              onClick={fetchOrders}
              disabled={loading}
              style={{
                backgroundColor: "#4f46e5",
                color: "white",
                padding: "8px 16px",
                borderRadius: 4,
                border: "none",
                cursor: loading ? "not-allowed" : "pointer",
                opacity: loading ? 0.7 : 1,
                marginRight: 8
              }}
            >
              {loading ? "Loading..." : "Fetch Orders"}
            </button>
          </div>

          {orders.length > 0 && (
            <div>
              <h3 style={{ marginBottom: 8 }}>Orders</h3>
              <div style={{ maxHeight: 300, overflowY: "auto" }}>
                {orders.map(order => (
                  <div
                    key={order.id}
                    style={{
                      padding: 8,
                      borderRadius: 4,
                      border: "1px solid #ccc",
                      marginBottom: 8,
                      backgroundColor: order.status === "DELIVERED" ? "#f0fdf4" : "white"
                    }}
                  >
                    <div style={{ display: "flex", justifyContent: "space-between" }}>
                      <span><strong>ID:</strong> {order.id}</span>
                      <span style={{
                        padding: "2px 6px",
                        borderRadius: 4,
                        fontSize: 12,
                        backgroundColor:
                          order.status === "PAID" ? "#dbeafe" :
                          order.status === "DELIVERED" ? "#dcfce7" :
                          "#fef9c3",
                        color:
                          order.status === "PAID" ? "#1e40af" :
                          order.status === "DELIVERED" ? "#166534" :
                          "#854d0e"
                      }}>
                        {order.status}
                      </span>
                    </div>
                    <div><strong>Shopee ID:</strong> {order.shopee_id}</div>
                    <div><strong>Product:</strong> {order.product}</div>
                    {order.status === "PAID" && (
                      <button
                        onClick={() => deliverOrder(order.id)}
                        style={{
                          backgroundColor: "#22c55e",
                          color: "white",
                          padding: "4px 8px",
                          borderRadius: 4,
                          border: "none",
                          cursor: "pointer",
                          marginTop: 8,
                          fontSize: 12
                        }}
                      >
                        Deliver Now
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      <div style={{ marginTop: 16, fontSize: 12, color: "#6b7280", textAlign: "center" }}>
        AUTO Marketplace Extension v1.0.0
      </div>
    </div>
  )
}

export default IndexPopup
