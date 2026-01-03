import { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Link from "next/link";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const STRIPE_KEY = process.env.NEXT_PUBLIC_STRIPE_KEY;

export default function Premium() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/auth");
      return;
    }

    // Check if already premium
    fetch(`${API_URL}/user/stats`, {
      headers: { "Authorization": `Bearer ${token}` }
    })
      .then((res) => res.json())
      .then((data) => {
        setUser(data);
        if (data.is_premium) {
          router.push("/");
        }
      })
      .catch((err) => {
        console.error(err);
        router.push("/auth");
      });
  }, [router]);

  const handleCheckout = async () => {
    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem("token");
      
      // Get current URL for redirect
      const successUrl = `${window.location.origin}/?upgrade=success`;
      const cancelUrl = `${window.location.origin}/premium`;

      const res = await fetch(`${API_URL}/stripe/create-checkout`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          success_url: successUrl,
          cancel_url: cancelUrl
        })
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Failed to create checkout");
      }

      const data = await res.json();
      
      // Redirect to Stripe Checkout
      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      } else {
        throw new Error("No checkout URL returned");
      }
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "0 auto", padding: "20px", fontFamily: "system-ui, sans-serif" }}>
      <div style={{ marginBottom: "24px" }}>
        <Link href="/"><a style={{ color: "#2196F3", textDecoration: "none" }}>← Back to Home</a></Link>
      </div>

      <h1>🚀 Upgrade to Premium</h1>

      <div style={{
        border: "2px solid #FFD700",
        borderRadius: "12px",
        padding: "32px",
        textAlign: "center",
        backgroundColor: "#FFFACD",
        marginBottom: "24px"
      }}>
        <div style={{ fontSize: "48px", marginBottom: "16px" }}>✨</div>
        <h2 style={{ margin: "0 0 16px 0" }}>Unlimited Predictions</h2>
        <p style={{ color: "#666", margin: 0, marginBottom: "24px" }}>Get unlimited UFC fight predictions for life with a single payment.</p>
        
        <div style={{
          display: "flex",
          alignItems: "baseline",
          justifyContent: "center",
          marginBottom: "24px"
        }}>
          <span style={{ fontSize: "48px", fontWeight: "bold", color: "#2196F3" }}>$25</span>
          <span style={{ color: "#666", marginLeft: "8px" }}>/lifetime</span>
        </div>

        <div style={{
          textAlign: "left",
          backgroundColor: "white",
          borderRadius: "8px",
          padding: "16px",
          marginBottom: "24px"
        }}>
          <ul style={{ margin: 0, paddingLeft: "20px" }}>
            <li>✅ Unlimited predictions</li>
            <li>✅ Instant fighter analysis</li>
            <li>✅ Confidence intervals & stats</li>
            <li>✅ Prediction history</li>
            <li>✅ One-time payment (no subscription)</li>
          </ul>
        </div>

        {error && (
          <div style={{
            color: "red",
            backgroundColor: "#FFEBEE",
            padding: "12px",
            borderRadius: "8px",
            marginBottom: "16px"
          }}>
            {error}
          </div>
        )}

        <button
          onClick={handleCheckout}
          disabled={loading}
          style={{
            width: "100%",
            padding: "14px",
            backgroundColor: "#4CAF50",
            color: "white",
            border: "none",
            borderRadius: "8px",
            fontSize: "16px",
            fontWeight: "bold",
            cursor: loading ? "not-allowed" : "pointer",
            opacity: loading ? 0.6 : 1
          }}
        >
          {loading ? "Redirecting to Stripe..." : "Upgrade Now with Stripe"}
        </button>

        <p style={{ fontSize: "12px", color: "#666", marginTop: "16px", margin: 0 }}>
          💳 Secure payment powered by Stripe
        </p>
      </div>

      <div style={{
        backgroundColor: "#F5F5F5",
        borderRadius: "8px",
        padding: "16px",
        marginBottom: "24px"
      }}>
        <h3 style={{ marginTop: 0 }}>Questions?</h3>
        <p style={{ color: "#666", margin: 0 }}>
          These predictions are for entertainment and analytical purposes. Not gambling advice.
        </p>
      </div>

      <div style={{
        textAlign: "center",
        fontSize: "12px",
        color: "#999"
      }}>
        <p>Need help? Contact support or email hello@ufcpredictor.com</p>
      </div>
    </div>
  );
}
