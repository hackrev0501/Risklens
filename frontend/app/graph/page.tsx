'use client'
import useSWR from 'swr'
import axios from 'axios'
import React from 'react'
import Link from 'next/link'

const api = (path: string) => process.env.NEXT_PUBLIC_API_URL ? `${process.env.NEXT_PUBLIC_API_URL}${path}` : `http://localhost:8000${path}`
const fetcher = (url: string) => fetch(url).then(r => r.json())

export default function Graph() {
  const { data, mutate } = useSWR(api('/api/graph/'), fetcher)

  const build = async () => {
    await axios.post(api('/api/graph/build'))
    mutate()
  }

  return (
    <div>
      <h2>Attack Graph</h2>
      <button onClick={build}>Build graph</button>
      <div style={{marginTop:8}}>
        <Link href="/graph/simulate">Patch Simulation</Link>
      </div>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}
