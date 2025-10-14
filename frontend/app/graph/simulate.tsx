'use client'
import React, { useState } from 'react'

const api = (path: string) => process.env.NEXT_PUBLIC_API_URL ? `${process.env.NEXT_PUBLIC_API_URL}${path}` : `http://localhost:8000${path}`

export default function Simulate() {
  const [node, setNode] = useState('vuln:1')
  const [res, setRes] = useState<any>(null)

  const run = async () => {
    const r = await fetch(api(`/api/paths/simulate?remove_node=${encodeURIComponent(node)}`))
    setRes(await r.json())
  }

  return (
    <div>
      <h3>Patch Simulation</h3>
      <div style={{display:'flex', gap:8}}>
        <input value={node} onChange={e=>setNode(e.target.value)} placeholder="Node id like vuln:1" />
        <button onClick={run}>Simulate</button>
      </div>
      <pre>{JSON.stringify(res, null, 2)}</pre>
    </div>
  )
}
