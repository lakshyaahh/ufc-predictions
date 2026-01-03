import { useState } from "react";
import { useRouter } from "next/router";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Auth() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isLogin, setIsLogin] = useState(true);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (isLogin) {
        // Login
        if (!username || !password) {
          throw new Error("Username and password required");
        }

        const res = await fetch(`${API_URL}/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        });

        if (!res.ok) {
          const data = await res.json();
          throw new Error(data.detail || "Login failed");
        }

        const data = await res.json();
        localStorage.setItem("token", data.access_token);
        router.push("/");
      } else {
        // Register
        if (!username || !email || !password || !confirmPassword) {
          throw new Error("All fields required");
        }

        if (password !== confirmPassword) {
          throw new Error("Passwords do not match");
        }

        if (password.length < 6) {
          throw new Error("Password must be at least 6 characters");
        }

        const res = await fetch(`${API_URL}/auth/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, email, password }),
        });

        if (!res.ok) {
          const data = await res.json();
          throw new Error(data.detail || "Registration failed");
        }

        const data = await res.json();
        localStorage.setItem("token", data.access_token);
        router.push("/");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const toggleMode = () => {
    setIsLogin(!isLogin);
    setError(null);
    setUsername("");
    setEmail("");
    setPassword("");
    setConfirmPassword("");
  };

  return (
    <div style={{
      maxWidth: "400px",
      margin: "60px auto",
      padding: "24px",
      fontFamily: "system-ui, sans-serif",
      border: "1px solid #DDD",
      borderRadius: "12px",
      boxShadow: "0 2px 8px rgba(0,0,0,0.1)"
    }}>
      <h1 style={{ textAlign: "center", margin: "0 0 24px 0" }}>🥊 UFC Predictor</h1>
      
      <h2 style={{ textAlign: "center", fontSize: "20px", marginBottom: "24px" }}>
        {isLogin ? "Login to Your Account" : "Create New Account"}
      </h2>

      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          disabled={loading}
          style={{
            padding: "10px",
            border: "1px solid #DDD",
            borderRadius: "6px",
            fontSize: "14px"
          }}
          required
        />

        {!isLogin && (
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={loading}
            style={{
              padding: "10px",
              border: "1px solid #DDD",
              borderRadius: "6px",
              fontSize: "14px"
            }}
            required
          />
        )}

        <input
          type="password"
          placeholder="Password (min 6 characters)"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          disabled={loading}
          style={{
            padding: "10px",
            border: "1px solid #DDD",
            borderRadius: "6px",
            fontSize: "14px"
          }}
          required
        />

        {!isLogin && (
          <input
            type="password"
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            disabled={loading}
            style={{
              padding: "10px",
              border: "1px solid #DDD",
              borderRadius: "6px",
              fontSize: "14px"
            }}
            required
          />
        )}

        {error && (
          <div style={{
            color: "red",
            backgroundColor: "#FFEBEE",
            padding: "10px",
            borderRadius: "6px",
            fontSize: "12px"
          }}>
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: "10px",
            backgroundColor: "#2196F3",
            color: "white",
            border: "none",
            borderRadius: "6px",
            fontSize: "16px",
            fontWeight: "bold",
            cursor: loading ? "not-allowed" : "pointer",
            opacity: loading ? 0.6 : 1
          }}
        >
          {loading ? "Loading..." : isLogin ? "Login" : "Register"}
        </button>
      </form>

      <div style={{ textAlign: "center", marginTop: "20px" }}>
        <p style={{ color: "#666", margin: "0 0 8px 0" }}>
          {isLogin ? "Don't have an account?" : "Already have an account?"}
        </p>
        <button
          onClick={toggleMode}
          disabled={loading}
          style={{
            background: "none",
            border: "none",
            color: "#2196F3",
            cursor: "pointer",
            fontSize: "14px",
            textDecoration: "underline",
            fontWeight: "bold"
          }}
        >
          {isLogin ? "Create one here" : "Login here"}
        </button>
      </div>

      <p style={{
        fontSize: "12px",
        color: "#999",
        textAlign: "center",
        marginTop: "20px",
        borderTop: "1px solid #EEE",
        paddingTop: "16px"
      }}>
        🔒 Your data is secure and encrypted.
      </p>
    </div>
  );
}

          style={{ padding: 10 }}
        />
        <button type="submit" disabled={loading} style={{ padding: 10, cursor: loading ? "not-allowed" : "pointer" }}>
          {loading ? "Loading..." : isLogin ? "Login" : "Register"}
        </button>
      </form>
      {error && <div style={{ color: "red", marginTop: 10 }}>{error}</div>}
      <div style={{ marginTop: 20, textAlign: "center" }}>
        <button onClick={() => setIsLogin(!isLogin)} style={{ background: "none", border: "none", cursor: "pointer", color: "blue" }}>
          {isLogin ? "Need an account? Register" : "Have an account? Login"}
        </button>
      </div>
    </div>
  );
}
