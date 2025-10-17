'use client'
import React, { useState } from 'react'
import useSWR from 'swr'
import axios from 'axios'

const api = (path: string) => process.env.NEXT_PUBLIC_API_URL ? `${process.env.NEXT_PUBLIC_API_URL}${path}` : `http://localhost:8000${path}`
const fetcher = (url: string) => fetch(url).then(r => r.json())

export default function Scans() {
  const { data, mutate } = useSWR(api('/api/scans/'), fetcher)
  const [target, setTarget] = useState('127.0.0.1')
  const [tools, setTools] = useState('nmap,nuclei,nikto')

  const startScan = async () => {
    await axios.post(api('/api/scans/'), { target, tools: tools.split(',').map(s => s.trim()) })
    mutate()
  }

  return (
    <div>
      <h2>Scans</h2>
      <div style={{display:'flex', gap:8}}>
        <input value={target} onChange={e=>setTarget(e.target.value)} placeholder="Target" />
        <input value={tools} onChange={e=>setTools(e.target.value)} placeholder="Tools (comma)" />
        <button onClick={startScan}>Start</button>
      </div>
      <div style={{marginTop:8}}>
        <button onClick={async ()=>{
          await fetch(api('/api/paths/deterministic')).then(r=>r.json()).then(console.log)
        }}>Enumerate Paths (console)</button>
      </div>
      <pre>{JSON.stringify(data?.map((s: any)=>({id:s.id, target:s.target, status:s.status})), null, 2)}</pre>
    </div>
  )
}
