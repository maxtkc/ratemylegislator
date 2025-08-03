import React from "react"
import { Link } from "gatsby"
import type { HeadFC, PageProps } from "gatsby"
import Layout from "../../components/Layout"
import membersData from "../../data/members.json"
import billsData from "../../data/bills_2025.json"

interface Member {
  id: number
  name: string
  latest_term: {
    year: number
    title: string
    party: string
    district_type: string
    district_number: number
    district_description: string
    email: string
    phone: string
  }
  committees: any[]
  photo_url: string
}

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

const MemberDetailPage: React.FC<PageProps<{}, {}, {}, { id: string }>> = ({ params }) => {
  const members = membersData as Member[]
  const bills = billsData as Bill[]
  
  const member = members.find(m => m.id === parseInt(params.id))
  
  if (!member) {
    return (
      <Layout>
        <div style={{ textAlign: "center", padding: "3rem" }}>
          <h1>Member Not Found</h1>
          <p>The requested member could not be found.</p>
          <Link to="/members" style={{ color: "#1e40af", textDecoration: "none" }}>
            ← Back to Members
          </Link>
        </div>
      </Layout>
    )
  }

  const memberBills = bills.filter(bill => 
    bill.introducer.toLowerCase().includes(member.name.toLowerCase().split(' ').slice(-1)[0]) ||
    bill.introducer.toLowerCase().includes(member.latest_term.title.toLowerCase())
  )

  return (
    <Layout>
      <div>
        <Link 
          to="/members" 
          style={{ 
            color: "#1e40af", 
            textDecoration: "none",
            display: "inline-flex",
            alignItems: "center",
            marginBottom: "2rem"
          }}
        >
          ← Back to Members
        </Link>
        
        <div style={{
          backgroundColor: "white",
          border: "1px solid #e2e8f0",
          borderRadius: "8px",
          padding: "2rem",
          marginBottom: "2rem",
          boxShadow: "0 1px 3px rgba(0,0,0,0.1)"
        }}>
          <div style={{ display: "flex", alignItems: "flex-start", gap: "2rem" }}>
            <div style={{
              width: "120px",
              height: "120px",
              borderRadius: "50%",
              backgroundColor: "#e2e8f0",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "2.5rem",
              fontWeight: "bold",
              color: "#64748b",
              flexShrink: 0
            }}>
              {member.name.split(' ').map(n => n[0]).join('').slice(0, 2)}
            </div>
            
            <div style={{ flex: 1 }}>
              <h1 style={{ 
                margin: "0 0 1rem 0", 
                color: "#1e293b",
                fontSize: "2rem"
              }}>
                {member.name}
              </h1>
              
              <div style={{ 
                display: "flex", 
                gap: "1rem", 
                marginBottom: "1.5rem",
                flexWrap: "wrap"
              }}>
                <span style={{
                  backgroundColor: member.latest_term.party === "Democratic" ? "#dbeafe" : "#fef3c7",
                  color: member.latest_term.party === "Democratic" ? "#1e40af" : "#92400e",
                  padding: "0.5rem 1rem",
                  borderRadius: "6px",
                  fontSize: "1rem",
                  fontWeight: "500"
                }}>
                  {member.latest_term.party}
                </span>
                
                <span style={{
                  backgroundColor: "#f1f5f9",
                  color: "#475569",
                  padding: "0.5rem 1rem",
                  borderRadius: "6px",
                  fontSize: "1rem"
                }}>
                  {member.latest_term.title}
                </span>
                
                <span style={{
                  backgroundColor: "#f1f5f9",
                  color: "#475569",
                  padding: "0.5rem 1rem",
                  borderRadius: "6px",
                  fontSize: "1rem"
                }}>
                  {member.latest_term.district_description}
                </span>
              </div>
              
              <div style={{ 
                display: "grid", 
                gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))", 
                gap: "1rem",
                color: "#64748b"
              }}>
                <div>
                  <strong>Email:</strong><br />
                  <a href={`mailto:${member.latest_term.email}`} style={{ color: "#1e40af" }}>
                    {member.latest_term.email}
                  </a>
                </div>
                <div>
                  <strong>Phone:</strong><br />
                  <a href={`tel:${member.latest_term.phone}`} style={{ color: "#1e40af" }}>
                    {member.latest_term.phone}
                  </a>
                </div>
                <div>
                  <strong>Chamber:</strong><br />
                  {member.latest_term.district_type}
                </div>
                <div>
                  <strong>District:</strong><br />
                  District {member.latest_term.district_number}
                </div>
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
              Recent Bills
            </h2>
            
            {memberBills.length > 0 ? (
              <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
                {memberBills.slice(0, 5).map(bill => (
                  <Link
                    key={bill.id}
                    to={`/bills/${bill.id}`}
                    style={{ textDecoration: "none" }}
                  >
                    <div style={{
                      padding: "1rem",
                      border: "1px solid #e2e8f0",
                      borderRadius: "6px",
                      transition: "all 0.2s"
                    }}
                    onMouseOver={(e) => e.currentTarget.style.backgroundColor = "#f8fafc"}
                    onMouseOut={(e) => e.currentTarget.style.backgroundColor = "white"}
                    >
                      <div style={{ 
                        display: "flex", 
                        justifyContent: "space-between", 
                        alignItems: "flex-start",
                        marginBottom: "0.5rem"
                      }}>
                        <span style={{
                          backgroundColor: "#f1f5f9",
                          color: "#475569",
                          padding: "0.25rem 0.5rem",
                          borderRadius: "4px",
                          fontSize: "0.875rem",
                          fontWeight: "500"
                        }}>
                          {bill.current_version}
                        </span>
                        <span style={{
                          fontSize: "0.875rem",
                          color: "#64748b"
                        }}>
                          {new Date(bill.latest_status.date).toLocaleDateString()}
                        </span>
                      </div>
                      
                      <h3 style={{ 
                        margin: "0 0 0.5rem 0", 
                        color: "#1e293b",
                        fontSize: "1rem"
                      }}>
                        {bill.title}
                      </h3>
                      
                      <p style={{ 
                        margin: "0 0 0.5rem 0", 
                        color: "#64748b",
                        fontSize: "0.875rem",
                        lineHeight: "1.4"
                      }}>
                        {bill.description}
                      </p>
                      
                      <div style={{
                        fontSize: "0.875rem",
                        color: "#059669",
                        fontWeight: "500"
                      }}>
                        {bill.latest_status.action}
                      </div>
                    </div>
                  </Link>
                ))}
                
                {memberBills.length > 5 && (
                  <Link 
                    to={`/bills?member=${member.id}`}
                    style={{ 
                      color: "#1e40af", 
                      textDecoration: "none",
                      textAlign: "center",
                      padding: "0.5rem"
                    }}
                  >
                    View all {memberBills.length} bills →
                  </Link>
                )}
              </div>
            ) : (
              <p style={{ color: "#64748b", fontStyle: "italic" }}>
                No bills found for this member in 2025.
              </p>
            )}
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
              Committee Assignments
            </h2>
            
            {member.committees.length > 0 ? (
              <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                {member.committees.map((committee, index) => (
                  <div 
                    key={index}
                    style={{
                      padding: "0.75rem",
                      backgroundColor: "#f8fafc",
                      borderRadius: "4px",
                      border: "1px solid #e2e8f0"
                    }}
                  >
                    {committee.name || "Committee information not available"}
                  </div>
                ))}
              </div>
            ) : (
              <p style={{ color: "#64748b", fontStyle: "italic" }}>
                Committee information not available.
              </p>
            )}
          </div>
        </div>
      </div>
    </Layout>
  )
}

export default MemberDetailPage

export const Head: HeadFC = ({ params }) => {
  const members = membersData as Member[]
  const member = members.find(m => m.id === parseInt(params?.id || "0"))
  
  return (
    <title>
      {member ? `${member.name} - Rate My Legislator` : "Member - Rate My Legislator"}
    </title>
  )
}