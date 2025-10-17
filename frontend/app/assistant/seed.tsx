'use client'
import React from 'react'

const api = (path: string) => process.env.NEXT_PUBLIC_API_URL ? `${process.env.NEXT_PUBLIC_API_URL}${path}` : `http://localhost:8000${path}`

export default function SeedAssistant() {
  const seed = async () => {
    await fetch(api('/api/assistant/index'),{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({doc_id:'exploitdb', text:'RCE CVE-2023-0001 exploit available internet facing web'})})
    await fetch(api('/api/assistant/index'),{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({doc_id:'pci', text:'PCI-DSS compliance requires patching critical vulnerabilities within 30 days'})})
  }
  return (
    <div>
      <h3>Seed Assistant</h3>
      <button onClick={seed}>Seed</button>
    </div>
  )
}
