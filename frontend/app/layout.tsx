import '../styles/globals.css'
import React from 'react'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header style={{padding: '10px', borderBottom: '1px solid #eee'}}>Unified VM Platform</header>
        <main style={{maxWidth: 1200, margin: '0 auto', padding: 16}}>{children}</main>
      </body>
    </html>
  )
}
