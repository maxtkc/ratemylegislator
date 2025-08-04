import React, { useState, useMemo } from "react"
import { Link } from "gatsby"
import type { HeadFC, PageProps } from "gatsby"
import Layout from "../components/Layout"
import billsData from "../data/bills_2025.json"
import membersData from "../data/members.json"

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

const BillsPage: React.FC<PageProps> = ({ location }) => {
  const [searchTerm, setSearchTerm] = useState("")
  const [filterType, setFilterType] = useState("all")
  const [filterStatus, setFilterStatus] = useState("all")
  const [sortBy, setSortBy] = useState("date")

  const bills = billsData as Bill[]
  const members = membersData as Member[]

  const urlParams = new URLSearchParams(location.search || "")
  const memberFilter = urlParams.get("member")

  const filteredAndSortedBills = useMemo(() => {
    let filtered = bills.filter(bill => {
      const matchesSearch = (bill.title?.toLowerCase().includes(searchTerm.toLowerCase()) || false) ||
                           (bill.description?.toLowerCase().includes(searchTerm.toLowerCase()) || false) ||
                           bill.current_version.toLowerCase().includes(searchTerm.toLowerCase())
      
      const matchesType = filterType === "all" || bill.bill_type === filterType
      
      const matchesStatus = filterStatus === "all" || 
                           bill.latest_status.action.toLowerCase().includes(filterStatus.toLowerCase())

      const matchesMember = !memberFilter || 
                           (bill.introducer?.toLowerCase().includes(memberFilter.toLowerCase()) || false)

      return matchesSearch && matchesType && matchesStatus && matchesMember
    })

    return filtered.sort((a, b) => {
      switch (sortBy) {
        case "date":
          return new Date(b.latest_status.date).getTime() - new Date(a.latest_status.date).getTime()
        case "title":
          return a.title.localeCompare(b.title)
        case "bill_number":
          if (a.bill_type === b.bill_type) {
            return a.bill_number - b.bill_number
          }
          return a.bill_type.localeCompare(b.bill_type)
        default:
          return 0
      }
    })
  }, [searchTerm, filterType, filterStatus, sortBy, bills, memberFilter])

  const billTypes = [...new Set(bills.map(bill => bill.bill_type))].sort()
  const statusActions = [...new Set(bills.map(bill => bill.latest_status.action))].sort()

  const getStatusColor = (action: string) => {
    if (action.toLowerCase().includes("passed")) return "#059669"
    if (action.toLowerCase().includes("introduced")) return "#3b82f6"
    if (action.toLowerCase().includes("committee")) return "#7c3aed"
    if (action.toLowerCase().includes("failed") || action.toLowerCase().includes("killed")) return "#dc2626"
    return "#64748b"
  }

  return (
    <Layout>
      <div>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "2rem" }}>
          <h1 style={{ margin: 0, color: "#1e293b" }}>Hawaii State Legislature Bills</h1>
          {memberFilter && (
            <Link 
              to="/bills" 
              style={{ 
                color: "#1e40af", 
                textDecoration: "none",
                display: "inline-flex",
                alignItems: "center"
              }}
            >
              Clear member filter ×
            </Link>
          )}
        </div>
        
        <div style={{ 
          backgroundColor: "#f8fafc", 
          padding: "1.5rem", 
          borderRadius: "8px", 
          marginBottom: "2rem",
          border: "1px solid #e2e8f0"
        }}>
          <div style={{ 
            display: "grid", 
            gridTemplateColumns: "2fr 1fr 1fr 1fr", 
            gap: "1rem",
            alignItems: "end"
          }}>
            <div>
              <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "500" }}>
                Search Bills
              </label>
              <input
                type="text"
                placeholder="Search by title, description, or bill number..."
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
                Bill Type
              </label>
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                style={{
                  width: "100%",
                  padding: "0.75rem",
                  border: "1px solid #d1d5db",
                  borderRadius: "4px",
                  fontSize: "1rem"
                }}
              >
                <option value="all">All Types</option>
                {billTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>
            
            <div>
              <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "500" }}>
                Status
              </label>
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                style={{
                  width: "100%",
                  padding: "0.75rem",
                  border: "1px solid #d1d5db",
                  borderRadius: "4px",
                  fontSize: "1rem"
                }}
              >
                <option value="all">All Statuses</option>
                {statusActions.map(status => (
                  <option key={status} value={status}>{status}</option>
                ))}
              </select>
            </div>
            
            <div>
              <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "500" }}>
                Sort By
              </label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                style={{
                  width: "100%",
                  padding: "0.75rem",
                  border: "1px solid #d1d5db",
                  borderRadius: "4px",
                  fontSize: "1rem"
                }}
              >
                <option value="date">Latest Activity</option>
                <option value="title">Title</option>
                <option value="bill_number">Bill Number</option>
              </select>
            </div>
          </div>
        </div>

        <div style={{ marginBottom: "1rem", color: "#64748b" }}>
          Showing {filteredAndSortedBills.length} of {bills.length} bills
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
          {filteredAndSortedBills.map(bill => (
            <Link
              key={bill.id}
              to={`/bills/${bill.id}`}
              style={{ textDecoration: "none" }}
            >
              <div style={{
                backgroundColor: "white",
                border: "1px solid #e2e8f0",
                borderRadius: "8px",
                padding: "1.5rem",
                boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
                transition: "all 0.2s"
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
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "1rem" }}>
                  <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
                    <span style={{
                      backgroundColor: "#f1f5f9",
                      color: "#475569",
                      padding: "0.5rem 1rem",
                      borderRadius: "6px",
                      fontSize: "1rem",
                      fontWeight: "600"
                    }}>
                      {bill.current_version}
                    </span>
                    
                    <span style={{
                      backgroundColor: "#f0fdf4",
                      color: "#166534",
                      padding: "0.25rem 0.75rem",
                      borderRadius: "4px",
                      fontSize: "0.875rem"
                    }}>
                      {bill.current_referral}
                    </span>
                  </div>
                  
                  <div style={{ textAlign: "right", fontSize: "0.875rem", color: "#64748b" }}>
                    <div>{new Date(bill.latest_status.date).toLocaleDateString()}</div>
                    <div>{bill.latest_status.chamber}</div>
                  </div>
                </div>
                
                <h3 style={{ 
                  margin: "0 0 0.75rem 0", 
                  color: "#1e293b",
                  fontSize: "1.25rem",
                  lineHeight: "1.4"
                }}>
                  {bill.title || `${bill.bill_type}${bill.bill_number}`}
                </h3>
                
                <p style={{ 
                  margin: "0 0 1rem 0", 
                  color: "#64748b",
                  lineHeight: "1.5"
                }}>
                  {bill.description || "No description available"}
                </p>
                
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div style={{ fontSize: "0.875rem", color: "#64748b" }}>
                    Introduced by: <strong>{bill.introducer || "Unknown"}</strong>
                  </div>
                  
                  <div style={{
                    fontSize: "0.875rem",
                    fontWeight: "600",
                    color: getStatusColor(bill.latest_status.action),
                    padding: "0.25rem 0.75rem",
                    backgroundColor: `${getStatusColor(bill.latest_status.action)}10`,
                    borderRadius: "4px"
                  }}>
                    {bill.latest_status.action}
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>

        {filteredAndSortedBills.length === 0 && (
          <div style={{
            textAlign: "center",
            padding: "3rem",
            color: "#64748b"
          }}>
            No bills found matching your search criteria.
          </div>
        )}
      </div>
    </Layout>
  )
}

export default BillsPage

export const Head: HeadFC = () => <title>Bills - Rate My Legislator</title>