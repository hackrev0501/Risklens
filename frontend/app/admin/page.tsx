'use client'
import useSWR from 'swr'

const api = (path: string) => process.env.NEXT_PUBLIC_API_URL ? `${process.env.NEXT_PUBLIC_API_URL}${path}` : `http://localhost:8000${path}`
const fetcher = (url: string) => fetch(url).then(r => r.json())

export default function Admin() {
  const { data } = useSWR(api('/api/admin/users'), fetcher)
  return (
    <div>
      <h2>Admin</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}
