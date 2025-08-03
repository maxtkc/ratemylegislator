import React from "react"
import { Link } from "gatsby"
import type { HeadFC, PageProps } from "gatsby"
import Layout from "../../components/Layout"
import billsData from "../../data/bills_2025.json"
import membersData from "../../data/members.json"

interface Bill {
  id: number
  bill_type: string
  bill_number: number
  year: number
  title: string
  description: string
  current_version: string
  introducer: string
  companion: string | null
  current_referral: string
  act_number: string | null
  governor_message_number: string | null
  current_bill_url: string
  current_pdf_url: string | null
  status_count: number
  latest_status: {
    date: string
    chamber: string
    action: string
  }
}

interface Member {
  id: number
  name: string
  latest_term: {
    title: string
    party: string
    district_type: string
    district_number: number
    district_description: string
  }
}

const BillDetailPage: React.FC<PageProps<{}, {}, {}, { id: string }>> = ({ params }) => {
  const bills = billsData as Bill[]
  const members = membersData as Member[]
  
  const bill = bills.find(b => b.id === parseInt(params.id))
  
  if (!bill) {
    return (
      <Layout>
        <div style={{ textAlign: "center", padding: "3rem" }}>
          <h1>Bill Not Found</h1>
          <p>The requested bill could not be found.</p>
          <Link to="/bills" style={{ color: "#1e40af", textDecoration: "none" }}>
            ← Back to Bills
          </Link>
        </div>
      </Layout>
    )
  }

  const getStatusColor = (action: string) => {
    if (action.toLowerCase().includes("passed")) return "#059669"
    if (action.toLowerCase().includes("introduced")) return "#3b82f6"
    if (action.toLowerCase().includes("committee")) return "#7c3aed"
    if (action.toLowerCase().includes("failed") || action.toLowerCase().includes("killed")) return "#dc2626"
    return "#64748b"
  }

  const getBillTypeColor = (type: string) => {
    switch (type) {
      case "SB": return { bg: "#eff6ff", color: "#1e40af" }
      case "HB": return { bg: "#f0fdf4", color: "#166534" }
      case "SR": return { bg: "#fef3c7", color: "#92400e" }
      case "HR": return { bg: "#fce7f3", color: "#be185d" }
      case "SCR": return { bg: "#f3e8ff", color: "#7c3aed" }
      case "HCR": return { bg: "#ecfdf5", color: "#059669" }
      default: return { bg: "#f1f5f9", color: "#475569" }
    }
  }

  const typeColors = getBillTypeColor(bill.bill_type)

  return (
    <Layout>
      <div>
        <Link 
          to="/bills" 
          style={{ 
            color: "#1e40af", 
            textDecoration: "none",
            display: "inline-flex",
            alignItems: "center",
            marginBottom: "2rem"
          }}
        >
          ← Back to Bills
        </Link>
        
        <div style={{
          backgroundColor: "white",
          border: "1px solid #e2e8f0",
          borderRadius: "8px",
          padding: "2rem",
          marginBottom: "2rem",
          boxShadow: "0 1px 3px rgba(0,0,0,0.1)"
        }}>
          <div style={{ marginBottom: "1.5rem" }}>
            <div style={{ display: "flex", gap: "1rem", alignItems: "center", marginBottom: "1rem" }}>
              <span style={{
                backgroundColor: typeColors.bg,
                color: typeColors.color,
                padding: "0.75rem 1.5rem",
                borderRadius: "8px",
                fontSize: "1.5rem",
                fontWeight: "700"
              }}>
                {bill.current_version}
              </span>
              
              <span style={{
                backgroundColor: "#f0fdf4",
                color: "#166534",
                padding: "0.5rem 1rem",
                borderRadius: "6px",
                fontSize: "1rem",
                fontWeight: "500"
              }}>
                {bill.current_referral}
              </span>
              
              {bill.companion && (
                <span style={{
                  backgroundColor: "#fef3c7",
                  color: "#92400e",
                  padding: "0.5rem 1rem",
                  borderRadius: "6px",
                  fontSize: "1rem"
                }}>
                  Companion: {bill.companion}
                </span>
              )}
            </div>
            
            <h1 style={{ 
              margin: "0 0 1rem 0", 
              color: "#1e293b",
              fontSize: "2rem",
              lineHeight: "1.3"
            }}>
              {bill.title}
            </h1>
            
            <p style={{ 
              margin: "0 0 1.5rem 0", 
              color: "#64748b",
              fontSize: "1.1rem",
              lineHeight: "1.6"
            }}>
              {bill.description}
            </p>
          </div>

          <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
            gap: "1.5rem",
            marginBottom: "2rem"
          }}>
            <div style={{
              backgroundColor: "#f8fafc",
              padding: "1rem",
              borderRadius: "6px",
              border: "1px solid #e2e8f0"
            }}>
              <h3 style={{ margin: "0 0 0.5rem 0", color: "#374151", fontSize: "1rem" }}>
                Introduced By
              </h3>
              <p style={{ margin: 0, color: "#1e293b", fontWeight: "500" }}>
                {bill.introducer}
              </p>
            </div>
            
            <div style={{
              backgroundColor: "#f8fafc",
              padding: "1rem",
              borderRadius: "6px",
              border: "1px solid #e2e8f0"
            }}>
              <h3 style={{ margin: "0 0 0.5rem 0", color: "#374151", fontSize: "1rem" }}>
                Bill Type
              </h3>
              <p style={{ margin: 0, color: "#1e293b", fontWeight: "500" }}>
                {bill.bill_type} {bill.bill_number} ({bill.year})
              </p>
            </div>
            
            <div style={{
              backgroundColor: "#f8fafc",
              padding: "1rem",
              borderRadius: "6px",
              border: "1px solid #e2e8f0"
            }}>
              <h3 style={{ margin: "0 0 0.5rem 0", color: "#374151", fontSize: "1rem" }}>
                Current Referral
              </h3>
              <p style={{ margin: 0, color: "#1e293b", fontWeight: "500" }}>
                {bill.current_referral}
              </p>
            </div>
            
            {bill.act_number && (
              <div style={{
                backgroundColor: "#f8fafc",
                padding: "1rem",
                borderRadius: "6px",
                border: "1px solid #e2e8f0"
              }}>
                <h3 style={{ margin: "0 0 0.5rem 0", color: "#374151", fontSize: "1rem" }}>
                  Act Number
                </h3>
                <p style={{ margin: 0, color: "#1e293b", fontWeight: "500" }}>
                  {bill.act_number}
                </p>
              </div>
            )}
          </div>

          <div style={{
            backgroundColor: "#f8fafc",
            padding: "1.5rem",
            borderRadius: "8px",
            border: "1px solid #e2e8f0"
          }}>
            <h2 style={{ 
              margin: "0 0 1rem 0", 
              color: "#1e293b",
              fontSize: "1.25rem"
            }}>
              Latest Status
            </h2>
            
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <div style={{
                  fontSize: "1.1rem",
                  fontWeight: "600",
                  color: getStatusColor(bill.latest_status.action),
                  marginBottom: "0.5rem"
                }}>
                  {bill.latest_status.action}
                </div>
                <div style={{ color: "#64748b" }}>
                  {bill.latest_status.chamber} • {new Date(bill.latest_status.date).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </div>
              </div>
              
              <div style={{
                backgroundColor: `${getStatusColor(bill.latest_status.action)}15`,
                padding: "0.75rem",
                borderRadius: "50%",
                width: "60px",
                height: "60px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center"
              }}>
                <div style={{
                  width: "20px",
                  height: "20px",
                  borderRadius: "50%",
                  backgroundColor: getStatusColor(bill.latest_status.action)
                }} />
              </div>
            </div>
          </div>
        </div>

        <div style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "2rem"
        }}>
          <div style={{
            backgroundColor: "white",
            border: "1px solid #e2e8f0",
            borderRadius: "8px",
            padding: "1.5rem",
            boxShadow: "0 1px 3px rgba(0,0,0,0.1)"
          }}>
            <h2 style={{ 
              margin: "0 0 1rem 0", 
              color: "#1e293b",
              fontSize: "1.5rem"
            }}>
              Bill Information
            </h2>
            
            <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
              <div style={{ display: "flex", justifyContent: "space-between", padding: "0.75rem 0", borderBottom: "1px solid #f1f5f9" }}>
                <span style={{ color: "#64748b" }}>Status Updates</span>
                <span style={{ fontWeight: "500" }}>{bill.status_count}</span>
              </div>
              
              <div style={{ display: "flex", justifyContent: "space-between", padding: "0.75rem 0", borderBottom: "1px solid #f1f5f9" }}>
                <span style={{ color: "#64748b" }}>Year</span>
                <span style={{ fontWeight: "500" }}>{bill.year}</span>
              </div>
              
              <div style={{ display: "flex", justifyContent: "space-between", padding: "0.75rem 0", borderBottom: "1px solid #f1f5f9" }}>
                <span style={{ color: "#64748b" }}>Bill Number</span>
                <span style={{ fontWeight: "500" }}>{bill.bill_type} {bill.bill_number}</span>
              </div>
              
              {bill.governor_message_number && (
                <div style={{ display: "flex", justifyContent: "space-between", padding: "0.75rem 0", borderBottom: "1px solid #f1f5f9" }}>
                  <span style={{ color: "#64748b" }}>Governor Message #</span>
                  <span style={{ fontWeight: "500" }}>{bill.governor_message_number}</span>
                </div>
              )}
            </div>
          </div>

          <div style={{
            backgroundColor: "white",
            border: "1px solid #e2e8f0",
            borderRadius: "8px",
            padding: "1.5rem",
            boxShadow: "0 1px 3px rgba(0,0,0,0.1)"
          }}>
            <h2 style={{ 
              margin: "0 0 1rem 0", 
              color: "#1e293b",
              fontSize: "1.5rem"
            }}>
              Resources
            </h2>
            
            <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
              {bill.current_bill_url && (
                <a
                  href={bill.current_bill_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    display: "block",
                    padding: "1rem",
                    backgroundColor: "#f8fafc",
                    border: "1px solid #e2e8f0",
                    borderRadius: "6px",
                    textDecoration: "none",
                    color: "#1e40af",
                    transition: "all 0.2s"
                  }}
                  onMouseOver={(e) => e.currentTarget.style.backgroundColor = "#f1f5f9"}
                  onMouseOut={(e) => e.currentTarget.style.backgroundColor = "#f8fafc"}
                >
                  <div style={{ fontWeight: "500", marginBottom: "0.25rem" }}>
                    View on Legislature Website
                  </div>
                  <div style={{ fontSize: "0.875rem", color: "#64748b" }}>
                    Official bill page with full text and history
                  </div>
                </a>
              )}
              
              {bill.current_pdf_url && (
                <a
                  href={bill.current_pdf_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    display: "block",
                    padding: "1rem",
                    backgroundColor: "#f8fafc",
                    border: "1px solid #e2e8f0",
                    borderRadius: "6px",
                    textDecoration: "none",
                    color: "#1e40af",
                    transition: "all 0.2s"
                  }}
                  onMouseOver={(e) => e.currentTarget.style.backgroundColor = "#f1f5f9"}
                  onMouseOut={(e) => e.currentTarget.style.backgroundColor = "#f8fafc"}
                >
                  <div style={{ fontWeight: "500", marginBottom: "0.25rem" }}>
                    Download PDF
                  </div>
                  <div style={{ fontSize: "0.875rem", color: "#64748b" }}>
                    Current version of the bill
                  </div>
                </a>
              )}
              
              {!bill.current_bill_url && !bill.current_pdf_url && (
                <div style={{
                  padding: "1rem",
                  backgroundColor: "#f8fafc",
                  border: "1px solid #e2e8f0",
                  borderRadius: "6px",
                  color: "#64748b",
                  fontStyle: "italic"
                }}>
                  No additional resources available
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}

export default BillDetailPage

export const Head: HeadFC = ({ params }) => {
  const bills = billsData as Bill[]
  const bill = bills.find(b => b.id === parseInt(params?.id || "0"))
  
  return (
    <title>
      {bill ? `${bill.current_version}: ${bill.title} - Rate My Legislator` : "Bill - Rate My Legislator"}
    </title>
  )
}