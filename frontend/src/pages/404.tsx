import * as React from "react"
import { Link, type HeadFC, type PageProps } from "gatsby"

const NotFoundPage: React.FC<PageProps> = () => {
  return (
    <main style={{ padding: "2rem", fontFamily: "system-ui, sans-serif", textAlign: "center" }}>
      <h1>Page not found</h1>
      <p>
        Sorry{" "}
        <span role="img" aria-label="Pensive emoji">
          😔
        </span>{" "}
        we couldn't find what you were looking for.
      </p>
      <Link to="/">Go home</Link>
    </main>
  )
}

export default NotFoundPage

export const Head: HeadFC = () => <title>Not found</title>