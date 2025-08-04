import React, { useState, useMemo } from "react"
import { Link } from "gatsby"
import type { HeadFC, PageProps } from "gatsby"
import Layout from "../components/Layout"
import membersData from "../data/members.json"

interface Member {
  id: number
  member_id: number
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
  } | null
  committees: any[]
  photo_url: string | null
}

const MembersPage: React.FC<PageProps> = () => {
  const [searchTerm, setSearchTerm] = useState("")
  const [filterParty, setFilterParty] = useState("all")
  const [filterChamber, setFilterChamber] = useState("all")

  const members = membersData as Member[]

  const filteredMembers = useMemo(() => {
    return members.filter(member => {
      // Search matching - include name search and district search if term data exists
      const matchesSearch = member.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           (member.latest_term?.district_description?.toLowerCase().includes(searchTerm.toLowerCase()) || false)
      
      // Party filtering - only apply if member has term data and filter is not "all"
      const matchesParty = filterParty === "all" || 
                          (member.latest_term?.party === filterParty || false)
      
      // Chamber filtering - only apply if member has term data and filter is not "all"
      const matchesChamber = filterChamber === "all" || 
                            (member.latest_term?.district_type === filterChamber || false)

      return matchesSearch && matchesParty && matchesChamber
    })
  }, [searchTerm, filterParty, filterChamber, members])

  const parties = [...new Set(members.filter(member => member.latest_term).map(member => member.latest_term!.party))].sort()
  const chambers = [...new Set(members.filter(member => member.latest_term).map(member => member.latest_term!.district_type))].sort()

  return (
    <Layout>
      <div>
        <h1 style={{ marginBottom: "2rem", color: "#1e293b" }}>Hawaii State Legislature Members</h1>
        
        <div style={{ 
          backgroundColor: "#f8fafc", 
          padding: "1.5rem", 
          borderRadius: "8px", 
          marginBottom: "2rem",
          border: "1px solid #e2e8f0"
        }}>
          <div style={{ 
            display: "grid", 
            gridTemplateColumns: "2fr 1fr 1fr", 
            gap: "1rem",
            alignItems: "end"
          }}>
            <div>
              <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "500" }}>
                Search Members
              </label>
              <input
                type="text"
                placeholder="Search by name or district..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{
                  width: "100%",
                  padding: "0.75rem",
                  border: "1px solid #d1d5db",
                  borderRadius: "4px",
                  fontSize: "1rem"
                }}
              />
            </div>
            
            <div>
              <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "500" }}>
                Party
              </label>
              <select
                value={filterParty}
                onChange={(e) => setFilterParty(e.target.value)}
                style={{
                  width: "100%",
                  padding: "0.75rem",
                  border: "1px solid #d1d5db",
                  borderRadius: "4px",
                  fontSize: "1rem"
                }}
              >
                <option value="all">All Parties</option>
                {parties.map(party => (
                  <option key={party} value={party}>{party}</option>
                ))}
              </select>
            </div>
            
            <div>
              <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "500" }}>
                Chamber
              </label>
              <select
                value={filterChamber}
                onChange={(e) => setFilterChamber(e.target.value)}
                style={{
                  width: "100%",
                  padding: "0.75rem",
                  border: "1px solid #d1d5db",
                  borderRadius: "4px",
                  fontSize: "1rem"
                }}
              >
                <option value="all">All Chambers</option>
                {chambers.map(chamber => (
                  <option key={chamber} value={chamber}>{chamber}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        <div style={{ marginBottom: "1rem", color: "#64748b" }}>
          Showing {filteredMembers.length} of {members.length} members
        </div>

        <div style={{ 
          display: "grid", 
          gridTemplateColumns: "repeat(auto-fill, minmax(400px, 1fr))", 
          gap: "1.5rem" 
        }}>
          {filteredMembers.map(member => (
            <Link
              key={member.id}
              to={`/members/${member.id}`}
              style={{ textDecoration: "none" }}
            >
              <div style={{
                backgroundColor: "white",
                border: "1px solid #e2e8f0",
                borderRadius: "8px",
                padding: "1.5rem",
                boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
                transition: "all 0.2s",
                cursor: "pointer"
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.boxShadow = "0 4px 6px rgba(0,0,0,0.1)"
                e.currentTarget.style.transform = "translateY(-2px)"
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.boxShadow = "0 1px 3px rgba(0,0,0,0.1)"
                e.currentTarget.style.transform = "translateY(0)"
              }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
                  <div style={{
                    width: "60px",
                    height: "60px",
                    borderRadius: "50%",
                    backgroundColor: "#e2e8f0",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: "1.5rem",
                    fontWeight: "bold",
                    color: "#64748b"
                  }}>
                    {member.name.split(' ').map(n => n[0]).join('').slice(0, 2)}
                  </div>
                  
                  <div style={{ flex: 1 }}>
                    <h3 style={{ 
                      margin: "0 0 0.5rem 0", 
                      color: "#1e293b",
                      fontSize: "1.1rem"
                    }}>
                      {member.name}
                    </h3>
                    
                    <div style={{ 
                      display: "flex", 
                      gap: "0.5rem", 
                      marginBottom: "0.5rem",
                      flexWrap: "wrap"
                    }}>
                      {member.latest_term?.party && (
                        <span style={{
                          backgroundColor: member.latest_term.party === "Democratic" ? "#dbeafe" : "#fef3c7",
                          color: member.latest_term.party === "Democratic" ? "#1e40af" : "#92400e",
                          padding: "0.25rem 0.5rem",
                          borderRadius: "4px",
                          fontSize: "0.875rem",
                          fontWeight: "500"
                        }}>
                          {member.latest_term.party}
                        </span>
                      )}
                      
                      {member.latest_term?.district_type && (
                        <span style={{
                          backgroundColor: "#f1f5f9",
                          color: "#475569",
                          padding: "0.25rem 0.5rem",
                          borderRadius: "4px",
                          fontSize: "0.875rem"
                        }}>
                          {member.latest_term.district_type}
                        </span>
                      )}
                      
                      {!member.latest_term && (
                        <span style={{
                          backgroundColor: "#f3f4f6",
                          color: "#6b7280",
                          padding: "0.25rem 0.5rem",
                          borderRadius: "4px",
                          fontSize: "0.875rem"
                        }}>
                          No current term data
                        </span>
                      )}
                    </div>
                    
                    <p style={{ 
                      margin: "0 0 0.75rem 0", 
                      color: "#64748b",
                      fontSize: "0.875rem"
                    }}>
                      {member.latest_term?.district_description || "District information not available"}
                    </p>
                    
                    {member.member_id && member.latest_term && (
                      <a
                        href={`https://www.capitol.hawaii.gov/legislature/memberpage.aspx?member=${member.member_id}&year=${member.latest_term.year}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={(e) => e.stopPropagation()}
                        style={{
                          color: "#1e40af",
                          fontSize: "0.75rem",
                          textDecoration: "none",
                          display: "inline-flex",
                          alignItems: "center",
                          gap: "0.25rem"
                        }}
                        onMouseOver={(e) => e.currentTarget.style.textDecoration = "underline"}
                        onMouseOut={(e) => e.currentTarget.style.textDecoration = "none"}
                      >
                        View legislature page ↗
                      </a>
                    )}
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>

        {filteredMembers.length === 0 && (
          <div style={{
            textAlign: "center",
            padding: "3rem",
            color: "#64748b"
          }}>
            No members found matching your search criteria.
          </div>
        )}
      </div>
    </Layout>
  )
}

export default MembersPage

export const Head: HeadFC = () => <title>Members - Rate My Legislator</title>