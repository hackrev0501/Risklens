'use client'
import React, { useState } from 'react'

const api = (path: string) => process.env.NEXT_PUBLIC_API_URL ? `${process.env.NEXT_PUBLIC_API_URL}${path}` : `http://localhost:8000${path}`

export default function Assistant() {
  const [q, setQ] = useState('RCE on production assets')
  const [res, setRes] = useState<any>(null)

  const ask = async () => {
    const r = await fetch(api(`/api/assistant/query?q=${encodeURIComponent(q)}`))
    setRes(await r.json())
  }

  return (
    <div>
      <h2>Assistant</h2>
      <div style={{display:'flex', gap:8}}>
        <input value={q} onChange={e=>setQ(e.target.value)} placeholder="Ask..." />
        <button onClick={ask}>Ask</button>
      </div>
      <pre>{JSON.stringify(res, null, 2)}</pre>
    </div>
  )
}
