import React from "react"
import { Link } from "gatsby"
import type { HeadFC, PageProps } from "gatsby"
import Layout from "../../components/Layout"
import membersData from "../../data/members.json"
import billsData from "../../data/bills_2025.json"

interface Member {
  id: number
  member_id: number
  name: string
  bio: string | null
  latest_term: {
    year: number
    title: string
    party: string
    district_type: string
    district_number: number
    district_description: string
    district_map_url: string | null
    email: string
    phone: string
    office: string | null
    fax: string | null
    current_experience: string | null
    previous_experience: string | null
    about_content: string | null
    experience_content: string | null
    news_content: string | null
    allowance_report_url: string | null
    rss_feed_url: string | null
  } | null
  committees: {
    committee_name: string
    position: string
    committee_type: string
  }[]
  measures_introduced: {
    bill_identifier: string
    title: string
    url: string
  }[]
  links: {
    text: string
    url: string
  }[]
  photo_url: string | null
}

interface Bill {
  id: number
  bill_type: string
  bill_number: number
  year: number
  title: string | null
  description: string | null
  current_version: string
  introducer: string | null
  companion: string | null
  current_referral: string | null
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

  const memberBills = bills.filter(bill => {
    if (!bill.introducer) return false
    
    const lastName = member.name.toLowerCase().split(' ').slice(-1)[0]
    const matchesLastName = bill.introducer.toLowerCase().includes(lastName)
    
    const matchesTitle = member.latest_term?.title && 
                        bill.introducer.toLowerCase().includes(member.latest_term.title.toLowerCase())
    
    return matchesLastName || matchesTitle
  })

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
              flexShrink: 0,
              overflow: "hidden"
            }}>
              {member.photo_url ? (
                <img 
                  src={member.photo_url} 
                  alt={member.name}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover"
                  }}
                />
              ) : (
                member.name.split(' ').map(n => n[0]).join('').slice(0, 2)
              )}
            </div>
            
            <div style={{ flex: 1 }}>
              <h1 style={{ 
                margin: "0 0 1rem 0", 
                color: "#1e293b",
                fontSize: "2rem"
              }}>
                {member.name}
              </h1>
              
              {member.latest_term ? (
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
              ) : (
                <div style={{ 
                  marginBottom: "1.5rem"
                }}>
                  <span style={{
                    backgroundColor: "#f3f4f6",
                    color: "#6b7280",
                    padding: "0.5rem 1rem",
                    borderRadius: "6px",
                    fontSize: "1rem"
                  }}>
                    No current term information available
                  </span>
                </div>
              )}
              
              {member.latest_term && (
                <div style={{ 
                  display: "grid", 
                  gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", 
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
                  {member.latest_term.office && (
                    <div>
                      <strong>Office:</strong><br />
                      Room {member.latest_term.office}
                    </div>
                  )}
                  {member.latest_term.fax && (
                    <div>
                      <strong>Fax:</strong><br />
                      {member.latest_term.fax}
                    </div>
                  )}
                  <div>
                    <strong>District:</strong><br />
                    {member.latest_term.district_type} {member.latest_term.district_number}
                  </div>
                  <div>
                    <strong>Legislature Page:</strong><br />
                    <a 
                      href={`https://www.capitol.hawaii.gov/legislature/memberpage.aspx?member=${member.member_id}&year=${member.latest_term.year}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{ color: "#1e40af" }}
                    >
                      View on capitol.hawaii.gov ↗
                    </a>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Legislature Website Link */}
        {member.member_id && (
          <div style={{
            backgroundColor: "white",
            border: "1px solid #e2e8f0",
            borderRadius: "8px",
            padding: "1.5rem",
            marginBottom: "2rem",
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
              <a
                href={`https://www.capitol.hawaii.gov/legislature/memberpage.aspx?member=${member.member_id}&year=${member.latest_term?.year || 2025}`}
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
                  Official member page with biography and current information
                </div>
              </a>

              {member.latest_term?.allowance_report_url && (
                <a
                  href={member.latest_term.allowance_report_url}
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
                    📄 {member.latest_term.year} Allowance Report
                  </div>
                  <div style={{ fontSize: "0.875rem", color: "#64748b" }}>
                    View official expenditure report (PDF)
                  </div>
                </a>
              )}

              {member.latest_term?.rss_feed_url && (
                <a
                  href={member.latest_term.rss_feed_url}
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
                    🔔 RSS News Feed
                  </div>
                  <div style={{ fontSize: "0.875rem", color: "#64748b" }}>
                    Subscribe to member updates and news
                  </div>
                </a>
              )}
            </div>
          </div>
        )}

        <div style={{ display: "flex", flexDirection: "column", gap: "2rem" }}>
          {/* About/Biography Section */}
          {(member.latest_term?.about_content || member.bio) && (
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
                About
              </h2>
              <div style={{
                lineHeight: "1.6",
                color: "#374151",
                whiteSpace: "pre-wrap"
              }}>
                {member.latest_term?.about_content || member.bio}
              </div>
            </div>
          )}

          <div style={{
            display: "grid",
            gridTemplateColumns: "2fr 1fr",
            gap: "2rem"
          }}>
            {/* Measures Introduced Section */}
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
                Measures Introduced in {member.latest_term?.year || 2025}
              </h2>
              
              {member.measures_introduced && member.measures_introduced.length > 0 ? (
                <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                  {member.measures_introduced.slice(0, 10).map((measure, index) => (
                    <a
                      key={index}
                      href={measure.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        display: "block",
                        padding: "0.75rem",
                        border: "1px solid #e2e8f0",
                        borderRadius: "6px",
                        textDecoration: "none",
                        transition: "all 0.2s"
                      }}
                      onMouseOver={(e) => e.currentTarget.style.backgroundColor = "#f8fafc"}
                      onMouseOut={(e) => e.currentTarget.style.backgroundColor = "white"}
                    >
                      <div style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "flex-start",
                        gap: "1rem"
                      }}>
                        <div style={{ flex: 1 }}>
                          <div style={{
                            fontWeight: "500",
                            color: "#1e40af",
                            marginBottom: "0.25rem"
                          }}>
                            {measure.bill_identifier}
                          </div>
                          <div style={{
                            fontSize: "0.875rem",
                            color: "#374151",
                            lineHeight: "1.4"
                          }}>
                            {measure.title}
                          </div>
                        </div>
                        <span style={{
                          fontSize: "0.75rem",
                          color: "#6b7280",
                          marginTop: "0.25rem"
                        }}>
                          ↗
                        </span>
                      </div>
                    </a>
                  ))}
                  
                  {member.measures_introduced.length > 10 && (
                    <div style={{
                      textAlign: "center",
                      padding: "0.5rem",
                      color: "#64748b",
                      fontSize: "0.875rem"
                    }}>
                      +{member.measures_introduced.length - 10} more measures
                    </div>
                  )}
                </div>
              ) : (
                <p style={{ color: "#64748b", fontStyle: "italic" }}>
                  No measures introduced in {member.latest_term?.year || 2025}.
                </p>
              )}
            </div>

            {/* Committee Assignments Section */}
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
                {member.latest_term?.year || 2025} Committee Member of
              </h2>
              
              {member.committees && member.committees.length > 0 ? (
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
                      <div style={{ fontWeight: "500", color: "#1e293b" }}>
                        {committee.committee_name}
                      </div>
                      {committee.position && committee.position !== "Member" && (
                        <div style={{ fontSize: "0.875rem", color: "#64748b", marginTop: "0.25rem" }}>
                          {committee.position}
                        </div>
                      )}
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