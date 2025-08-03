import React from "react"
import { Link } from "gatsby"

interface LayoutProps {
  children: React.ReactNode
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div style={{ 
      minHeight: "100vh",
      display: "flex",
      flexDirection: "column",
      fontFamily: "system-ui, sans-serif"
    }}>
      <header style={{
        backgroundColor: "#1e40af",
        color: "white",
        padding: "1rem 2rem",
        boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
      }}>
        <nav style={{ 
          display: "flex", 
          alignItems: "center", 
          justifyContent: "space-between",
          maxWidth: "1200px",
          margin: "0 auto"
        }}>
          <Link 
            to="/" 
            style={{ 
              color: "white", 
              textDecoration: "none", 
              fontSize: "1.5rem", 
              fontWeight: "bold" 
            }}
          >
            Rate My Legislator
          </Link>
          <div style={{ display: "flex", gap: "2rem" }}>
            <Link 
              to="/members" 
              style={{ 
                color: "white", 
                textDecoration: "none",
                padding: "0.5rem 1rem",
                borderRadius: "4px",
                transition: "background-color 0.2s"
              }}
              onMouseOver={(e) => e.currentTarget.style.backgroundColor = "rgba(255,255,255,0.1)"}
              onMouseOut={(e) => e.currentTarget.style.backgroundColor = "transparent"}
            >
              Members
            </Link>
            <Link 
              to="/bills" 
              style={{ 
                color: "white", 
                textDecoration: "none",
                padding: "0.5rem 1rem",
                borderRadius: "4px",
                transition: "background-color 0.2s"
              }}
              onMouseOver={(e) => e.currentTarget.style.backgroundColor = "rgba(255,255,255,0.1)"}
              onMouseOut={(e) => e.currentTarget.style.backgroundColor = "transparent"}
            >
              Bills
            </Link>
          </div>
        </nav>
      </header>
      
      <main style={{ 
        flex: 1, 
        padding: "2rem",
        maxWidth: "1200px",
        margin: "0 auto",
        width: "100%"
      }}>
        {children}
      </main>
      
      <footer style={{ 
        backgroundColor: "#f8fafc", 
        padding: "1rem 2rem", 
        textAlign: "center",
        borderTop: "1px solid #e2e8f0",
        color: "#64748b"
      }}>
        <p>© 2025 Rate My Legislator - Tracking Hawaii State Legislature</p>
      </footer>
    </div>
  )
}

export default Layout