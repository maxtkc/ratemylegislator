import type { GatsbyConfig } from "gatsby"

const config: GatsbyConfig = {
  siteMetadata: {
    title: `Rate My Legislator`,
    description: `Track and rate Hawaii State Legislature performance with comprehensive data and insights.`,
    author: `@ratemylegislator`,
    siteUrl: `https://your-username.github.io`, // Update this for GitHub Pages
  },
  // Configure for GitHub Pages deployment
  pathPrefix: `/ratemylegislator`,
  // More easily incorporate content into your pages through automatic TypeScript type generation and better GraphQL IntelliSense.
  // If you use VSCode you can also use the GraphQL plugin
  // Learn more at: https://gatsby.dev/graphql-typegen
  graphqlTypegen: true,
  plugins: [
    `gatsby-plugin-image`,
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `images`,
        path: `${__dirname}/src/images`,
      },
    },
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `data`,
        path: `${__dirname}/src/data`,
      },
    },
    `gatsby-transformer-json`,
    `gatsby-transformer-sharp`,
    `gatsby-plugin-sharp`,
    {
      resolve: `gatsby-plugin-manifest`,
      options: {
        name: `Rate My Legislator`,
        short_name: `RateMyLeg`,
        start_url: `/`,
        background_color: `#1e3a8a`,
        theme_color: `#1e3a8a`,
        display: `minimal-ui`,
        icon: `src/images/hawaii-icon.png`, // You'll need to add this
      },
    },
  ],
}

export default config