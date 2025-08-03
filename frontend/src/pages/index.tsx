import * as React from "react"
import { Link } from "gatsby"
import type { HeadFC, PageProps } from "gatsby"
import Layout from "../components/Layout"
import summaryData from "../data/summary.json"
import membersData from "../data/members.json"
import billsData from "../data/bills_2025.json"

const IndexPage: React.FC<PageProps> = () => {
  const members = membersData.length
  const bills = billsData.length
  
  return (
    <Layout>
      <div>
        <div style={{ textAlign: "center", marginBottom: "3rem" }}>
          <h1 style={{ 
            fontSize: "3rem", 
            margin: "0 0 1rem 0", 
            color: "#1e293b",
            fontWeight: "700"
          }}>
            Rate My Legislator
          </h1>
          <p style={{ 
            fontSize: "1.2rem", 
            color: "#64748b", 
            maxWidth: "600px", 
            margin: "0 auto",
            lineHeight: "1.6"
          }}>
            Track Hawaii State Legislature performance with comprehensive data 
            about members, bills, and legislative activity.
          </p>
        </div>

        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
          gap: "2rem",
          marginBottom: "3rem"
        }}>
          <Link to="/members" style={{ textDecoration: "none" }}>
            <div style={{
              backgroundColor: "white",
              border: "1px solid #e2e8f0",
              borderRadius: "12px",
              padding: "2rem",
              textAlign: "center",
              boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
              transition: "all 0.2s",
              cursor: "pointer"
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.boxShadow = "0 8px 25px rgba(0,0,0,0.15)"
              e.currentTarget.style.transform = "translateY(-4px)"
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.boxShadow = "0 1px 3px rgba(0,0,0,0.1)"
              e.currentTarget.style.transform = "translateY(0)"
            }}
            >
              <div style={{
                fontSize: "3rem",
                marginBottom: "1rem",
                color: "#1e40af"
              }}>
                👥
              </div>
              <h2 style={{ 
                margin: "0 0 0.5rem 0", 
                color: "#1e293b",
                fontSize: "1.5rem"
              }}>
                Legislature Members
              </h2>
              <p style={{ 
                margin: "0 0 1rem 0", 
                color: "#64748b",
                lineHeight: "1.5"
              }}>
                Browse {members} current legislators, view their profiles, and track their activity
              </p>
              <div style={{
                backgroundColor: "#1e40af",
                color: "white",
                padding: "0.75rem 1.5rem",
                borderRadius: "6px",
                fontWeight: "500",
                display: "inline-block"
              }}>
                Explore Members
              </div>
            </div>
          </Link>

          <Link to="/bills" style={{ textDecoration: "none" }}>
            <div style={{
              backgroundColor: "white",
              border: "1px solid #e2e8f0",
              borderRadius: "12px",
              padding: "2rem",
              textAlign: "center",
              boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
              transition: "all 0.2s",
              cursor: "pointer"
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.boxShadow = "0 8px 25px rgba(0,0,0,0.15)"
              e.currentTarget.style.transform = "translateY(-4px)"
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.boxShadow = "0 1px 3px rgba(0,0,0,0.1)"
              e.currentTarget.style.transform = "translateY(0)"
            }}
            >
              <div style={{
                fontSize: "3rem",
                marginBottom: "1rem",
                color: "#059669"
              }}>
                📋
              </div>
              <h2 style={{ 
                margin: "0 0 0.5rem 0", 
                color: "#1e293b",
                fontSize: "1.5rem"
              }}>
                Legislative Bills
              </h2>
              <p style={{ 
                margin: "0 0 1rem 0", 
                color: "#64748b",
                lineHeight: "1.5"
              }}>
                Track {bills} bills from 2025, search by topic, and monitor their progress
              </p>
              <div style={{
                backgroundColor: "#059669",
                color: "white",
                padding: "0.75rem 1.5rem",
                borderRadius: "6px",
                fontWeight: "500",
                display: "inline-block"
              }}>
                Browse Bills
              </div>
            </div>
          </Link>
        </div>

        <div style={{
          backgroundColor: "white",
          border: "1px solid #e2e8f0",
          borderRadius: "12px",
          padding: "2rem",
          marginBottom: "2rem",
          boxShadow: "0 1px 3px rgba(0,0,0,0.1)"
        }}>
          <h2 style={{ 
            margin: "0 0 1.5rem 0", 
            color: "#1e293b",
            fontSize: "1.5rem",
            textAlign: "center"
          }}>
            Key Features
          </h2>
          
          <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
            gap: "1.5rem"
          }}>
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>🔍</div>
              <h3 style={{ margin: "0 0 0.5rem 0", color: "#374151" }}>Search & Filter</h3>
              <p style={{ margin: 0, color: "#64748b", fontSize: "0.9rem" }}>
                Find members by name, party, or district. Filter bills by type and status.
              </p>
            </div>
            
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>📊</div>
              <h3 style={{ margin: "0 0 0.5rem 0", color: "#374151" }}>Real-time Data</h3>
              <p style={{ margin: 0, color: "#64748b", fontSize: "0.9rem" }}>
                Data sourced directly from the Hawaii State Legislature website.
              </p>
            </div>
            
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>📱</div>
              <h3 style={{ margin: "0 0 0.5rem 0", color: "#374151" }}>Mobile Friendly</h3>
              <p style={{ margin: 0, color: "#64748b", fontSize: "0.9rem" }}>
                Responsive design works seamlessly on all devices.
              </p>
            </div>
            
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>🏛️</div>
              <h3 style={{ margin: "0 0 0.5rem 0", color: "#374151" }}>Complete Coverage</h3>
              <p style={{ margin: 0, color: "#64748b", fontSize: "0.9rem" }}>
                Track both House and Senate members and all types of legislation.
              </p>
            </div>
          </div>
        </div>

        <div style={{
          backgroundColor: "#f8fafc",
          border: "1px solid #e2e8f0",
          borderRadius: "8px",
          padding: "1.5rem",
          textAlign: "center"
        }}>
          <h2 style={{ 
            margin: "0 0 1rem 0", 
            color: "#1e293b",
            fontSize: "1.25rem"
          }}>
            About the Data
          </h2>
          <p style={{ 
            margin: 0, 
            color: "#64748b",
            lineHeight: "1.6"
          }}>
            All data is automatically scraped from the official Hawaii State Legislature 
            website and updated regularly. Information includes member details, bill text, 
            status updates, and committee assignments from publicly available records.
          </p>
        </div>
      </div>
    </Layout>
  )
}

export default IndexPage

export const Head: HeadFC = () => <title>Rate My Legislator - Hawaii Legislature Tracking</title>