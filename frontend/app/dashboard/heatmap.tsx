'use client'
import useSWR from 'swr'

const api = (path: string) => process.env.NEXT_PUBLIC_API_URL ? `${process.env.NEXT_PUBLIC_API_URL}${path}` : `http://localhost:8000${path}`
const fetcher = (url: string) => fetch(url).then(r => r.json())

export default function Heatmap() {
  const { data } = useSWR(api('/api/metrics/heatmap'), fetcher)
  return (
    <div>
      <h3>Exposure Heatmap</h3>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}
