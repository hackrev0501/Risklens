'use client'
import useSWR from 'swr'
import axios from 'axios'
import React, { useState } from 'react'

const api = (path: string) => process.env.NEXT_PUBLIC_API_URL ? `${process.env.NEXT_PUBLIC_API_URL}${path}` : `http://localhost:8000${path}`
const fetcher = (url: string) => fetch(url).then(r => r.json())

export default function Assets() {
  const { data, mutate } = useSWR(api('/api/assets/'), fetcher)
  const [identifier, setIdentifier] = useState('127.0.0.1')
  const [tags, setTags] = useState('Payment API')

  const add = async () => {
    await axios.post(api('/api/assets/'), { identifier, tags: tags.split(',').map(s=>s.trim()) })
    mutate()
  }

  return (
    <div>
      <h2>Assets</h2>
      <div style={{display:'flex', gap:8}}>
        <input value={identifier} onChange={e=>setIdentifier(e.target.value)} placeholder="Identifier" />
        <input value={tags} onChange={e=>setTags(e.target.value)} placeholder="Tags" />
        <button onClick={add}>Add</button>
      </div>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}
