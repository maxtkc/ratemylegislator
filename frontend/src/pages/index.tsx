import * as React from "react"
import type { HeadFC, PageProps } from "gatsby"

const IndexPage: React.FC<PageProps> = () => {
  return (
    <main style={{ padding: "2rem", fontFamily: "system-ui, sans-serif" }}>
      <h1>Rate My Legislator</h1>
      <p>
        Welcome to the Hawaii State Legislature tracking platform. 
        This application provides comprehensive data and insights about 
        legislative performance, bill tracking, and member information.
      </p>
      
      <div style={{ marginTop: "2rem" }}>
        <h2>Features Coming Soon:</h2>
        <ul>
          <li>📊 Legislator Performance Metrics</li>
          <li>📋 Bill Tracking and Status Updates</li>
          <li>🏛️ Committee Assignment Tracking</li>
          <li>📈 Data Visualization and Trends</li>
          <li>🔍 Search and Filter Functionality</li>
          <li>📱 Mobile-Responsive Design</li>
        </ul>
      </div>

      <div style={{ marginTop: "2rem" }}>
        <h2>About the Data</h2>
        <p>
          Our platform scrapes publicly available data from the Hawaii State Legislature
          website to provide up-to-date information about bills, members, and legislative activity.
          All data is sourced from official government records.
        </p>
      </div>

      <footer style={{ marginTop: "3rem", padding: "1rem", backgroundColor: "#f5f5f5" }}>
        <p>© 2025 Rate My Legislator - Built with Gatsby.js</p>
      </footer>
    </main>
  )
}

export default IndexPage

export const Head: HeadFC = () => <title>Rate My Legislator - Hawaii Legislature Tracking</title>