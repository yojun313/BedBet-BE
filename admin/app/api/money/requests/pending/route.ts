import { NextResponse } from "next/server"

const API_BASE = "https://bedbet.knpu.re.kr/api"

export async function GET() {
  try {
    const response = await fetch(`${API_BASE}/money/requests/pending`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${process.env.API_TOKEN}`,
      },
    })

    if (!response.ok) {
      return NextResponse.json({ error: "Failed to fetch money requests" }, { status: response.status })
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error("Error fetching money requests:", error)
    return NextResponse.json({ error: "Internal server error" }, { status: 500 })
  }
}
