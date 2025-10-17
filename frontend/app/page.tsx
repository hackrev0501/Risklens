import Link from 'next/link'

export default function Home() {
  return (
    <div style={{display:'grid', gap: 12}}>
      <h2>Dashboard</h2>
      <nav style={{display:'flex', gap: 12}}>
        <Link href="/scans">Scans</Link>
        <Link href="/assets">Assets</Link>
        <Link href="/vulns">Vulnerabilities</Link>
        <Link href="/graph">Graph</Link>
        <Link href="/assistant">Assistant</Link>
        <Link href="/reports">Reports</Link>
        <Link href="/admin">Admin</Link>
      </nav>
      <p>Welcome. Use the nav to explore features.</p>
    </div>
  )
}
